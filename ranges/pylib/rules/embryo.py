"""
Parse embryo traits: length and count.

These traits are intermixed in text, and Currently, traiter isn't equipped to deal
with this.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import SEP, BaseLength

DECODER = {
    "(": {"TEXT": {"IN": t_const.OPEN}, "OP": "?"},
    ")": {"TEXT": {"IN": t_const.CLOSE}, "OP": "?"},
    ",": {"LOWER": {"REGEX": r"^([a-z]+|[!+,/~\-])$"}, "OP": "{,2}"},
    "99": {"ENT_TYPE": "number", "OP": "+"},
    ":": {"TEXT": {"IN": SEP}, "OP": "?"},
    "emb_key": {"ENT_TYPE": "embryo_key"},
    "key": {"ENT_TYPE": {"IN": ["len_key", "embryo_key"]}},
    "len_key": {"ENT_TYPE": "len_key"},
    "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "present": {"ENT_TYPE": {"IN": ["no", "yes"]}, "OP": "+"},
    "side": {"ENT_TYPE": "side", "OP": "+"},
    "word": {"LOWER": {"REGEX": r"^[a-z]+$"}, "OP": "?"},
    "x": {"LOWER": {"IN": t_const.CROSS}, "OP": "?"},
}


@dataclass(eq=False)
class Embryo(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "embryo"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "embryo_length_terms.csv",
        Path(__file__).parent / "terms" / "embryo_count_terms.csv",
    ]
    side: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "side")

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    # Length fields are in the parent class
    width: float = None

    # Count fields
    count: int = None
    left: int = None
    right: int = None
    female: int = None
    male: int = None
    one: int = None
    two: int = None

    def to_dwc(self, dwc) -> DarwinCore:
        super().to_dwc(dwc)  # Get length fields

        value = {}

        if self.width is not None:
            value |= {"embryoWidthInMillimeters": self.width}

        if self.count is not None:
            value |= {"embryoCount": self.count}

        if self.left is not None:
            value |= {"embryoCountLeft": self.left}

        if self.right is not None:
            value |= {"embryoCountRight": self.right}

        if self.female is not None:
            value |= {"embryoCountFemale": self.female}

        if self.male is not None:
            value |= {"embryoCountMale": self.male}

        if self.one is not None:
            value |= {"embryoCountSide1": self.one}

        if self.two is not None:
            value |= {"embryoCountSide2": self.two}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="embryo_terms", path=cls.csvs, delete_patterns="in")

        cls.bad_length_pipe(nlp)
        cls.embryo_width_pipe(nlp)
        cls.embryo_mix_1_2_pipe(nlp)
        cls.embryo_mix_1_pipe(nlp)
        cls.embryo_mix_2_3_pipe(nlp)
        cls.embryo_mix_2_pipe(nlp)
        cls.embryo_count_pipe(nlp)
        cls.embryo_present_pipe(nlp)
        cls.length_pipe(nlp, label=cls.name)
        cls.cleanup_pipe(nlp)

    @classmethod
    def embryo_count_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_count_patterns",
            compiler=cls.embryo_count_patterns(),
            overwrite=["number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_present_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_present_patterns",
            compiler=cls.embryo_present_patterns(),
            overwrite=["number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_mix_1_pipe(cls, nlp):
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_patterns",
            compiler=cls.embryo_mix_1_patterns(),
            overwrite="number metric_length imperial_length".split(),
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_mix_1_2_pipe(cls, nlp):
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_2_patterns",
            compiler=cls.embryo_mix_1_2_patterns(),
            overwrite="number metric_length imperial_length".split(),
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_mix_2_pipe(cls, nlp):
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_patterns",
            compiler=cls.embryo_mix_2_patterns(),
            overwrite="number metric_length imperial_length".split(),
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_mix_2_3_pipe(cls, nlp):
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_3_patterns",
            compiler=cls.embryo_mix_2_3_patterns(),
            overwrite="number metric_length imperial_length".split(),
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_width_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_width_patterns",
            compiler=cls.embryo_width_patterns(),
            overwrite="number metric_length imperial_length".split(),
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def embryo_count_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_count_match",
                decoder=DECODER,
                patterns=[
                    "emb_key+ : 99  ",
                    "           99 word emb_key+ ",
                    "emb_key+ : 99      emb_key* , ( 99 side , 99 side ) ",
                    "           99 word emb_key+ , ( 99 side , 99 side ) ",
                    "                   emb_key+ , ( 99 side , 99 side ) ",
                    "                   emb_key+ : ( 99 side , 99 side ) ",
                    "                   emb_key+ : ( 99 side ) ",
                    "                              ( 99 side , 99 side ) : key+ ",
                    "           99 word emb_key+        side , 99 side ",
                    " 99 word  word     emb_key+ ",
                    "                   emb_key+ : ( 99 side , 99 side ) : 99 ",
                    " 99 emb_key word side word ,    99 word side ",
                    " 99 present+ emb_key+",
                    " emb_key+ : 99 side x 99 side ",
                ],
            ),
        ]

    @classmethod
    def embryo_present_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_present_match",
                decoder=DECODER,
                patterns=[
                    "emb_key+ : present ",
                    "emb_key+ : present side ",
                    "emb_key+ :         side ",
                    "           present word word emb_key+ ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_1_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_1_match",
                decoder=DECODER,
                patterns=[
                    "      99 key+ word , 99 mm+ , ( 99 side , 99 side ) ",
                    "      99 key+ word , 99 mm+ ",
                    " side 99 key+ word , 99 mm* , side 99 key+ ",
                    "      99 key+ side word , 99 mm* , 99 key+ side ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_1_2_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_1_2_match",
                decoder=DECODER,
                patterns=[
                    "      99 key+ word , 99 x 99 mm+ , ( 99 side , 99 side ) ",
                    "      99 key+ word , 99 x 99 mm+ ",
                    " side 99 key+ word , 99 x 99 mm* , side 99 key+ ",
                    "      99 key+ side word , 99 x 99 mm* , key* 99 side ",
                    "      99 key+ side word , 99 x 99 mm* , key* side 99 ",
                    "      99 key+ side word , 99 x 99 mm* , 99 key* side ",
                    "      99 key+ side word , 99 x 99 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_2_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_2_match",
                decoder=DECODER,
                patterns=[
                    " 99 key+ side word , 99 word side ,      99 mm* ",
                    "    key+ side word , 99 word side , key* 99 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_2_3_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_2_3_match",
                decoder=DECODER,
                patterns=[
                    " 99 key+ side word , 99 word side , 99 x 99 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_width_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_width_match",
                decoder=DECODER,
                patterns=[
                    "key+ : 99 x 99 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_count_match(cls, ent):
        counts = [e for e in ent.ents if e.label_ == "number"]
        counts = [int(c._.trait.number) for c in counts]

        sides = [e for e in ent.ents if e.label_ == "side"]
        sides = [cls.side.get(s.text.lower()) for s in sides]

        if len(counts) > len(sides):
            total = max(counts)
            counts.remove(total)
        else:
            total = sum(counts)

        data = {"count": total}

        for count, side in zip(counts, sides, strict=False):
            data[side] = count

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_present_match(cls, ent):
        side = [e for e in ent.ents if e.label_ == "side"]
        side = [cls.side.get(s.text.lower()) for s in side]

        count = 1 if any(e.label_ == "yes" for e in ent.ents) or side else 0
        count = 1 if side else count

        data = {"count": count}

        if side:
            data[side[0]] = count

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_mix_match(cls, ent, length_idx, width_idx=None):
        counts = [e for e in ent.ents if e.label_ == "number"]

        length = counts.pop(length_idx)
        width = counts.pop(width_idx - 1) if width_idx else None

        counts = [int(c._.trait.number) for c in counts]

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        length = cls.in_millimeters(length, units)
        if width:
            width = cls.in_millimeters(width, units)

        side_lbs = [e for e in ent.ents if e.label_ == "side"]
        side_lbs = [cls.side.get(s.text.lower()) for s in side_lbs]

        if len(counts) > len(side_lbs):
            total = max(counts)
            counts.remove(total)
        else:
            total = sum(counts)

        data = {
            "_prefix": "embryo",
            "length": length,
            "width": width,
            "count": total,
        }

        for count, side in zip(counts, side_lbs, strict=False):
            data[side] = count

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_width_match(cls, ent):
        length, width = (e for e in ent.ents if e.label_ == "number")

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        length = cls.in_millimeters(length, units)
        width = cls.in_millimeters(width, units)

        data = {
            "_prefix": "embryo",
            "length": length,
            "width": width,
            "units_inferred": units_inferred,
        }

        return cls.from_ent(ent, **data)


@registry.misc("embryo_count_match")
def embryo_count_match(ent):
    return Embryo.embryo_count_match(ent)


@registry.misc("embryo_present_match")
def embryo_present_match(ent):
    return Embryo.embryo_present_match(ent)


@registry.misc("embryo_length_match")
def embryo_length_match(ent):
    return Embryo.length_match(ent)


@registry.misc("embryo_mix_1_match")
def embryo_mix_1_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=1)


@registry.misc("embryo_mix_1_2_match")
def embryo_mix_1_2_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=1, width_idx=2)


@registry.misc("embryo_mix_2_match")
def embryo_mix_2_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=2)


@registry.misc("embryo_mix_2_3_match")
def embryo_mix_2_3_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=2, width_idx=3)


@registry.misc("embryo_length_bad_match")
def embryo_length_bad_match(ent):
    return Embryo.bad_match(ent)


@registry.misc("embryo_width_match")
def embryo_width_match(ent):
    return Embryo.embryo_width_match(ent)
