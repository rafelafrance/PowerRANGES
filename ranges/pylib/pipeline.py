import spacy
from spacy.language import Language
from traiter.pipes import extensions
from traiter.rules.date_ import Date
from traiter.rules.elevation import Elevation
from traiter.rules.lat_long import LatLong
from traiter.rules.number import Number
from traiter.rules.uuid import Uuid

from ranges.pylib import tokenizer

# from ranges.rules import delete
from ranges.rules.body_mass import BodyMass
from ranges.rules.ear_length import EarLength
from ranges.rules.embryo import Embryo
from ranges.rules.female_state_shorthand import FemaleStateShorthand
from ranges.rules.forearm_length import ForearmLength
from ranges.rules.gonad import Gonad
from ranges.rules.hind_foot_length import HindFootLength
from ranges.rules.lactation_state import LactationState
from ranges.rules.length_shorthand import LengthShorthand
from ranges.rules.life_stage import LifeStage
from ranges.rules.mammary import Mammary
from ranges.rules.nipple import Nipple
from ranges.rules.ovary import Ovary
from ranges.rules.placenta_scar_count import PlacentalScarCount
from ranges.rules.pregnancy_state import PregnancyState
from ranges.rules.sex import Sex
from ranges.rules.tail_length import TailLength
from ranges.rules.testicle import Testicle
from ranges.rules.total_length import TotalLength
from ranges.rules.tragus_length import TragusLength
from ranges.rules.vagina_state import VaginaState


def build() -> Language:
    extensions.add_extensions()
    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup(nlp)

    Uuid.pipe(nlp)
    Date.pipe(nlp)
    Elevation.pipe(nlp)
    LatLong.pipe(nlp)

    Number.pipe(nlp)

    LengthShorthand.pipe(nlp)
    Number.pipe(nlp)

    BodyMass.pipe(nlp)

    PlacentalScarCount.pipe(nlp)
    Number.pipe(nlp)

    Embryo.pipe(nlp)
    Number.pipe(nlp)

    EarLength.pipe(nlp)

    ForearmLength.pipe(nlp)

    TragusLength.pipe(nlp)

    HindFootLength.pipe(nlp)

    FemaleStateShorthand.pipe(nlp)
    Mammary.pipe(nlp)
    Nipple.pipe(nlp)
    LactationState.pipe(nlp)
    PregnancyState.pipe(nlp)

    Testicle.pipe(nlp)

    Ovary.pipe(nlp)

    Gonad.pipe(nlp)

    VaginaState.pipe(nlp)

    TailLength.pipe(nlp)
    Number.pipe(nlp)

    TotalLength.pipe(nlp)

    LifeStage.pipe(nlp)
    Sex.pipe(nlp)

    # delete.pipe(nlp)

    return nlp
