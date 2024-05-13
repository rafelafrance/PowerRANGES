from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Testicle(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "testicle_terms.csv",
    ]
    # ---------------------

    description: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(scrotalState=self.description)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="testicle_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="testicle_description_patterns",
            compiler=cls.testicle_description_patterns(),
        )

        add.trait_pipe(
            nlp,
            name="testicle_state_patterns",
            compiler=cls.testicle_state_patterns(),
        )

        # add.debug_tokens(nlp)  # ############################################
        add.cleanup_pipe(nlp, name="testicle_description_cleanup")

    @classmethod
    def testicle_description_patterns(cls):
        return [
            Compiler(
                label="description",
                on_match="testicle_description_match",
                decoder={
                    "abdominal": {"ENT_TYPE": "abdominal", "OP": "+"},
                    "descended": {"ENT_TYPE": "descended", "OP": "+"},
                    "fully": {"ENT_TYPE": "fully", "OP": "+"},
                    "non": {"ENT_TYPE": "non", "OP": "+"},
                    "partially": {"ENT_TYPE": "partially", "OP": "+"},
                    "size": {"ENT_TYPE": "size", "OP": "+"},
                },
                patterns=[
                    " non fully descended ",
                    " abdominal non descended ",
                    " abdominal descended ",
                    " non descended ",
                    " fully descended ",
                    " partially descended ",
                    " size non descended ",
                    " size descended ",
                    " descended ",
                ],
            ),
        ]

    @classmethod
    def testicle_state_patterns(cls):
        return [
            Compiler(
                label="testicle",
                keep="testicle",
                on_match="testicle_state_match",
                decoder={
                    "descr": {"ENT_TYPE": "description", "OP": "+"},
                    "non": {"ENT_TYPE": "non", "OP": "+"},
                    "testes": {"ENT_TYPE": "testes", "OP": "+"},
                },
                patterns=[
                    " non testes ",
                    "     testes descr ",
                ],
            ),
        ]

    @classmethod
    def testicle_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def testicle_state_match(cls, ent):
        data = {}
        descr = [e.text.lower() for e in ent.ents if e.label_ == "description"]
        data["description"] = descr[0] if descr else ent.text.lower()
        return cls.from_ent(ent, **data)


@registry.misc("testicle_description_match")
def testicle_description_match(ent):
    return Testicle.testicle_description_match(ent)


@registry.misc("testicle_state_match")
def testicle_state_match(ent):
    return Testicle.testicle_state_match(ent)
