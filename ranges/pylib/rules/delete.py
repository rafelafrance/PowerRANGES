import os

from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from ranges.pylib import trait_util as tu


def pipe(nlp: Language):
    config = {
        "delete": """ number """.split(),
    }

    try:
        use_mock_data = int(os.getenv("MOCK_DATA"))
    except (TypeError, ValueError):
        use_mock_data = 0

    if not use_mock_data:
        config["delete"].append("uuid")

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
        self.delete = delete if delete else []  # List of traits to delete

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete or ent.label_ in self.delete:
                tu.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
