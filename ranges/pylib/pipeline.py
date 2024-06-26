import spacy
from traiter.pylib.pipes import extensions
from traiter.pylib.rules.date_ import Date
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.number import Number
from traiter.pylib.rules.uuid import Uuid

from ranges.pylib import tokenizer
from ranges.pylib.rules import delete
from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.ear_length import EarLength
from ranges.pylib.rules.embryo import Embryo
from ranges.pylib.rules.female_state_shorthand import FemaleStateShorthand
from ranges.pylib.rules.forearm_length import ForearmLength
from ranges.pylib.rules.gonad import Gonad
from ranges.pylib.rules.hind_foot_length import HindFootLength
from ranges.pylib.rules.lactation_state import LactationState
from ranges.pylib.rules.length_shorthand import LengthShorthand
from ranges.pylib.rules.life_stage import LifeStage
from ranges.pylib.rules.mammary import Mammary
from ranges.pylib.rules.nipple import Nipple
from ranges.pylib.rules.ovary import Ovary
from ranges.pylib.rules.placenta_scar_count import PlacentalScarCount
from ranges.pylib.rules.pregnancy_state import PregnancyState
from ranges.pylib.rules.sex import Sex
from ranges.pylib.rules.tail_length import TailLength
from ranges.pylib.rules.testicle import Testicle
from ranges.pylib.rules.total_length import TotalLength
from ranges.pylib.rules.tragus_length import TragusLength
from ranges.pylib.rules.vagina_state import VaginaState


def build():
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

    delete.pipe(nlp)

    return nlp
