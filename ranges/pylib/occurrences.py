import csv
from dataclasses import dataclass, field
from pathlib import Path

from tqdm import tqdm
from traiter.pylib.rules.base import Base

from ranges.pylib import pipeline


@dataclass
class Occurrence:
    occurrence_id: str
    info_fields: dict[str, str] = field(default_factory=dict)
    parse_fields: dict[str, str] = field(default_factory=dict)
    traits: dict[str, list[Base]] = field(default_factory=dict)


class Occurrences:
    def __init__(
        self,
        path: Path,
        id_field: str,
        parse_fields: list[str],
        info_fields: list[str],
    ):
        self.nlp = pipeline.build()
        self.occurrences = self.read_occurrences(
            path, id_field, parse_fields, info_fields
        )

    @staticmethod
    def read_occurrences(
        path: Path,
        id_field: str,
        parse_fields: list[str],
        info_fields: list[str],
    ) -> list[Occurrence]:
        occurrences = []
        with path.open() as in_tsv:
            reader = csv.DictReader(in_tsv, delimiter="\t")

            for row in reader:
                occur = Occurrence(occurrence_id=row[id_field])
                occur.info_fields = {k: row[k] for k in info_fields}
                occur.parse_fields = {k: row[k] for k in parse_fields}
                occurrences.append(occur)

        return occurrences

    def parse(self):
        for occur in tqdm(self.occurrences, desc="Parse"):
            for name, text in occur.parse_fields.items():
                if text:
                    doc = self.nlp(text)
                    occur.traits[name] = [e._.trait for e in doc.ents]
