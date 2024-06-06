import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tqdm import tqdm

from ranges.pylib import pipeline
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


class Occurrences:
    def __init__(
        self,
        *,
        path: Path,
        id_field: str,
        info_fields: list[str],
        parse_fields: list[str],
        overwrite_fields: list[str],
        summary_field: str,
        sample: int,
    ):
        self.nlp = pipeline.build()
        self.path = path
        self.id_field = id_field
        self.info_fields = info_fields
        self.parse_fields = parse_fields
        self.summary_field = summary_field
        self.overwrite_fields = overwrite_fields
        self.sample = sample
        self.occurrences = self.read_occurrences()
        self._summary_by_field = None
        self._summary_by_trait = None

    def read_occurrences(self) -> list[Occurrence]:
        csv.field_size_limit(10_000_000)
        with self.path.open() as in_tsv:
            reader = csv.DictReader(in_tsv, delimiter="\t")
            rows = [
                Occurrence(
                    occurrence_id=row[self.id_field],
                    info_fields={k: row[k] for k in self.info_fields},
                    parse_fields={k: row[k] for k in self.parse_fields},
                    overwrite_fields={k: row[k] for k in self.overwrite_fields},
                )
                for row in reader
            ]
        return rows

    def parse(self):
        for occur in tqdm(self.occurrences, desc="Parse"):
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
                    doc = self.nlp(text)
                    occur.traits[parse_field] = [
                        e._.trait
                        for e in doc.ents
                        if e._.trait and e._.trait._trait not in overwritten
                    ]

    def summary_by_field(self) -> dict[str, SummaryCounts]:
        if not self.summary_field:
            return {}

        if self._summary_by_field is None:
            counts = defaultdict(lambda: SummaryCounts())

            for occur in self.occurrences:
                name = occur.info_fields.get(self.summary_field, "").strip()
                counts[name].total += 1
                counts[name].with_traits += 1 if occur.has_traits else 0

            counts = dict(sorted(counts.items()))
            counts["Total"] = SummaryCounts(
                total=len(self.occurrences),
                with_traits=sum(c.with_traits for c in counts.values()),
            )
            self._summary_by_field = counts

        return self._summary_by_field

    def summary_by_trait(self) -> dict[str, int]:
        if self._summary_by_trait is None:
            counts = defaultdict(int)

            for occur in self.occurrences:
                for trait in occur.all_traits:
                    counts[trait[0]] += 1

            counts = dict(sorted(counts.items()))
            counts["Total"] = sum(c for c in counts.values())
            self._summary_by_trait = counts

        return self._summary_by_trait
