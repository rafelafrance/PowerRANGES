from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Testes(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "testes_state_terms.csv",
    ]
    # ---------------------

    state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(scrotalState=self.state)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="testes_state_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ############################################
        add.trait_pipe(
            nlp,
            name="testes_state_patterns",
            compiler=cls.testes_state_patterns(),
        )
        add.cleanup_pipe(nlp, name="testes_state_cleanup")

    @classmethod
    def testes_state_patterns(cls):
        decoder = {
            # "not": {"ENT_TYPE": {"IN": cls.nots}, "OP": "+"},
            "not_pregnant": {"ENT_TYPE": "not_pregnant", "OP": "+"},
            "pregnant": {"ENT_TYPE": "pregnant", "OP": "+"},
            "prob": {"ENT_TYPE": "probably", "OP": "+"},
            "stage": {"ENT_TYPE": "stage", "OP": "+"},
        }
        return [
            Compiler(
                label="testes_state",
                keep="testes_state",
                on_match="testes_state_match",
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
    def testes_state_match(cls, ent):
        # state = "pregnant"
        # if next((e for e in ent.ents if e.label_ in cls.not_preg), None):
        #     state = "not pregnant"
        return cls.from_ent(ent)


@registry.misc("testes_state_match")
def testes_state_match(ent):
    return Testes.testes_state_match(ent)
