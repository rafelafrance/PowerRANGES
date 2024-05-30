from collections import defaultdict
from itertools import groupby
from pathlib import Path

import pandas as pd
from traiter.pylib.darwin_core import DarwinCore

from ranges.pylib.occurrences import Occurrences


class CsvWriter:
    def __init__(self, csv_file: Path):
        self.csv_file = csv_file

    @staticmethod
    def count_fields(occurrences: Occurrences) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for occur in occurrences.occurrences:
            for key, group in groupby(occur.all_traits, key=lambda t: t._trait):
                counts[key] = max(counts[key], len(list(group)))
        return counts

    def write(self, occurrences: Occurrences) -> None:
        counts = self.count_fields(occurrences)

        data = []
        for occur in occurrences.occurrences:
            row = {occurrences.id_field: occur.occurrence_id}
            row |= {k: occur.info_fields[k] for k in occurrences.info_fields}
            row |= {k: occur.parse_fields[k] for k in occurrences.parse_fields}
            for _, group in groupby(occur.all_traits, key=lambda t: t._trait):
                for i, trait in enumerate(group, 1):
                    suffix = f"_#{i}" if counts[trait._trait] > 1 else ""

                    dwc = DarwinCore()
                    dwc = trait.to_dwc(dwc).flatten()

                    for header, value in dwc.items():
                        row[header + suffix] = value

            data.append(row)

        df = pd.DataFrame(data)
        df.to_csv(self.csv_file, index=False)
