from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class PregnancyState(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "pregnancy_state_terms.csv",
    ]
    nots: ClassVar[list[str]] = ["none", "post", "recent"]
    not_preg: ClassVar[list[str]] = [*nots, "not_pregnant"]
    # ---------------------

    state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(pregnancyState=self.state)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="pregnancy_state_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ############################################
        add.trait_pipe(
            nlp,
            name="pregnancy_state_patterns",
            compiler=cls.pregnancy_state_patterns(),
        )
        add.cleanup_pipe(nlp, name="pregnancy_state_cleanup")

    @classmethod
    def pregnancy_state_patterns(cls):
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
                keep="pregnancy_state",
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
    def pregnancy_state_match(cls, ent):
        state = "pregnant"
        if next((e for e in ent.ents if e.label_ in cls.not_preg), None):
            state = "not pregnant"
        return cls.from_ent(ent, state=state)


@registry.misc("pregnancy_state_match")
def pregnancy_state_match(ent):
    return PregnancyState.pregnancy_state_match(ent)
