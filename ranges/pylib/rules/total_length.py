from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import BaseLength


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
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    def labeled(self) -> dict[str, dict[str, Any]]:
        value = {"total length": {"total length": self.length}}

        if self.units_inferred:
            value["total length"] |= {"total length units inferred": True}

        if self.ambiguous:
            value["total length"] |= {"total length ambiguous": True}

        if self.estimated:
            value["total length"] |= {"total length estimated": True}

        return value

    @classmethod
    def pipe(cls, nlp):
        cls.term_pipe(nlp, delete_patterns="in")
        cls.bad_length_pipe(nlp)
        cls.compound_length_pipe(nlp, allow_no_key=True)
        cls.range_length_pipe(nlp, allow_no_key=True)
        cls.tic_pipe(nlp, allow_no_key=True)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)


@registry.misc("total_length_match")
def total_length_match(ent):
    return TotalLength.length_match(ent)


@registry.misc("total_length_compound_match")
def total_length_compound_match(ent):
    return TotalLength.compound_match(ent)


@registry.misc("total_length_tic_match")
def total_length_tic_match(ent):
    return TotalLength.tic_match(ent)


@registry.misc("total_length_range_match")
def total_length_range_match(ent):
    return TotalLength.range_match(ent)


@registry.misc("total_length_bad_match")
def total_length_bad_match(ent):
    return TotalLength.bad_match(ent)
