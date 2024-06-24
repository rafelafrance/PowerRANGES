from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class LactationState(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "lactation_state_terms.csv",
    ]
    lac_labels: ClassVar[list[str]] = ["lac", "not_lac", "post", "not"]
    # ---------------------

    state: str = None

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {"lactation_state": {"lactation_state": self.state}}

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(lactationState=self.state)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="lactation_state_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="lactation_state_patterns",
            compiler=cls.lactation_state_patterns(),
        )
        # add.debug_tokens(nlp)  # ############################################
        add.cleanup_pipe(nlp, name="lactation_state_cleanup")

    @classmethod
    def lactation_state_patterns(cls):
        decoder = {
            "lac": {"ENT_TYPE": "lac"},
            "not": {"ENT_TYPE": {"IN": ["not", "post"]}},
            "not_lac": {"ENT_TYPE": "not_lac"},
            "-": {"LOWER": {"IN": t_const.DASH}, "OP": "?"},
        }
        return [
            Compiler(
                label="lactation_state",
                keep="lactation_state",
                on_match="lactating_match",
                decoder=decoder,
                patterns=[
                    " lac ",
                ],
            ),
            Compiler(
                label="not_lactating_state",
                keep="not_lactating_state",
                on_match="not_lactating_match",
                decoder=decoder,
                patterns=[
                    " lac   not ",
                    " not - lac ",
                    " not_lac ",
                ],
            ),
        ]

    @classmethod
    def lactating_match(cls, ent):
        return cls.from_ent(ent, state="lactating")

    @classmethod
    def not_lactating_match(cls, ent):
        ent._.relabel = "lactation_state"
        return cls.from_ent(ent, state="not lactating")


@registry.misc("lactating_match")
def lactating_match(ent):
    return LactationState.lactating_match(ent)


@registry.misc("not_lactating_match")
def not_lactating_match(ent):
    return LactationState.not_lactating_match(ent)
