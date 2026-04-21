from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler

from ranges.rules.base import Base


class DictFunc(Enum):
    LENGTH = auto()
    COMPOUND = auto()
    RANGE = auto()
    TIC = auto()


SEP = t_const.COLON + t_const.COMMA + t_const.DASH + t_const.EQ + t_const.SLASH
SEP += [r"&", r"!", r"+", r"~"]

BAD = ["tag"]

DECODER = {
    ",": {"TEXT": {"IN": t_const.COMMA}, "OP": "?"},
    "99": {"ENT_TYPE": "number", "OP": "+"},
    "=": {"TEXT": {"IN": SEP}},
    ":": {"TEXT": {"IN": SEP}, "OP": "?"},
    "[": {"TEXT": {"IN": t_const.OPEN}, "OP": "?"},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    "]": {"TEXT": {"IN": t_const.CLOSE}, "OP": "?"},
    "ambig": {"ENT_TYPE": "ambiguous_key", "OP": "+"},
    "any": {},
    "bad": {"LOWER": {"IN": BAD}},
    "bad_prefix": {"ENT_TYPE": "bad_prefix", "OP": "+"},
    "bad_suffix": {"ENT_TYPE": "bad_suffix", "OP": "+"},
    "ft": {"ENT_TYPE": "imperial_length", "OP": "+"},
    "in": {"ENT_TYPE": {"IN": ["imperial_length", "imperial_inches"]}, "OP": "+"},
    "key": {"ENT_TYPE": {"IN": ["len_key", "key_with_units"]}, "OP": "+"},
    "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "sp": {"SPACY": True},
    "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
    '"': {"TEXT": {"IN": t_const.D_QUOTE}},
    "word": {"LOWER": {"REGEX": r"^[a-z]+$"}, "OP": "?"},
}


