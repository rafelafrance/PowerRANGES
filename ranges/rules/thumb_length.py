from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes.reject_match import RejectMatch
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.rules import terms as t_terms

from ranges.rules.base_length import BaseLength, DictFunc

# from traiter.pipes import add


@dataclass(eq=False)
class ThumbLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "thumb"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "thumb_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    measured_keys: ClassVar[dict[str, str]] = term_util.look_up_table(
        csvs, "measured_with"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    measured_from: str | None = None

    def as_dict(self) -> dict[str, dict[str, Any]]:
        value: dict[str, Any] = {"thumb_length": {"_parser": self.__class__.__name__}}

        if self.measured_from:
            value["thumb_length"] |= {"thumb_length_measured_from": self.measured_from}

        value["thumb_length"] |= {"thumb_length_mm": self.length}

        if self.units_inferred:
            value["thumb_length"] |= {"thumb_length_units_inferred": True}

        if self.ambiguous:
            value["thumb_length"] |= {"thumb_length_ambiguous": True}

        if self.estimated:
            value["thumb_length"] |= {"thumb_length_estimated": True}

        return value

    def to_dwc(self, dwc: DarwinCore) -> DarwinCore:
        super().to_dwc(dwc)

        if self.measured_from:
            dwc.add_dyn(thumbLengthMeasuredFrom=self.measured_from)

        return dwc

    def for_csv(self) -> dict[str, Any]:
        value: dict[str, Any] = {"thumb_length": self.length}
        if self.measured_from:
            value["thumb_length_measured_from"] = self.measured_from
        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        cls.term_pipe(nlp)
        cls.bad_length_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        # add.debug_tokens(nlp)  # ###########################################
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def check_ambiguous_key(cls, trait: "ThumbLength") -> None:
        if trait.ambiguous and trait.units_inferred:
            raise RejectMatch

    @classmethod
    def get_measured_from(cls, ent: Span, trait: "ThumbLength") -> None:
        keys = [e for e in ent.ents if e.label_ in cls.keys]
        for key in keys:
            if value := cls.measured_keys.get(key.text.lower()):
                trait.measured_from = value

    @classmethod
    def thumb_length_match(cls, ent: Span) -> "ThumbLength":
        trait = cls.to_obj(ent, DictFunc.LENGTH)
        # cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait

    @classmethod
    def thumb_length_range_match(cls, ent: Span) -> "ThumbLength":
        trait = cls.to_obj(ent, DictFunc.RANGE)
        cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait

    @classmethod
    def thumb_length_tic_match(cls, ent: Span) -> "ThumbLength":
        trait = cls.to_obj(ent, DictFunc.TIC)
        cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "ThumbLength":
        base = cls.class_dict(ent, dict_func)
        return cls(**base)


@registry.misc("thumb_length_match")
def thumb_length_match(ent: Span) -> ThumbLength:
    return ThumbLength.thumb_length_match(ent)


@registry.misc("thumb_length_range_match")
def thumb_length_range_match(ent: Span) -> ThumbLength:
    return ThumbLength.thumb_length_range_match(ent)


@registry.misc("thumb_length_tic_match")
def thumb_length_tic_match(ent: Span) -> ThumbLength:
    return ThumbLength.thumb_length_tic_match(ent)


@registry.misc("thumb_length_bad_match")
def thumb_length_bad_match(ent: Span) -> BaseLength:
    return ThumbLength.bad_match(ent)
