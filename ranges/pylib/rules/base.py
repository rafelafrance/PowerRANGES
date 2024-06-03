from dataclasses import dataclass
from typing import Any

from spacy.language import Language
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.rules.base import Base as TraiterBase


@dataclass(eq=False)
class Base(TraiterBase):
    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    def to_dwc(self, dwc) -> DarwinCore:
        raise NotImplementedError

    def labeled(self) -> dict[str, dict[str, Any]]:
        raise NotImplementedError
