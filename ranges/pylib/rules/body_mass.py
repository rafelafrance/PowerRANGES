from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class BodyMass(Base):
    # Class vars ----------
    csv: ClassVar[Path] = Path(__file__).parent / "terms" / "body_mass_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(csv, "replace")
    # ---------------------

    mass: float = None
    units_inferred: bool = None
    is_shorthand: bool = None
    ambiguous_key: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {"bodyMassInGrams": self.mass}
        if self.units_inferred:
            value |= {"bodyMassUnitsInferred": True}
        if self.is_shorthand:
            value |= {"bodyMassShorthand": True}
        if self.ambiguous_key:
            value |= {"bodyMassAmbiguousKey": True}
        return dwc.add_dyn()

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="body_mass_terms", path=cls.csv)

        add.trait_pipe(
            nlp,
            name="body_mass_patterns",
            compiler=cls.body_mass_patterns(),
            overwrite=["metric_length", "imperial_length"],
        )

        add.cleanup_pipe(nlp, name="body_mass_cleanup")

    @classmethod
    def body_mass_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
        }
        return [
            Compiler(
                label="body_mass",
                keep="body_mass",
                on_match="body_mass_match",
                decoder=decoder,
                patterns=[],
            ),
        ]

    @classmethod
    def body_mass_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("body_mass_match")
def body_mass_match(ent):
    return BodyMass.body_mass_match(ent)
