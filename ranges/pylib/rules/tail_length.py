from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import BaseLength


@dataclass(eq=False)
class TailLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "tail"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "tail_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    def labeled(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        value["tail_length"] = {"tail_length": self.length}

        if self.units_inferred:
            value["tail_length"] |= {"tail_length_units_inferred": True}

        if self.ambiguous:
            value["tail_length"] |= {"tail_length_ambiguous": True}

        if self.estimated:
            value["tail_length"] |= {"tail_length_estimated": True}

        return value

    @classmethod
    def pipe(cls, nlp):
        cls.term_pipe(nlp)
        cls.bad_length_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)


@registry.misc("tail_length_match")
def tail_length_match(ent):
    return TailLength.length_match(ent)


@registry.misc("tail_length_range_match")
def tail_length_range_match(ent):
    return TailLength.range_match(ent)


@registry.misc("tail_length_tic_match")
def tail_length_tic_match(ent):
    return TailLength.tic_match(ent)


@registry.misc("tail_length_bad_match")
def tail_length_bad_match(ent):
    return TailLength.bad_match(ent)
