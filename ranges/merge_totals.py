#!/usr/bin/env python3

import csv
from collections import defaultdict
from pathlib import Path


def trait_totals():
    root = Path() / "data" / "totals"
    pattern = "grand_totals_scientificName?.csv"

    counts = defaultdict(int)

    for path in sorted(root.glob(pattern)):
        with path.open() as inp:
            reader = csv.DictReader(inp)
            for row in reader:
                counts[row["trait"]] += int(row["count"])

    counts = sorted(counts.items())

    path = root / "grand_total_traits.csv"
    with path.open("w") as out:
        writer = csv.writer(out)
        writer.writerow(["trait", "count"])
        for trait, count in counts:
            writer.writerow([trait, count])


def species_totals():
    root = Path() / "data" / "totals"
    pattern = "grand_totals_scientificName?.csv"

    counts = defaultdict(lambda: {"total": 0, "with traits": 0})

    for path in sorted(root.glob(pattern)):
        with path.open() as inp:
            reader = csv.DictReader(inp)
            for row in reader:
                counts[row["scientificName"]]["total"] += int(row["total"])
                counts[row["scientificName"]]["with traits"] += int(row["with traits"])

    counts = sorted(counts.items())

    path = root / "grand_total_scientificName.csv"
    with path.open("w") as out:
        writer = csv.writer(out)
        writer.writerow(["scientificName", "total", "with traits"])
        for trait, count in counts:
            writer.writerow([trait, count["total"], count["with traits"]])


if __name__ == "__main__":
    species_totals()
