from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Scrotum(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "scrotal_state_terms.csv",
    ]
    # ---------------------

    state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(scrotalState=self.state)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="scrotal_state_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ############################################
        add.trait_pipe(
            nlp,
            name="scrotal_state_patterns",
            compiler=cls.scrotal_state_patterns(),
        )
        add.cleanup_pipe(nlp, name="scrotal_state_cleanup")

    @classmethod
    def scrotal_state_patterns(cls):
        decoder = {
            # "not": {"ENT_TYPE": {"IN": cls.nots}, "OP": "+"},
            "not_pregnant": {"ENT_TYPE": "not_pregnant", "OP": "+"},
            "pregnant": {"ENT_TYPE": "pregnant", "OP": "+"},
            "prob": {"ENT_TYPE": "probably", "OP": "+"},
            "stage": {"ENT_TYPE": "stage", "OP": "+"},
        }
        return [
            Compiler(
                label="scrotal_state",
                keep="scrotal_state",
                on_match="scrotal_state_match",
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
    def scrotal_state_match(cls, ent):
        # state = "pregnant"
        # if next((e for e in ent.ents if e.label_ in cls.not_preg), None):
        #     state = "not pregnant"
        return cls.from_ent(ent)


@registry.misc("scrotal_state_match")
def scrotal_state_match(ent):
    return Scrotum.scrotal_state_match(ent)
