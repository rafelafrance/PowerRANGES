from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pylib import term_util
from traiter.rules import terms as t_terms

from ranges.rules.base_length import BaseLength, DictFunc


@dataclass(eq=False)
class TragusLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "tragus"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "tragus_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    def as_dict(self) -> dict[str, dict[str, Any]]:
        value: dict[str, Any] = {"tragus_length": {"tragus_length_mm": self.length}}
        value["tragus_length"]["_parser"] = self.__class__.__name__

        if self.units_inferred:
            value["tragus_length"] |= {"tragus_length_units_inferred": True}

        if self.ambiguous:
            value["tragus_length"] |= {"tragus_length_ambiguous": True}

        if self.estimated:
            value["tragus_length"] |= {"tragus_length_estimated": True}

        return value

    def for_csv(self) -> dict[str, Any]:
        return {"tragus_length": self.length}

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "TragusLength":
        base = cls.class_dict(ent, dict_func)
        return cls(**base)


@registry.misc("tragus_length_match")
def tragus_length_match(ent: Span) -> TragusLength:
    return TragusLength.to_obj(ent, DictFunc.LENGTH)


@registry.misc("tragus_length_range_match")
def tragus_length_range_match(ent: Span) -> TragusLength:
    return TragusLength.to_obj(ent, DictFunc.RANGE)


@registry.misc("tragus_length_tic_match")
def tragus_length_tic_match(ent: Span) -> TragusLength:
    return TragusLength.to_obj(ent, DictFunc.TIC)
