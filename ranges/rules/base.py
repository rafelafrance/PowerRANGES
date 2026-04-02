from dataclasses import dataclass
from typing import Any

from spacy.language import Language
from traiter.pylib.darwin_core import DarwinCore
from traiter.rules.base_rule import BaseRule as TraiterBase


@dataclass(eq=False)
class Base(TraiterBase):
    @classmethod
    def pipe(cls, nlp: Language) -> None:
        raise NotImplementedError

    def to_dwc(self, dwc: DarwinCore) -> DarwinCore:
        raise NotImplementedError

    def as_dict(self) -> dict[str, dict[str, Any]]:
        raise NotImplementedError
