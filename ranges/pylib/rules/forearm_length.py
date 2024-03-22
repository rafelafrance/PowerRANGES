from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import BaseLength


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
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    @classmethod
    def pipe(cls, nlp):
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)


@registry.misc("forearm_length_match")
def forearm_length_match(ent):
    return ForearmLength.length_match(ent)


@registry.misc("forearm_length_range_match")
def forearm_length_range_match(ent):
    return ForearmLength.range_match(ent)


@registry.misc("forearm_length_tic_match")
def forearm_length_tic_match(ent):
    return ForearmLength.tic_match(ent)
