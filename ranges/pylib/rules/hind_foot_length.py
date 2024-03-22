from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base_length import BaseLength


@dataclass(eq=False)
class HindFootLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "hind_foot"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "hind_foot_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    includes_keys: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "includes")
    # ---------------------

    includes: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        super().to_dwc(dwc)

        if self.includes:
            dwc.add_dyn({"hindFootLengthIncludes": self.includes})

        return dwc

    @classmethod
    def pipe(cls, nlp):
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def get_includes(cls, ent, trait):
        keys = [e for e in ent.ents if e.label_ in cls.keys]
        for key in keys:
            if value := cls.includes_keys.get(key.text.lower()):
                trait.includes = value

    @classmethod
    def hind_foot_length_match(cls, ent):
        trait = cls.length_match(ent)
        cls.get_includes(ent, trait)
        return trait

    @classmethod
    def hind_foot_length_range_match(cls, ent):
        trait = cls.range_match(ent)
        cls.get_includes(ent, trait)
        return trait

    @classmethod
    def hind_foot_length_tic_match(cls, ent):
        trait = cls.tic_match(ent)
        cls.get_includes(ent, trait)
        return trait


@registry.misc("hind_foot_length_match")
def hind_foot_length_match(ent):
    return HindFootLength.hind_foot_length_match(ent)


@registry.misc("hind_foot_length_range_match")
def hind_foot_length_range_match(ent):
    return HindFootLength.hind_foot_length_range_match(ent)


@registry.misc("hind_foot_length_tic_match")
def hind_foot_length_tic_match(ent):
    return HindFootLength.hind_foot_length_tic_match(ent)
