import spacy
from traiter.pylib.pipes import extensions, tokenizer

from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.uuid import Uuid


def build():
    extensions.add_extensions()
    nlp = spacy.load("en_core_web_md", exclude=["ner"])
    tokenizer.setup_tokenizer(nlp)

    Uuid.pipe(nlp)

    BodyMass.pipe(nlp)

    return nlp
