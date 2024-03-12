import spacy
from traiter.pylib.pipes import extensions
from traiter.pylib.rules.date_ import Date

from ranges.pylib import tokenizer
from ranges.pylib.rules import delete
from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.ear_length import EarLength
from ranges.pylib.rules.forearm_length import ForearmLength
from ranges.pylib.rules.hind_foot_length import HindFootLength
from ranges.pylib.rules.number import Number
from ranges.pylib.rules.shorthand import Shorthand
from ranges.pylib.rules.total_length import TotalLength
from ranges.pylib.rules.uuid import Uuid


def build():
    extensions.add_extensions()
    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup(nlp)

    Uuid.pipe(nlp)
    Date.pipe(nlp)

    Number.pipe(nlp)
    Shorthand.pipe(nlp)

    Number.pipe(nlp)
    BodyMass.pipe(nlp)

    EarLength.pipe(nlp)
    ForearmLength.pipe(nlp)
    HindFootLength.pipe(nlp)

    TotalLength.pipe(nlp)

    delete.pipe(nlp)

    return nlp
