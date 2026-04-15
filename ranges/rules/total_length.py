from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pylib import term_util
from traiter.rules import terms as t_terms

from ranges.rules.base_length import BaseLength, DictFunc

# from traiter.pipes import add


@dataclass(eq=False)
class TotalLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "total"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "total_length_terms.csv",
    ]
    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    def as_dict(self) -> dict[str, dict[str, Any]]:
        value: dict[str, Any] = {"total_length": {"total_length_mm": self.length}}
        value["total_length"]["_parser"] = self.__class__.__name__

        if self.units_inferred:
            value["total_length"] |= {"total_length_units_inferred": True}

        if self.ambiguous:
            value["total_length"] |= {"total_length_ambiguous": True}

        if self.estimated:
            value["total_length"] |= {"total_length_estimated": True}

        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        cls.term_pipe(nlp)
        cls.bad_length_pipe(nlp)
        cls.compound_length_pipe(nlp, allow_no_key=True)
        cls.range_length_pipe(nlp, allow_no_key=True)
        cls.tic_pipe(nlp, allow_no_key=True)
        cls.length_pipe(nlp)
        # add.debug_tokens(nlp)  # ###########################################
        cls.cleanup_pipe(nlp)

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "TotalLength":
        base = cls.class_dict(ent, dict_func)
        return cls(**base)


@registry.misc("total_length_match")
def total_length_match(ent: Span) -> TotalLength:
    return TotalLength.to_obj(ent, DictFunc.LENGTH)


@registry.misc("total_length_compound_match")
def total_length_compound_match(ent: Span) -> TotalLength:
    return TotalLength.to_obj(ent, DictFunc.COMPUND)


@registry.misc("total_length_tic_match")
def total_length_tic_match(ent: Span) -> TotalLength:
    return TotalLength.to_obj(ent, DictFunc.TIC)


@registry.misc("total_length_range_match")
def total_length_range_match(ent: Span) -> TotalLength:
    return TotalLength.to_obj(ent, DictFunc.RANGE)


@registry.misc("total_length_bad_match")
def total_length_bad_match(ent: Span) -> BaseLength:
    return TotalLength.bad_match(ent)
