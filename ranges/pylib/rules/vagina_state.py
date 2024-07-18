from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class VaginaState(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "vagina_state_terms.csv",
    ]
    states: ClassVar[list[str]] = ["open", "closed", "plugged", "swollen"]
    # ---------------------

    state: str = None

    def as_dict(self) -> dict[str, dict[str, Any]]:
        return {
            "vagina_state": {
                "vagina_state": self.state,
                "_parser": self.__class__.__name__,
            }
        }

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(vaginaState=self.state)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="vagina_state_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ############################################
        add.trait_pipe(
            nlp,
            name="vagina_state_patterns",
            compiler=cls.vagina_state_patterns(),
        )
        add.cleanup_pipe(nlp, name="vagina_state_cleanup")

    @classmethod
    def vagina_state_patterns(cls):
        decoder = {
            ",": {"IS_PUNCT": True, "OP": "?"},
            "vagina": {"ENT_TYPE": "vagina", "OP": "+"},
            "partially": {"ENT_TYPE": "partially", "OP": "*"},
            "state": {"ENT_TYPE": {"IN": cls.states}, "OP": "+"},
        }
        return [
            Compiler(
                label="vagina_state",
                keep="vagina_state",
                on_match="vagina_state_match",
                decoder=decoder,
                patterns=[
                    " vagina , partially , state ",
                    " vagina             , state ",
                    " state                      ",
                    " state  , vagina            ",
                    " state  , vagina    , state ",
                ],
            ),
        ]

    @classmethod
    def vagina_state_match(cls, ent):
        state = [e.label_ for e in ent.ents if e.label_ in cls.states]
        state = ", ".join(state)
        return cls.from_ent(ent, state=state)


@registry.misc("vagina_state_match")
def vagina_state_match(ent):
    return VaginaState.vagina_state_match(ent)
