import csv
from dataclasses import dataclass, field
from pathlib import Path

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
    source: str
    id_field: tuple[str, str]
    info_fields: dict[str, str] = field(default_factory=dict)
    parse_fields: dict[str, str] = field(default_factory=dict)
    overwrite_fields: dict[str, list[Base]] = field(default_factory=dict)
    traits: dict[str, list[Base]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        value = {
            self.id_field[0]: self.id_field[1],
            "source": self.source,
        }
        value |= {"info_fields": self.info_fields}
        value |= {"parse_fields": self.parse_fields}
        traits = []
        for source_field, trait_list in self.traits.items():
            for trait in trait_list:
                as_dict = trait.labeled()
                as_dict |= {
                    "_start": trait.start,
                    "_end": trait.end,
                    "_trait": trait._trait,
                    "_field": source_field,
                }
                traits.append(as_dict)
        value |= {"traits": traits}
        return value


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
                id_field=(id_field, row[id_field]),
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
