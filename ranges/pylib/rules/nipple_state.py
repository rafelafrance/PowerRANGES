from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class NippleState(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "nipple_terms.csv",
        Path(__file__).parent / "terms" / "nipple_state_terms.csv",
    ]
    # ---------------------

    state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(nippleState=self.state)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="embryo_terms", path=cls.csvs)

        add.cleanup_pipe(nlp, name="nipple_state_cleanup")

    @classmethod
    def nipple_state_patterns(cls):
        return [
            Compiler(
                label="nipple_state",
                keep="nipple_state",
                on_match="nipple_state_match",
                decoder={},
                patterns=[],
            ),
        ]

    @classmethod
    def nipple_state_match(cls, ent):
        data = {}
        return cls.from_ent(ent, **data)


@registry.misc("nipple_state_match")
def nipple_state_match(ent):
    return NippleState.nipple_state_match(ent)
