import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ranges.pylib.rules.base import Base
from ranges.pylib.rules.sex import Sex

OVERWRITE = {
    "sex": Sex,
}


@dataclass
class SummaryCounts:
    total: int = 0
    with_traits: int | str = 0


@dataclass
class Occurrence:
    occurrence_id: str
    source: str
    info_fields: dict[str, str] = field(default_factory=dict)
    parse_fields: dict[str, str] = field(default_factory=dict)
    overwrite_fields: dict[str, list[Base]] = field(default_factory=dict)
    traits: dict[str, list[Base]] = field(default_factory=dict)
    _all_traits: list[str, dict[str, Any]] = None

    @property
    def has_traits(self) -> bool:
        return any(len(v) for v in self.traits.values())

    @property
    def has_parse(self) -> bool:
        return any(v for val in self.parse_fields.values() if (v := val.strip()))

    @property
    def all_traits(self) -> list[str, dict[str, Any]]:
        if self._all_traits is None:
            traits = {}
            for trait_list in self.traits.values():
                for trait in trait_list:
                    traits |= trait.labeled()

            self._all_traits = sorted(traits.items())
        return self._all_traits


def read_occurrences(
    input_tsv: Path,
    *,
    id_field: str,
    info_fields: list[str],
    parse_fields: list[str],
    overwrite_fields: list[str],
) -> list[Occurrence]:
    csv.field_size_limit(10_000_000)
    source = input_tsv.name
    with input_tsv.open() as in_tsv:
        reader = csv.DictReader(in_tsv, delimiter="\t")
        rows = [
            Occurrence(
                occurrence_id=row[id_field],
                source=source,
                info_fields={k: row[k] for k in info_fields},
                parse_fields={k: row[k] for k in parse_fields},
                overwrite_fields={k: row[k] for k in overwrite_fields},
            )
            for row in reader
        ]
    return rows


def parse_occurrences(occurrences: list[Occurrence], nlp):
    for occur in occurrences:
        overwritten = set()
        for overwrite_field, text in occur.overwrite_fields.items():
            if text:
                overwritten.add(overwrite_field)
                data = {
                    "start": 0,
                    "end": len(text),
                    "_trait": overwrite_field,
                    "_text": text,
                    overwrite_field: text,
                }
                trait = OVERWRITE[overwrite_field](**data)
                occur.traits[overwrite_field] = [trait]

        for parse_field, text in occur.parse_fields.items():
            if text:
                doc = nlp(text)
                occur.traits[parse_field] = [
                    e._.trait
                    for e in doc.ents
                    if e._.trait and e._.trait._trait not in overwritten
                ]
