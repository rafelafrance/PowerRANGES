from dataclasses import dataclass
from typing import Any

from spacy.language import Language
from traiter.rules.base_rule import BaseRule as TraiterBase


@dataclass(eq=False)
class Base(TraiterBase):
    @classmethod
    def pipe(cls, nlp: Language) -> None:
        del nlp
        raise NotImplementedError

    def for_csv(self) -> dict[str, Any]:
        raise NotImplementedError
