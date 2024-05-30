"""
Parse ovary traits: length and size.

These traits are intermixed in text, and Currently, traiter isn't equipped to deal
with this easily.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Token
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Ovary(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "ovary_terms.csv",
    ]

    side_map: ClassVar[dict[str, str]] = {
        "left": "left_side",
        "right": "right_side",
        "both": "both_sides",
        "left_ovary": "left_side",
        "right_ovary": "right_side",
    }

    keys: ClassVar[list[str]] = """
        ovary_len ovary_len_mm ovary_width ovary_width_mm """.split()

    sides: ClassVar[list[str]] = ["left", "right", "both"]
    side_ovary: ClassVar[list[str]] = ["left_ovary", "right_ovary"]
    all_sides: ClassVar[list[str]] = sides + side_ovary

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    units: ClassVar[list[str]] = ["metric_length", "imperial_length"]

    descriptors: ClassVar[list[str]] = """
        active albicans color corpus covered cyst destroyed developed fallopian luteum
        mature other size texture visible
        """.split()

    decoder: ClassVar[dict[str, dict]] = {
        "'": {"LOWER": {"IN": t_const.QUOTE}, "OP": "?"},
        ",": {"LOWER": {"IN": list(":;,.-=<>")}, "OP": "?"},
        "9": {"ENT_TYPE": "number", "OP": "+"},
        "[+]": {"LOWER": {"IN": t_const.PLUS + t_const.DASH}, "OP": "?"},
        "adp": {"POS": "ADP", "OP": "*"},
        "albicans": {"ENT_TYPE": "albicans", "OP": "+"},
        "and": {"ENT_TYPE": "and", "OP": "+"},
        "corpus": {"ENT_TYPE": "corpus", "OP": "+"},
        "covered": {"ENT_TYPE": "covered", "OP": "+"},
        "descr": {"ENT_TYPE": "description", "OP": "+"},
        "descriptors": {"ENT_TYPE": {"IN": descriptors}, "OP": "+"},
        "fallopian": {"ENT_TYPE": "fallopian", "OP": "+"},
        "fat": {"ENT_TYPE": "fat", "OP": "+"},
        "horn": {"ENT_TYPE": "horn", "OP": "+"},
        "key": {"ENT_TYPE": {"IN": keys}, "OP": "+"},
        "linker": {"ENT_TYPE": "linker", "OP": "*"},
        "luteum": {"ENT_TYPE": "luteum", "OP": "+"},
        "mm": {"ENT_TYPE": {"IN": units}, "OP": "*"},
        "non": {"ENT_TYPE": "non", "OP": "+"},
        "ovaries": {"ENT_TYPE": "ovaries", "OP": "+"},
        "ovary": {"ENT_TYPE": "ovary", "OP": "+"},
        "side": {"ENT_TYPE": {"IN": sides}},
        "side_ovary": {"ENT_TYPE": {"IN": side_ovary}, "OP": "+"},
        "uterus": {"ENT_TYPE": "uterus", "OP": "+"},
        "word": {"LOWER": {"REGEX": r"^[a-z]\w*$"}},
        "x": {"LOWER": {"IN": t_const.CROSS}},
    }
    # ---------------------

    description: str = None
    left_side: str = None
    right_side: str = None
    both_sides: str = None

    length: float = None
    length2: float = None

    width: float = None
    width2: float = None

    units_inferred: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}

        if self.description is not None:
            value |= {"ovaryDescription": self.description}

        if self.left_side is not None:
            value |= {"ovaryDescriptionLeft": self.left_side}

        if self.right_side is not None:
            value |= {"ovaryDescriptionRight": self.right_side}

        if self.both_sides is not None:
            value |= {"ovaryDescriptionBothSides": self.both_sides}

        if self.length is not None:
            value |= {"ovaryLength": self.length}

        if self.length2 is not None:
            value |= {"ovaryLength2": self.length2}

        if self.width is not None:
            value |= {"ovaryWidth": self.width}

        if self.width2 is not None:
            value |= {"ovaryWidth2": self.width2}

        if self.units_inferred is not None:
            value |= {"ovaryUnitsInferred": self.units_inferred}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="ovary_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="ovary_grouper_patterns",
            compiler=cls.ovary_grouper_patterns(),
        )

        add.trait_pipe(
            nlp,
            name="ovary_description_patterns",
            compiler=cls.ovary_description_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="ovary_keyed_size_patterns",
            compiler=cls.ovary_keyed_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="ovary_size_patterns",
            compiler=cls.ovary_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="ovary_state_patterns",
            compiler=cls.ovary_state_patterns(),
            overwrite=["number"],
        )

        # add.debug_tokens(nlp)  # ###########################################

        add.cleanup_pipe(nlp, name="ovary_cleanup")

    @classmethod
    def ovary_grouper_patterns(cls):
        return [
            Compiler(
                label="ovaries",
                on_match="ovary_grouper_match",
                decoder=cls.decoder,
                patterns=[
                    " ovary ",
                    " ovary and? uterus horn? ",
                    " ovary and? fallopian ",
                ],
            ),
        ]

    @classmethod
    def ovary_description_patterns(cls):
        return [
            Compiler(
                label="description",
                on_match="ovary_description_match",
                decoder=cls.decoder,
                patterns=[
                    " 9? adp descriptors ",
                    " 9? non descriptors ",
                    " [+] descriptors ",
                    " [+] descriptors , and? non? descriptors ",
                    " [+] descriptors word? word? fat  ",
                ],
            ),
        ]

    @classmethod
    def ovary_state_patterns(cls):
        return [
            Compiler(
                label="ovary",
                keep="ovary",
                on_match="ovary_state_match",
                decoder=cls.decoder,
                patterns=[
                    " descr , adp , side* , ovaries ",
                    " ovaries , descr ",
                    " ovaries , side* , adp , descr ",
                    " ovaries , side* descr , side* descr ",
                    " ovaries , side* linker descr ",
                    " side+ , adp , ovaries        , descr ",
                    " side+ linker  ovaries linker , descr ",
                    " side_ovary descr , side_ovary descr , side* ovaries descr ",
                ],
            ),
        ]

    @classmethod
    def ovary_size_patterns(cls):
        return [
            Compiler(
                label="ovary",
                keep="ovary",
                on_match="ovary_size_match",
                decoder=cls.decoder,
                patterns=[
                    " side* ovaries ,         9        mm ",
                    " side* ovaries ,         9 mm x 9 mm ",
                    " side* ovaries ,         9        mm , descr ",
                    " side* ovaries ,         9 mm x 9 mm , descr ",
                    " side* ovaries , descr , 9        mm ",
                    " side* ovaries , descr , 9 mm x 9 mm ",
                    " side* ovaries , descr , 9 mm x 9 mm , 9 mm x 9 mm ",
                    " side* ovaries ,         9 mm x 9 mm , 9 mm x 9 mm ",
                    " ovaries , descr , side* 9 mm x 9 mm , side* 9 mm x 9 mm ",
                    " ovaries ,         side* 9 mm x 9 mm , side* 9 mm x 9 mm ",
                ],
            ),
        ]

    @classmethod
    def ovary_keyed_size_patterns(cls):
        return [
            Compiler(
                label="ovary",
                keep="ovary",
                on_match="ovary_keyed_size_match",
                decoder=cls.decoder,
                patterns=[
                    " key ' , ' 9 mm ",
                ],
            ),
        ]

    @classmethod
    def ovary_grouper_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def ovary_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def in_millimeters(cls, number, units: Token | str | None):
        if hasattr(units, "text"):
            units = units.text.lower()
        elif isinstance(units, str):
            units = units.lower()

        factor = cls.factor_mm.get(units, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def ovary_state_match(cls, ent):
        data = {}

        sides = [e.label_ for e in ent.ents if e.label_ in cls.all_sides]
        descr = [e.text.lower() for e in ent.ents if e.label_ == "description"]
        if sides and descr:
            for side, desc in zip(sides, descr, strict=False):
                data[cls.side_map[side]] = desc
        elif descr:
            data["description"] = descr[0]

        return cls.from_ent(ent, **data)

    @classmethod
    def ovary_size_match(cls, ent):
        data = {}

        units = next((e for e in ent.ents if e.label_ in cls.units), None)

        sides = [e.label_ for e in ent.ents if e.label_ in cls.all_sides]

        nums = [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]

        one_pair = 2
        two_pairs = 4

        data["length"] = nums[0]
        data["width"] = nums[1] if len(nums) > 1 else None
        data["length2"] = nums[2] if len(nums) > one_pair else None
        data["width2"] = nums[3] if len(nums) >= two_pairs else None

        # Match the description to the side
        descr = next(
            (e.text.lower() for e in ent.ents if e.label_ == "description"), None
        )
        if sides and descr:
            data[cls.side_map[sides[0]]] = descr
        elif descr:
            data["description"] = descr

        data["units_inferred"] = True if units is None else None

        return cls.from_ent(ent, **data)

    @classmethod
    def ovary_keyed_size_match(cls, ent):
        data = {}
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        key = next((e.label_ for e in ent.ents if e.label_ in cls.keys), None)
        val = next(
            (cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"),
            None,
        )

        if not units and key in ("ovary_len", "ovary_width"):
            data["units_inferred"] = True

        if key in ("ovary_len", "ovary_len_mm"):
            data["length"] = val
        else:
            data["width"] = val

        return cls.from_ent(ent, **data)


@registry.misc("ovary_grouper_match")
def ovary_grouper_match(ent):
    return Ovary.ovary_grouper_match(ent)


@registry.misc("ovary_description_match")
def ovary_description_match(ent):
    return Ovary.ovary_description_match(ent)


@registry.misc("ovary_state_match")
def ovary_state_match(ent):
    return Ovary.ovary_state_match(ent)


@registry.misc("ovary_size_match")
def ovary_size_match(ent):
    return Ovary.ovary_size_match(ent)


@registry.misc("ovary_keyed_size_match")
def ovary_keyed_size_match(ent):
    return Ovary.ovary_keyed_size_match(ent)
