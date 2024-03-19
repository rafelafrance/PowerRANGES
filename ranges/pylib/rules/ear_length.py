from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pipes.reject_match import RejectMatch
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

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    measured_keys: ClassVar[dict[str, str]] = term_util.look_up_table(
        csvs, "measured_from"
    )
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
        cls.bad_length_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def check_ambiguous_key(cls, trait):
        if trait.ambiguous and trait.units_inferred:
            raise RejectMatch

    @classmethod
    def get_measured_from(cls, ent, trait):
        keys = [e for e in ent.ents if e.label_ in cls.keys]
        for key in keys:
            if value := cls.measured_keys.get(key.text.lower()):
                trait.measured_from = value

    @classmethod
    def ear_length_match(cls, ent):
        trait = cls.length_match(ent)
        cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait

    @classmethod
    def ear_length_range_match(cls, ent):
        trait = cls.range_match(ent)
        cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait

    @classmethod
    def ear_length_tic_match(cls, ent):
        trait = cls.tic_match(ent)
        cls.check_ambiguous_key(trait)
        cls.get_measured_from(ent, trait)
        return trait


@registry.misc("ear_length_match")
def ear_length_match(ent):
    return EarLength.ear_length_match(ent)


@registry.misc("ear_length_range_match")
def ear_length_range_match(ent):
    return EarLength.ear_length_range_match(ent)


@registry.misc("ear_length_tic_match")
def ear_length_tic_match(ent):
    return EarLength.ear_length_tic_match(ent)


@registry.misc("ear_length_bad_match")
def ear_length_bad_match(ent):
    return EarLength.bad_match(ent)
