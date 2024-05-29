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

    @property
    def has_traits(self) -> bool:
        return any(len(v) for v in self.traits.values())

    @property
    def has_parse(self) -> bool:
        return any(v for val in self.parse_fields.values() if (v := val.strip()))


class Occurrences:
    def __init__(
        self,
        *,
        path: Path,
        id_field: str,
        info_fields: list[str],
        parse_fields: list[str],
        summary_field: str,
    ):
        self.nlp = pipeline.build()
        self.path = path
        self.id_field = id_field
        self.info_fields = info_fields
        self.parse_fields = parse_fields
        self.summary_field = summary_field
        self.occurrences = self.read_occurrences()

    def read_occurrences(self) -> list[Occurrence]:
        with self.path.open() as in_tsv:
            reader = csv.DictReader(in_tsv, delimiter="\t")
            return [
                Occurrence(
                    occurrence_id=row[self.id_field],
                    info_fields={k: row[k] for k in self.info_fields},
                    parse_fields={k: row[k] for k in self.parse_fields},
                )
                for row in reader
            ]

    def parse(self):
        for occur in tqdm(self.occurrences, desc="Parse"):
            for name, text in occur.parse_fields.items():
                if text:
                    doc = self.nlp(text)
                    occur.traits[name] = [e._.trait for e in doc.ents]
