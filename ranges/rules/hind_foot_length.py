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
class HindFootLength(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "hind_foot"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_tic_terms.csv",
        Path(__file__).parent / "terms" / "hind_foot_length_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    includes_keys: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "includes")
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    includes: str | None = None

    def for_csv(self) -> dict[str, Any]:
        value = {}

        value["hind_foot_length"] = self.length

        if self.includes:
            value["hind_foot_length_includes"] = self.includes

        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        cls.term_pipe(nlp)
        cls.range_length_pipe(nlp)
        cls.tic_pipe(nlp)
        cls.length_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def get_includes(cls, ent: Span, trait: "HindFootLength") -> None:
        keys = [e for e in ent.ents if e.label_ in cls.keys]
        for key in keys:
            if value := cls.includes_keys.get(key.text.lower()):
                trait.includes = value

    @classmethod
    def hind_foot_length_match(cls, ent: Span) -> "HindFootLength":
        trait = cls.to_obj(ent, DictFunc.LENGTH)
        cls.get_includes(ent, trait)
        return trait

    @classmethod
    def hind_foot_length_range_match(cls, ent: Span) -> "HindFootLength":
        trait = cls.to_obj(ent, DictFunc.RANGE)
        cls.get_includes(ent, trait)
        return trait

    @classmethod
    def hind_foot_length_tic_match(cls, ent: Span) -> "HindFootLength":
        trait = cls.to_obj(ent, DictFunc.TIC)
        cls.get_includes(ent, trait)
        return trait

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "HindFootLength":
        base = cls.class_dict(ent, dict_func)
        return cls(**base)


@registry.misc("hind_foot_length_match")
def hind_foot_length_match(ent: Span) -> HindFootLength:
    return HindFootLength.hind_foot_length_match(ent)


@registry.misc("hind_foot_length_range_match")
def hind_foot_length_range_match(ent: Span) -> HindFootLength:
    return HindFootLength.hind_foot_length_range_match(ent)


@registry.misc("hind_foot_length_tic_match")
def hind_foot_length_tic_match(ent: Span) -> HindFootLength:
    return HindFootLength.hind_foot_length_tic_match(ent)
