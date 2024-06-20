import re
from collections import defaultdict
from itertools import groupby
from pathlib import Path

import pandas as pd

from ranges.pylib.occurrences import Occurrences


class CsvWriter:
    def __init__(self, csv_file: Path):
        self.csv_file = csv_file

    @staticmethod
    def count_fields(occurrences: Occurrences) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for occur in occurrences.occurrences:
            for key, group in groupby(occur.all_traits, lambda t: t[0]):
                counts[key] = max(counts[key], len(list(group)))
        return counts

    def write(self, occurrences: Occurrences) -> None:
        counts = self.count_fields(occurrences)

        data = []
        trait_cols = set()
        for occur in occurrences.occurrences:
            row = {occurrences.id_field: occur.occurrence_id}
            row |= {k: occur.info_fields[k] for k in occurrences.info_fields}
            row |= {k: occur.parse_fields[k] for k in occurrences.parse_fields}
            for key, group in groupby(occur.all_traits, key=lambda t: t[0]):
                for i, fields in enumerate(group, 1):
                    suffix = f"_{i}" if counts[key] > 1 else ""

                    for header, value in fields[1].items():
                        name = header + suffix
                        name = re.sub(r"\W", "_", name)
                        row[name] = value
                        trait_cols.add((key, i, name))

            data.append(row)

        trait_cols = sorted(trait_cols)
        columns = [
            occurrences.id_field,
            *occurrences.info_fields,
            *occurrences.parse_fields,
            *[t[2] for t in sorted(trait_cols)],
        ]

        df = pd.DataFrame(data)
        df = df.loc[:, columns]
        df.to_csv(self.csv_file, index=False)
