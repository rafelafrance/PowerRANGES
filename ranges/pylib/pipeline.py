import spacy
from traiter.pylib.pipes import extensions, tokenizer
from traiter.pylib.rules.date_ import Date

from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.shorthand import Shorthand
from ranges.pylib.rules.uuid import Uuid


def build():
    extensions.add_extensions()
    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)
    # Always break tokens on these characters
    tokenizer.append_infix_regex(nlp, r""" = - \( \) \[ \] : " """.split())

    Uuid.pipe(nlp)
    Date.pipe(nlp)

    Shorthand.pipe(nlp)

    BodyMass.pipe(nlp)

    return nlp
