from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Gonad(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "gonad_terms.csv",
    ]
    # ---------------------

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}
        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="gonad_terms", path=cls.csvs)

    @classmethod
    def gonad_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def gonad_size_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("gonad_description_match")
def gonad_description_match(ent):
    return Gonad.gonad_description_match(ent)


@registry.misc("gonad_size_match")
def gonad_size_match(ent):
    return Gonad.gonad_size_match(ent)
