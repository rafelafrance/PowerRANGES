from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

SKIP = """ start end _trait _text """.split()


def write_csv(
    csv_file: Path,
    occurrences: list[dict[str, Any]],
    id_field: str,
    info_fields=None,
    parse_fields=None,
) -> None:
    info_fields = info_fields if info_fields else []
    parse_fields = parse_fields if parse_fields else []

    counts = count_fields(occurrences)

    data = []
    trait_cols = set()

    for occur in occurrences:
        row = {id_field: occur["id_field"], "source": occur["source"]}
        row |= {k: occur["info_fields"][k] for k in info_fields}
        row |= {k: occur["parse_fields"][k] for k in parse_fields}

        for trait_list in occur["traits"].values():
            for i, trait in enumerate(trait_list):
                suffix = f"_{i}" if counts[trait["_trait"]] > 1 else ""

                for header, value in trait.items():
                    if header in SKIP:
                        continue
                    name = header + suffix
                    row[name] = value
                    trait_cols.add((trait["_trait"], i, name))

            data.append(row)

    # Sort columns
    trait_cols = sorted(trait_cols)
    columns = [
        id_field,
        "source",
        *info_fields,
        *parse_fields,
        *[t[2] for t in sorted(trait_cols)],
    ]
    df = pd.DataFrame(data)
    df = df.loc[:, columns]

    df.to_csv(csv_file, index=False)


def count_fields(occurrences: list[dict[str, Any]]) -> dict[str, int]:
    maxes: dict[str, int] = defaultdict(int)

    for occur in occurrences:
        # Check how many times a trait is recorded in an occurrence
        counts = defaultdict(int)
        if occur["traits"]:
            for traits in occur["traits"].values():
                for trait in traits:
                    counts[trait["_trait"]] += 1

        # Check if the occurrence is the new max
        for key, count in counts.items():
            maxes[key] = max(maxes[key], count)

    return maxes
