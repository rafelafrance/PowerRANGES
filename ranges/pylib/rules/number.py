from dataclasses import dataclass

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base

FLOAT_RE: str = r"\d{1,4}(\.\d{,3})?"
FLOAT3_RE: str = r"\d{3}(\.\d{,3})?"
INT_RE: str = r"\d{1,4}"
FRACT_RE: str = r"\.\d{1,3}"

# This pipe is used multiple times
NUMBER_COUNT = 0  # Used to rename the Number pipe


@dataclass(eq=False)
class Number(Base):
    number: float = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn()

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        global NUMBER_COUNT
        NUMBER_COUNT += 1
        add.trait_pipe(
            nlp, name=f"number_{NUMBER_COUNT}", compiler=cls.number_patterns()
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def number_patterns(cls):
        decoder = {
            ",": {"TEXT": {"IN": t_const.COMMA}},
            "99.0": {"LOWER": {"REGEX": f"^{FLOAT_RE}+$"}},
            "999.0": {"LOWER": {"REGEX": f"^{FLOAT3_RE}+$"}},
            "99": {"LOWER": {"REGEX": f"^{INT_RE}+$"}},
            ".99": {"LOWER": {"REGEX": f"^{FRACT_RE}+$"}},
        }
        return [
            Compiler(
                label="number",
                keep="number",
                on_match="number_match",
                decoder=decoder,
                patterns=[
                    " 99.0 ",
                    " 99 , 999.0 ",
                    " .99 ",
                ],
            ),
        ]

    @classmethod
    def number_match(cls, ent):
        number = t_util.to_positive_float(ent.text)
        trait = cls.from_ent(ent, number=number)
        ent[0]._.trait = trait
        ent[0]._.flag = "number"
        return trait


@registry.misc("number_match")
def number_match(ent):
    return Number.number_match(ent)
