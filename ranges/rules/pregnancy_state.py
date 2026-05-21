from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from ranges.rules.base import Base


@dataclass(eq=False)
class PregnancyState(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "pregnancy_state_terms.csv",
    ]
    nots: ClassVar[list[str]] = ["none", "post", "recent"]
    not_preg: ClassVar[list[str]] = [*nots, "not_pregnant"]
    # ---------------------

    pregnancy: bool | None = None

    def for_csv(self) -> dict[str, Any]:
        return {"pregnancy_state": self.pregnancy}

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="pregnancy_state_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="pregnancy_state_patterns",
            compiler=cls.pregnancy_state_patterns(),
        )
        add.cleanup_pipe(nlp, name="pregnancy_state_cleanup")

    @classmethod
    def pregnancy_state_patterns(cls) -> list[Compiler]:
        decoder = {
            "not": {"ENT_TYPE": {"IN": cls.nots}, "OP": "+"},
            "not_pregnant": {"ENT_TYPE": "not_pregnant", "OP": "+"},
            "pregnant": {"ENT_TYPE": "pregnant", "OP": "+"},
            "prob": {"ENT_TYPE": "probably", "OP": "+"},
            "stage": {"ENT_TYPE": "stage", "OP": "+"},
        }
        return [
            Compiler(
                label="pregnancy_state",
                on_match="pregnancy_state_match",
                decoder=decoder,
                patterns=[
                    "     pregnant ",
                    "     pregnant not ",
                    " not pregnant ",
                    " not_pregnant ",
                ],
            ),
        ]

    @classmethod
    def pregnancy_state_match(cls, ent: Span) -> "PregnancyState":
        state = True
        if next((e for e in ent.ents if e.label_ in cls.not_preg), None):
            state = False
        return cls.from_ent(ent, pregnancy=state)


@registry.misc("pregnancy_state_match")
def pregnancy_state_match(ent: Span) -> PregnancyState:
    return PregnancyState.pregnancy_state_match(ent)
