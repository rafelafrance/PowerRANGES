from dataclasses import dataclass

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class FemaleStateShorthand(Base):
    vagina_state: str = None
    nipple_state: str = None
    lactation_state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}

        if self.vagina_state:
            value |= {"vaginaState": self.vagina_state}

        if self.nipple_state:
            value |= {"nippleState": self.nipple_state}

        if self.lactation_state:
            value |= {"lactationState": self.lactation_state}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp):
        add.trait_pipe(
            nlp,
            name="shorthand_female_states_patterns",
            compiler=cls.shorthand_female_states_patterns(),
        )
        add.cleanup_pipe(nlp, name="shorthand_female_states_cleanup")

    @classmethod
    def shorthand_female_states_patterns(cls):
        decoder = {
            "triple": {"LOWER": {"REGEX": r"^[oc][smel][ln](ac)?$"}},
        }
        return [
            Compiler(
                label="shorthand_female_states",
                keep="shorthand_female_states",
                on_match="shorthand_female_states_match",
                decoder=decoder,
                patterns=[
                    " triple ",
                ],
            ),
        ]

    @classmethod
    def shorthand_female_states_match(cls, ent):
        vag, nip, lac, *_ = list(ent.text.lower())

        vag = "open" if vag == "o" else "closed"
        lac = "lactating" if lac == "l" else "not lactating"

        match nip:
            case "s":
                nip = "small"
            case "m":
                nip = "medium"
            case "e":
                nip = "enlarged"
            case "l":
                nip = "large"

        return cls.from_ent(
            ent, vagina_state=vag, nipple_state=nip, lactation_state=lac
        )


@registry.misc("shorthand_female_states_match")
def shorthand_female_states_match(ent):
    return FemaleStateShorthand.shorthand_female_states_match(ent)
