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
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class TotalLength(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "total_length_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.term_data(csvs, "replace")
    factor_cm: ClassVar[dict[str, str]] = term_util.term_data(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    keys: ClassVar[list[str]] = """ key_with_units key_leader len_key """.split()
    units: ClassVar[list[str]] = """
        key_with_units metric_length imperial_length
        """.split()
    # ---------------------

    length: float | list[float] = None
    units_inferred: bool = None
    ambiguous: bool = None
    estimated: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {"totalLengthInMillimeters": self.length}

        if self.units_inferred:
            value |= {"totalLengthUnitsInferred": True}

        if self.ambiguous:
            value |= {"totalLengthAmbiguous": True}

        if self.estimated:
            value |= {"totalLengthEstimated": True}

        return dwc.add_dyn()

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="total_length_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="compound_length_patterns",
            compiler=cls.compound_length_patterns(),
            overwrite=["metric_length", "imperial_length", "number"],
        )
        add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="length_range_patterns",
            compiler=cls.length_range_patterns(),
            overwrite=["metric_length", "imperial_length", "number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="total_length_patterns",
            compiler=cls.total_length_patterns(),
            overwrite=["metric_length", "imperial_length", "number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.cleanup_pipe(nlp, name="total_length_cleanup")
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def total_length_patterns(cls):
        decoder = {
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "[": {"TEXT": "[", "OP": "?"},
            "]": {"TEXT": "]", "OP": "?"},
            "ambig": {"ENT_TYPE": "ambiguous_key", "OP": "+"},
            "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "key": {"ENT_TYPE": "len_key", "OP": "+"},
            "key_mm": {"ENT_TYPE": "key_with_units", "OP": "+"},
            '"': {"TEXT": {"IN": t_const.QUOTE}, "OP": "?"},
        }
        return [
            Compiler(
                label="total_length",
                keep="total_length",
                on_match="total_length_match",
                decoder=decoder,
                patterns=[
                    ' key_mm " : " [ 99 ] ',
                    '        " : " [ 99 ] mm+ ] ',
                    ' key    " : " [ 99 ] mm* ] ',
                    ' ambig  " : " [ 99 ] mm* ] ',
                ],
            ),
        ]

    @classmethod
    def compound_length_patterns(cls):
        decoder = {
            ",": {"TEXT": {"IN": t_const.COMMA}, "OP": "?"},
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "key": {"ENT_TYPE": "len_key", "OP": "+"},
            "ft": {"ENT_TYPE": "imperial_length", "OP": "+"},
            "in": {"ENT_TYPE": "imperial_length", "OP": "+"},
            "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
        }
        return [
            Compiler(
                label="total_length",
                keep="total_length",
                on_match="compound_length_match",
                decoder=decoder,
                patterns=[
                    "       99 ft ,       99 in ",
                    " key : 99 ft ,       99 in ",
                    " key : 99 ft , 99 to 99 in ",
                    "       99 ft , 99 to 99 in ",
                ],
            ),
        ]

    @classmethod
    def length_range_patterns(cls):
        decoder = {
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "key": {"ENT_TYPE": "len_key", "OP": "+"},
            "key_mm": {"ENT_TYPE": "key_with_units", "OP": "+"},
            "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
        }
        return [
            Compiler(
                label="total_length",
                keep="total_length",
                on_match="length_range_match",
                decoder=decoder,
                patterns=[
                    " key_mm+ : 99 to 99     ",
                    "           99 to 99 mm+ ",
                    " key+    : 99 to 99 mm* ",
                ],
            ),
        ]

    @classmethod
    def in_millimeters(cls, number, units):
        units = units.text.lower() if units else ""
        factor = cls.factor_mm.get(units, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def total_length_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        estimated = True if ent.text.find("[") > -1 else None

        number = next(e for e in ent.ents if e.label_ == "number")
        length = cls.in_millimeters(number, units)

        return cls.from_ent(
            ent,
            length=length,
            ambiguous=ambiguous,
            estimated=estimated,
            units_inferred=units_inferred,
        )

    @classmethod
    def compound_length_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        numbers = [e for e in ent.ents if e.label_ == "number"]

        units = [e for e in ent.ents if e.label_ == "imperial_length"]

        is_range = 3

        length = cls.in_millimeters(numbers[0], units[0])

        if len(numbers) < is_range:
            length += cls.in_millimeters(numbers[1], units[1])
            length = round(length, 2)
        else:
            length = [
                round(length + cls.in_millimeters(numbers[1], units[1]), 2),
                round(length + cls.in_millimeters(numbers[2], units[1]), 2),
            ]

        return cls.from_ent(ent, length=length, ambiguous=ambiguous)

    @classmethod
    def length_range_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        numbers = [e for e in ent.ents if e.label_ == "number"]

        length = [
            cls.in_millimeters(numbers[0], units),
            cls.in_millimeters(numbers[1], units),
        ]

        return cls.from_ent(
            ent, length=length, ambiguous=ambiguous, units_inferred=units_inferred
        )

    @classmethod
    def not_total_length_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("total_length_match")
def total_length_match(ent):
    return TotalLength.total_length_match(ent)


@registry.misc("compound_length_match")
def compound_length_match(ent):
    return TotalLength.compound_length_match(ent)


@registry.misc("length_range_match")
def length_range_match(ent):
    return TotalLength.length_range_match(ent)


@registry.misc("not_total_length_match")
def not_total_length_match(ent):
    return TotalLength.not_total_length_match(ent)
