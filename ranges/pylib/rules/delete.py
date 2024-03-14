from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from ranges.pylib import trait_util as tu


def pipe(nlp: Language):
    config = {
        "delete": """ number date elevation lat_long uuid """.split(),
    }
    add.custom_pipe(nlp, "delete", config=config)


@Language.factory("delete")
class Delete:
    def __init__(
        self,
        nlp: Language,
        name: str,
        delete: list[str],
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete or ent.label_ in self.delete:
                tu.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
