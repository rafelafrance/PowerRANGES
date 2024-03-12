from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy.tokens import Token
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base

DECODER = {
    ",": {"TEXT": {"IN": t_const.COMMA}, "OP": "?"},
    "99": {"ENT_TYPE": "number", "OP": "+"},
    ":": {"TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ}, "OP": "?"},
    "[": {"TEXT": {"IN": t_const.OPEN}, "OP": "?"},
    "]": {"TEXT": {"IN": t_const.CLOSE}, "OP": "?"},
    "ambig": {"ENT_TYPE": "ambiguous_key", "OP": "+"},
    "ft": {"ENT_TYPE": "imperial_length", "OP": "+"},
    "in": {"ENT_TYPE": "imperial_length", "OP": "+"},
    "key": {"ENT_TYPE": "len_key", "OP": "+"},
    "key_mm": {"ENT_TYPE": "key_with_units", "OP": "+"},
    "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
    '"': {"TEXT": {"IN": t_const.QUOTE}, "OP": "?"},
}


@dataclass(eq=False)
class BaseLength(Base):
    # Class vars ----------
    name: ClassVar[str] = "unknown"

    csvs: ClassVar[list[Path]] = []

    keys: ClassVar[list[str]] = """ key_with_units key_leader len_key """.split()
    units: ClassVar[list[str]] = """
        key_with_units metric_length imperial_length
        """.split()

    factor_mm: ClassVar[dict[str, str]] = {}
    # ---------------------

    length: float | list[float] = None
    units_inferred: bool = None
    ambiguous: bool = None
    estimated: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {f"{self.name}LengthInMillimeters": self.length}

        if self.units_inferred:
            value |= {f"{self.name}LengthUnitsInferred": True}

        if self.ambiguous:
            value |= {f"{self.name}LengthAmbiguous": True}

        if self.estimated:
            value |= {f"{self.name}LengthEstimated": True}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    @classmethod
    def term_pipe(cls, nlp):
        add.term_pipe(nlp, name=f"{cls.name}_length_terms", path=cls.csvs)

    @classmethod
    def compound_length_pipe(cls, nlp, *, allow_no_key=False):
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_compound_patterns",
            compiler=cls.compound_length_patterns(allow_no_key=allow_no_key),
            overwrite=["imperial_length", "number"],
        )

    @classmethod
    def range_length_pipe(cls, nlp, *, allow_no_key=False):
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_range_patterns",
            compiler=cls.range_length_patterns(allow_no_key=allow_no_key),
            overwrite=["metric_length", "imperial_length", "number"],
        )

    @classmethod
    def length_pipe(cls, nlp, *, allow_no_key=False):
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_patterns",
            compiler=cls.length_patterns(allow_no_key=allow_no_key),
            overwrite=["metric_length", "imperial_length", "number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def tic_pipe(cls, nlp, *, allow_no_key=False):
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_tic_patterns",
            compiler=cls.tic_length_patterns(allow_no_key=allow_no_key),
            overwrite=["number"],
        )

    @classmethod
    def cleanup_pipe(cls, nlp):
        add.cleanup_pipe(nlp, name=f"{cls.name}_length_cleanup")

    @classmethod
    def compound_length_patterns(cls, *, allow_no_key=False):
        patterns = [
            " key : 99 ft ,       99 in ",
            " key : 99 ft , 99 to 99 in ",
        ]
        if allow_no_key:
            patterns += [
                " 99 ft ,       99 in ",
                " 99 ft , 99 to 99 in ",
            ]

        return [
            Compiler(
                label=f"{cls.name}_length",
                keep=f"{cls.name}_length",
                on_match=f"{cls.name}_length_compound_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

    @classmethod
    def range_length_patterns(cls, *, allow_no_key=False):
        patterns = [
            ' key_mm " : " 99 to 99     ',
            ' key    " : " 99 to 99 mm* ',
            ' ambig  " : " 99 to 99 mm* ',
            ' ambig  " : " 99 to 99 mm* key mm* ',
            "              99 to 99 mm* key mm* ",
            "              99 to 99     key_mm  ",
        ]
        if allow_no_key:
            patterns += [
                " 99 to 99 mm+ ",
            ]

        return [
            Compiler(
                label=f"{cls.name}_length",
                keep=f"{cls.name}_length",
                on_match=f"{cls.name}_length_range_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

    @classmethod
    def tic_length_patterns(cls, *, allow_no_key=False):
        patterns = [
            ' key       : 99 " ',
            '     ambig : 99 " ',
            ' key ambig : 99 " ',
        ]
        if allow_no_key:
            patterns += []

        return [
            Compiler(
                label=f"{cls.name}_length",
                keep=f"{cls.name}_length",
                on_match=f"{cls.name}_length_tic_match",
                decoder=DECODER | {'"': {"TEXT": {"IN": t_const.QUOTE}}},
                patterns=patterns,
            ),
        ]

    @classmethod
    def length_patterns(cls, *, allow_no_key=False):
        patterns = [
            ' key_mm " : " [ 99 ] ',
            ' key    " : " [ 99 ] mm* ] ',
            ' ambig  " : " [ 99 ] mm* ] ',
            "              [ 99 ] mm+ ] key ",
            ' key    " : " [ 99 ] mm* ] ',
        ]
        if allow_no_key:
            patterns += [
                " [ 99 ] mm+ ] ",
            ]

        return [
            Compiler(
                label=f"{cls.name}_length",
                keep=f"{cls.name}_length",
                on_match=f"{cls.name}_length_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

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
    def match(cls, ent):
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
    def compound_match(cls, ent):
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
    def range_match(cls, ent):
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
    def tic_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        number = next(e for e in ent.ents if e.label_ == "number")
        length = cls.in_millimeters(number, "inches")

        return cls.from_ent(ent, length=length, ambiguous=ambiguous)
