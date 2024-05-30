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

    @property
    def all_traits(self):
        traits = []
        for trait_list in self.traits.values():
            traits += [t for t in trait_list if t]
        return sorted(traits, key=lambda t: t._trait)


class Occurrences:
    def __init__(
        self,
        *,
        path: Path,
        id_field: str,
        info_fields: list[str],
        parse_fields: list[str],
        summary_field: str,
        sample: int,
    ):
        self.nlp = pipeline.build()
        self.path = path
        self.id_field = id_field
        self.info_fields = info_fields
        self.parse_fields = parse_fields
        self.summary_field = summary_field
        self.sample = sample
        self.occurrences = self.read_occurrences()

    def read_occurrences(self) -> list[Occurrence]:
        csv.field_size_limit(10_000_000)
        with self.path.open() as in_tsv:
            reader = csv.DictReader(in_tsv, delimiter="\t")
            rows = [
                Occurrence(
                    occurrence_id=row[self.id_field],
                    info_fields={k: row[k] for k in self.info_fields},
                    parse_fields={k: row[k] for k in self.parse_fields},
                )
                for row in reader
            ]
        return rows

    def parse(self):
        for occur in tqdm(self.occurrences, desc="Parse"):
            for name, text in occur.parse_fields.items():
                if text:
                    doc = self.nlp(text)
                    occur.traits[name] = [e._.trait for e in doc.ents if e._.trait]