@dataclass(eq=False)
class BaseLength(Base):
    # Class vars ----------
    name: ClassVar[str] = "unknown"

    csvs: ClassVar[list[Path]] = []

    keys: ClassVar[list[str]] = ["key_with_units", "key_leader", "len_key"]
    units: ClassVar[list[str]] = [
        "key_with_units",
        "metric_length",
        "imperial_length",
        "imperial_inches",
    ]

    factor_mm: ClassVar[dict[str, float]] = {}

    dwc_prefix: ClassVar[dict[str, str]] = {}
    replace: ClassVar[dict[str, str]] = {}
    # ---------------------

    length: float | list[float] | None = None
    units_inferred: bool | None = None
    ambiguous: bool | None = None
    estimated: bool | None = None
    _prefix: str | None = None

    def as_dict(self) -> dict[str, dict[str, Any]]:
        raise NotImplementedError

    def for_csv(self) -> dict[str, dict[str, Any]]:
        raise NotImplementedError

    def to_dwc(self, dwc: DarwinCore) -> DarwinCore:
        value = {}

        if self.length is not None:
            value |= {f"{self._prefix}LengthInMillimeters": self.length}

        if self.units_inferred:
            value |= {f"{self._prefix}LengthUnitsInferred": True}

        if self.ambiguous:
            value |= {f"{self._prefix}LengthAmbiguous": True}

        if self.estimated:
            value |= {f"{self._prefix}LengthEstimated": True}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        raise NotImplementedError

    @classmethod
    def term_pipe(cls, nlp: Language) -> None:
        add.term_pipe(
            nlp,
            name=f"{cls.name}_length_terms",
            path=cls.csvs,
        )

    @classmethod
    def length_pipe(
        cls,
        nlp: Language,
        *,
        allow_no_key: bool = False,
        label: str | None = None,
    ) -> None:
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_patterns",
            compiler=cls.length_patterns(allow_no_key=allow_no_key, label=label),
            overwrite=["metric_length", "imperial_length", "number"],
        )

    @classmethod
    def compound_length_pipe(cls, nlp: Language, *, allow_no_key: bool = False) -> None:
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_compound_patterns",
            compiler=cls.compound_length_patterns(allow_no_key=allow_no_key),
            overwrite=["imperial_length", "number"],
        )

    @classmethod
    def range_length_pipe(cls, nlp: Language, *, allow_no_key: bool = False) -> None:
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_range_patterns",
            compiler=cls.range_length_patterns(allow_no_key=allow_no_key),
            overwrite=["metric_length", "imperial_length", "number"],
        )

    @classmethod
    def bad_length_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_bad_length_patterns",
            compiler=cls.bad_length_patterns(),
            overwrite=["metric_length", "imperial_length", "number"],
        )

    @classmethod
    def tic_pipe(cls, nlp: Language, *, allow_no_key: bool = False) -> None:
        add.trait_pipe(
            nlp,
            name=f"{cls.name}_length_tic_patterns",
            compiler=cls.tic_length_patterns(allow_no_key=allow_no_key),
            overwrite=["number"],
        )

    @classmethod
    def cleanup_pipe(cls, nlp: Language, delete: list[str] | None = None) -> None:
        delete = delete or []
        delete = ["bad_length", *delete]
        add.cleanup_pipe(nlp, name=f"{cls.name}_length_cleanup", delete=delete)

    @classmethod
    def length_patterns(
        cls,
        *,
        allow_no_key: bool = False,
        label: str | None = None,
    ) -> list[Compiler]:
        label = label or f"{cls.name}_length"
        patterns = [
            ' key             "? : "? [ 99 ] mm* ] ',
            '      ambig :    "? : "? [ 99 ] mm+ ] ',
            '      ambig : sp "? : "? [ 99 ] mm+ ] ',
            '      ambig =    "? : "? [ 99 ] mm* ] ',
            ' key  ambig      "? : "? [ 99 ] mm* ] ',
            "                         [ 99 ] mm* ] [ key ] ",
            " key : word :              99   mm+ ",
        ]
        if allow_no_key:
            patterns += [
                " [ 99 ] mm+ ] ",
            ]

        return [
            Compiler(
                label=label,
                on_match=f"{cls.name}_length_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

    @classmethod
    def compound_length_patterns(cls, *, allow_no_key: bool = False) -> list[Compiler]:
        patterns = [
            " key       : 99 ft ,       99 in ",
            " key       : 99 ft , 99 to 99 in ",
            "     ambig : 99 ft ,       99 in ",
            "     ambig : 99 ft , 99 to 99 in ",
            " key ambig : 99 ft ,       99 in ",
            " key ambig : 99 ft , 99 to 99 in ",
        ]
        if allow_no_key:
            patterns += [
                " 99 ft ,       99 in ",
                " 99 ft , 99 to 99 in ",
            ]

        return [
            Compiler(
                label=f"{cls.name}_length",
                on_match=f"{cls.name}_length_compound_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

    @classmethod
    def range_length_patterns(cls, *, allow_no_key: bool = False) -> list[Compiler]:
        patterns = [
            ' key       "? : "? 99 to 99 mm* ',
            ' key ambig "? : "? 99 to 99 mm* ',
            ' key ambig "? : "? 99 to 99 mm* key mm* ',
            '     ambig "? : "? 99 to 99 mm* ',
            '     ambig "? : "? 99 to 99 mm* key mm* ',
            "                   99 to 99 mm* key mm* ",
        ]
        if allow_no_key:
            patterns += [
                " 99 to 99 mm+ ",
            ]

        return [
            Compiler(
                label=f"{cls.name}_length",
                on_match=f"{cls.name}_length_range_match",
                decoder=DECODER,
                patterns=patterns,
            ),
        ]

    @classmethod
    def tic_length_patterns(cls, *, allow_no_key: bool = False) -> list[Compiler]:
        patterns = [
            ' ambig key   : 99 "+ ',
            '       key   : 99 "+ ',
            '       ambig : 99 "+ ',
            ' key   ambig : 99 "+ ',
            " ambig key   : 99 in ",
            "       key   : 99 in ",
            "       ambig : 99 in ",
            " key   ambig : 99 in ",
        ]
        if allow_no_key:
            patterns += []

        return [
            Compiler(
                label=f"{cls.name}_length",
                on_match=f"{cls.name}_length_tic_match",
                decoder=DECODER | {'"': {"TEXT": {"IN": t_const.QUOTE}}},
                patterns=patterns,
            ),
        ]

    @classmethod
    def bad_length_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="bad_length",
                on_match=f"{cls.name}_length_bad_match",
                is_temp=True,
                decoder=DECODER,
                patterns=[
                    " bad ",
                    " bad_prefix key ",
                    " bad_prefix ambig ",
                    " bad_prefix any{,3} ambig any 99 mm* ",
                    " bad_prefix any{,5}           99 mm* ",
                    " 99 bad_suffix",
                ],
            ),
        ]

    @classmethod
    def in_millimeters(cls, number: Span, units: Span | str | None) -> float:
        units_ = ""
        if isinstance(units, Span):
            units_ = units.text.lower()
        elif isinstance(units, str):
            units_ = units.lower()

        factor = cls.factor_mm.get(units_, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def get_prefix(cls, labels: list[Span]) -> str:
        for ent in labels:
            if prefix := cls.dwc_prefix.get(ent.text.lower()):
                return prefix
        return cls.name

    @classmethod
    def get_ambiguous_and_prefix(cls, ent: Span) -> tuple[bool | None, str]:
        labels = [e for e in ent.ents if e.label_ in cls.keys]
        prefix = cls.get_prefix(labels)
        ambiguous = True if len(labels) == 0 else None
        return ambiguous, prefix

    @classmethod
    def length_match(cls, ent: Span) -> dict:
        ambiguous, prefix = cls.get_ambiguous_and_prefix(ent)

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        estimated = True if ent.text.find("[") > -1 else None

        number = next(e for e in ent.ents if e.label_ == "number")
        length = cls.in_millimeters(number, units)

        return {
            "length": length,
            "_prefix": prefix,
            "ambiguous": ambiguous,
            "estimated": estimated,
            "units_inferred": units_inferred,
            "start": ent.start_char,
            "end": ent.end_char,
        }

    @classmethod
    def compound_match(cls, ent: Span) -> dict[str, Any]:
        ambiguous, prefix = cls.get_ambiguous_and_prefix(ent)

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

        return {
            "length": length,
            "ambiguous": ambiguous,
            "_prefix": prefix,
            "start": ent.start_char,
            "end": ent.end_char,
        }

    @classmethod
    def range_match(cls, ent: Span) -> dict[str, Any]:
        ambiguous, prefix = cls.get_ambiguous_and_prefix(ent)

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        numbers = [e for e in ent.ents if e.label_ == "number"]

        length = [
            cls.in_millimeters(numbers[0], units),
            cls.in_millimeters(numbers[1], units),
        ]

        return {
            "length": length,
            "_prefix": prefix,
            "ambiguous": ambiguous,
            "units_inferred": units_inferred,
            "start": ent.start_char,
            "end": ent.end_char,
        }

    @classmethod
    def class_dict(cls, ent: Span, dict_func: DictFunc) -> dict[str, Any]:
        match dict_func:
            case DictFunc.LENGTH:
                return cls.length_match(ent)
            case DictFunc.COMPOUND:
                return cls.compound_match(ent)
            case DictFunc.RANGE:
                return cls.range_match(ent)
            case DictFunc.TIC:
                return cls.tic_match(ent)

    @classmethod
    def tic_match(cls, ent: Span) -> dict[str, Any]:
        ambiguous, prefix = cls.get_ambiguous_and_prefix(ent)

        number = next(e for e in ent.ents if e.label_ == "number")
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units = cls.replace.get(units.text, "inches") if units else "inches"
        length = cls.in_millimeters(number, units)

        return {
            "length": length,
            "ambiguous": ambiguous,
            "_prefix": prefix,
            "start": ent.start_char,
            "end": ent.end_char,
        }

    @classmethod
    def bad_match(cls, ent: Span) -> "BaseLength":
        return cls.from_ent(ent)
