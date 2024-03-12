from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import BaseLength


@dataclass(eq=False)
class EarLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "ear"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "ear_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.term_data(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    measured_from: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        super().to_dwc(dwc)

        if self.measured_from:
            dwc.add_dyn({"earLengthMeasuredFrom": self.measured_from})

        return dwc

    @classmethod
    def pipe(cls, nlp):
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def not_ear_length_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("ear_length_match")
def ear_length_match(ent):
    return EarLength.match(ent)


@registry.misc("ear_length_range_match")
def length_range_match(ent):
    return EarLength.range_match(ent)


@registry.misc("not_ear_length_match")
def not_ear_length_match(ent):
    return EarLength.not_ear_length_match(ent)
