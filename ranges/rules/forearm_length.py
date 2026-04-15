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
class ForearmLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "forearm"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "forearm_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    def as_dict(self) -> dict[str, dict[str, Any]]:
        value: dict[str, Any] = {"forearm_length": {"forearm_length_mm": self.length}}
        value["forearm_length"]["_parser"] = self.__class__.__name__

        if self.units_inferred:
            value["forearm_length"] |= {"forearm_length_units_inferred": True}

        if self.ambiguous:
            value["forearm_length"] |= {"forearm_length_ambiguous": True}

        if self.estimated:
            value["forearm_length"] |= {"forearm_length_estimated": True}

        return value

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "ForearmLength":
        base = cls.class_dict(ent, dict_func)
        return cls(**base)


@registry.misc("forearm_length_match")
def forearm_length_match(ent: Span) -> ForearmLength:
    return ForearmLength.to_obj(ent, DictFunc.LENGTH)


@registry.misc("forearm_length_range_match")
def forearm_length_range_match(ent: Span) -> ForearmLength:
    return ForearmLength.to_obj(ent, DictFunc.RANGE)


@registry.misc("forearm_length_tic_match")
def forearm_length_tic_match(ent: Span) -> ForearmLength:
    return ForearmLength.to_obj(ent, DictFunc.TIC)
