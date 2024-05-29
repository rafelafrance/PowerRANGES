from pathlib import Path

from ranges.pylib.occurrences import Occurrences


class CsvWriter:
    def __init__(self, csv_file: Path):
        self.csv_file = csv_file

    def write(self, occurrences: Occurrences) -> None:
        ...
