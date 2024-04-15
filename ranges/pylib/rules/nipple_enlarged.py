from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class NippleEnlarged(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "nipple_terms.csv",
        Path(__file__).parent / "terms" / "nipple_enlarged_terms.csv",
    ]
    # ---------------------

    enlarged: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(nippleEnlarged=self.enlarged)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="nipple_enlarged_terms", path=cls.csvs)

        add.cleanup_pipe(nlp, name="nipple_enlarged_cleanup")

    @classmethod
    def nipple_enlarged_patterns(cls):
        return [
            Compiler(
                label="nipple_enlarged",
                keep="nipple_enlarged",
                on_match="nipple_enlarged_match",
                decoder={},
                patterns=[],
            ),
        ]

    @classmethod
    def nipple_enlarged_match(cls, ent):
        data = {}
        return cls.from_ent(ent, **data)


@registry.misc("nipple_enlarged_match")
def nipple_enlarged_match(ent):
    return NippleEnlarged.nipple_enlarged_match(ent)
