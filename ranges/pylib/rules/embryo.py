"""
Parse embryo traits: length and count.

These traits are intermixed in text, and Currently, traiter isn't equipped to deal
with this easily.
"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

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
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ",": {"TEXT": {"IN": SEP}, "OP": "{,2}"},
    "9": {"ENT_TYPE": "number"},
    ":": {"TEXT": {"IN": SEP}, "OP": "{,2}"},
    "=": {"TEXT": {"IN": t_const.EQ}},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "emb_key": {"ENT_TYPE": "embryo_key"},
    "key": {"ENT_TYPE": {"IN": ["len_key", "embryo_key"]}},
    "len_key": {"ENT_TYPE": "len_key"},
    "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "present": {"ENT_TYPE": {"IN": ["no", "yes"]}, "OP": "+"},
    "side": {"ENT_TYPE": "side", "OP": "+"},
    "word": {"IS_ALPHA": True, "OP": "{,2}"},
    "x": {"LOWER": {"IN": t_const.CROSS}, "OP": "?"},
    "xx": {"LOWER": {"IN": t_const.CROSS}},
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
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    # Length fields are in the parent class
    width: float = None

    # Count fields
    count: int = None
    left: int = None
    right: int = None
    female: int = None
    male: int = None
    side1: int = None
    side2: int = None

    def to_dict(self) -> dict[str, dict[str, Any]]:  # noqa: C901, PLR0912
        value = defaultdict(dict)

        if self.length is not None:
            value["embryo_size"] |= {"embryo_size_length_mm": self.length}

        if self.width is not None:
            value["embryo_size"] |= {"embryo_size_width_mm": self.width}

        if self.units_inferred is not None:
            value["embryo_size"] |= {"embryo_size_units_inferred": self.units_inferred}

        if self.ambiguous is not None:
            value["embryo_size"] |= {"embryo_size_ambiguous": self.ambiguous}

        if self.estimated is not None:
            value["embryo_size"] |= {"embryo_size_estimated": self.estimated}

        if self.count is not None:
            value["embryo_count"] |= {"embryo_count": self.count}

        if self.left is not None:
            value["embryo_count"] |= {"embryo_count_left": self.left}

        if self.right is not None:
            value["embryo_count"] |= {"embryo_count_right": self.right}

        if self.female is not None:
            value["embryo_count"] |= {"embryo_count_females": self.female}

        if self.male is not None:
            value["embryo_count"] |= {"embryo_count_males": self.male}

        if self.side1 is not None:
            value["embryo_count"] |= {"embryo_count_side_1": self.side1}

        if self.side2 is not None:
            value["embryo_count"] |= {"embryo_count_side_2": self.side2}

        if "embryo_size" in value:
            value["embryo_size"]["_parser"] = self.__class__.__name__

        if "embryo_count" in value:
            value["embryo_count"]["_parser"] = self.__class__.__name__

        return value

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

        if self.side1 is not None:
            value |= {"embryoCountSide1": self.side1}

        if self.side2 is not None:
            value |= {"embryoCountSide2": self.side2}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="embryo_terms", path=cls.csvs, delete_patterns="in")

        cls.bad_embryo_pipe(nlp)
        cls.bad_length_pipe(nlp)
        cls.embryo_mix_2_3_pipe(nlp)
        cls.embryo_mix_1_2_pipe(nlp)
        cls.embryo_mix_3_pipe(nlp)
        cls.embryo_mix_2_pipe(nlp)
        cls.embryo_mix_1_pipe(nlp)
        cls.embryo_mix_0_pipe(nlp)
        # add.debug_tokens(nlp)  # ###########################################
        cls.embryo_width_pipe(nlp)
        cls.length_pipe(nlp, label=cls.name)
        cls.embryo_count_pipe(nlp)
        cls.embryo_present_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def bad_embryo_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="bad_embryo_patterns",
            compiler=cls.bad_embryo_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_count_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_count_patterns",
            compiler=cls.embryo_count_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_present_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_present_patterns",
            compiler=cls.embryo_present_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_0_pipe(cls, nlp):
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_0_patterns",
            compiler=cls.embryo_mix_0_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_1_pipe(cls, nlp):
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_patterns",
            compiler=cls.embryo_mix_1_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_1_2_pipe(cls, nlp):
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_2_patterns",
            compiler=cls.embryo_mix_1_2_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_2_pipe(cls, nlp):
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_patterns",
            compiler=cls.embryo_mix_2_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_2_3_pipe(cls, nlp):
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_3_patterns",
            compiler=cls.embryo_mix_2_3_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_3_pipe(cls, nlp):
        """Length is at index 3."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_3_patterns",
            compiler=cls.embryo_mix_3_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_width_pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="embryo_width_patterns",
            compiler=cls.embryo_width_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def bad_embryo_patterns(cls):
        return [
            Compiler(
                label="bad_embryo",
                on_match="bad_embryo_match",
                decoder=DECODER,
                patterns=[
                    " 9 / 9",
                ],
            ),
        ]

    @classmethod
    def embryo_count_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_count_match",
                decoder=DECODER,
                patterns=[
                    "              ( 9 ( side ) , 9 ( side ) : key+ ",
                    "   emb_key+ : ( 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) : 9 ",
                    "   emb_key+ : 9  ",
                    "   emb_key+ : 9 ( side ) x 9 ( side ) ",
                    "   emb_key+ : 9 [+] 9 = 9 ",
                    "   emb_key+ : 9 key* , ( 9 ( side ) , 9 ( side ) ",
                    " 9 present+ emb_key+",
                    " 9 word emb_key+ ",
                    " 9 word emb_key+ , ( side ) , 9 ( side ) ",
                    " 9 word emb_key+ : ( 9 ( side ) , word 9 ( side ) ",
                    " 9 word emb_key+ word ( side ) word , 9 word ( side ) ",
                    " 9 word key+ ( side ) , 9 , word ( side ) , 9 ) ",
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
                    "           present word emb_key+ ",
                    "emb_key+ :         ( side ) ",
                    "emb_key+ : present ",
                    "emb_key+ : present ( side ) ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_0_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_0_match",
                decoder=DECODER,
                patterns=[
                    " 9 mm+ , key+ , 9 ( side ) ",
                    " 9 mm+ , key+ , 9 ( side ) , 9 ( side ) ",
                    " 9 mm+ , key+ , 9",
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
                    "      9 key+ ( side ) word , 9 mm* , 9 key+ ( side ) ",
                    "      9 key+ word , 9 mm+ ",
                    "      9 key+ word , 9 mm+ , ( 9 ( side ) , 9 ( side ) ",
                    " ( side ) word 9 : key+ , 9 mm* ",
                    " ( side ) word 9 : key+ , 9 mm* , ( side ) word 9 ",
                    " ( side ) word 9 : key+ x , 9 mm* ",
                    " ( side ) word 9 : key+ x , 9 mm* , ( side ) word 9 ",
                    " 9 9 mm+ key+ ",
                    " 9 9 mm+ key+ , 9 ( side ) , 9 ( side ) ",
                    " emb_key+ ( side ) word , 9 , word ( side ) , key* 9 mm+ ) ",
                    " emb_key+ , 9 , ( side ) ( len_key+ , 9 mm* ) , 9 ( side ) ",
                    " emb_key+ , 9 , len_key+ , 9 mm* ",
                    " emb_key+ , 9 , len_key+ , 9 mm* , 9 ( side ) x 9 ( side ) ",
                    " emb_key+ 9 x 9 ( side ) , 9 , ( side ) 9 ) ",
                    " emb_key+ 9 x 9 ( side ) , 9 , word ( side ) ",
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
                    "      9 key+ word , 9 x 9 mm+ , ( 9 side , 9 side ) ",
                    "      9 key+ word , 9 x 9 mm+ ",
                    " side 9 key+ word , 9 x 9 mm* , side 9 key+ ",
                    "      9 key+ side word , 9 x 9 mm* , key* 9 side ",
                    "      9 key+ side word , 9 x 9 mm* , key* side 9 ",
                    "      9 key+ side word , 9 x 9 mm* , 9 key* side ",
                    "      9 key+ side word , 9 x 9 mm* ",
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
                    " 9 key+ : ( side word , 9 , word side ,     9 mm+ ) ",
                    " 9      :   side word , 9 , word side ,     9 mm+   , key+ ",
                    "            side word , 9 , side word , 9 : 9 mm*   , key+ ",
                    "            side word , 9 , side word , 9 , key+ 9 mm+ ",
                    "   key+ : ( side word , 9 , side word , 9 , key* 9 mm+ ) ",
                    "   key+ : ( side ) word , 9 , ( side ) word , 9 , key* 9 mm+ ",
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
                    " 9 key+          word , 9 word ( side ) , 9 x 9 mm* ",
                    " 9 key+ ( side ) word , 9 word ( side ) , 9 x 9 mm* ",
                    " 9 key+ ( side ) word , ( 9 word )      , 9 x 9 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_3_patterns(cls):
        return [
            Compiler(
                label="embryo",
                keep="embryo",
                on_match="embryo_mix_3_match",
                decoder=DECODER,
                patterns=[
                    " 9 key+ : ( 9   side   word , 9 , word   side ,   : 9 mm* ) ",
                    " 9 key+ :   9 ( side ) word , 9 , word ( side ) , : 9 mm* ",
                    " 9      :   9 ( side ) word , 9 , word ( side ) , : 9 mm* , key+ ",
                    " key+ : ( 9 side   word , 9 ,   side   word , 9 , : key* 9 mm* ) ",
                    " key+ :   9 ( side ) word , 9 , ( side ) word , 9 , : key* 9 mm* ",
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
                    "key+ : 9 xx 9 mm* ",
                ],
            ),
        ]

    @classmethod
    def add_sides(cls, data, counts, sides):
        for count, side in zip(counts, sides, strict=False):
            if side == "both":
                data["left"] = count
                data["right"] = count
                data["count"] = count + count
            else:
                data[side] = count

    @classmethod
    def get_sides(cls, ent, counts):
        needs_sides = 3
        sides = [e for e in ent.ents if e.label_ == "side"]
        sides = [cls.side.get(s.text.lower()) for s in sides]
        sides = sides if sides or len(counts) != needs_sides else ["side1", "side2"]
        return sides

    @classmethod
    def embryo_count_match(cls, ent):
        counts = [e for e in ent.ents if e.label_ == "number"]
        counts = [int(c._.trait.number) for c in counts]

        sides = cls.get_sides(ent, counts)

        if len(counts) > len(sides):
            total = max(counts)
            counts.remove(total)
        else:
            total = sum(counts)

        data = {"count": total}
        cls.add_sides(data, counts, sides)

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

        sides = cls.get_sides(ent, counts)

        if len(counts) > len(sides):
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

        cls.add_sides(data, counts, sides)

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

    @classmethod
    def bad_embryo_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("embryo_count_match")
def embryo_count_match(ent):
    return Embryo.embryo_count_match(ent)


@registry.misc("embryo_present_match")
def embryo_present_match(ent):
    return Embryo.embryo_present_match(ent)


@registry.misc("embryo_length_match")
def embryo_length_match(ent):
    return Embryo.length_match(ent)


@registry.misc("embryo_mix_0_match")
def embryo_mix_0_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=0)


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


@registry.misc("embryo_mix_3_match")
def embryo_mix_3_match(ent):
    return Embryo.embryo_mix_match(ent, length_idx=3)


@registry.misc("embryo_length_bad_match")
def embryo_length_bad_match(ent):
    return Embryo.bad_match(ent)


@registry.misc("embryo_width_match")
def embryo_width_match(ent):
    return Embryo.embryo_width_match(ent)


@registry.misc("bad_embryo_match")
def bad_embryo_match(ent):
    return Embryo.bad_embryo_match(ent)
