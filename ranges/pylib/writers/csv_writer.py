import re
import traceback
from collections import defaultdict
from itertools import groupby
from pathlib import Path

import pandas as pd

from ranges.pylib import occurrence, pipeline


def process_occurrences(
    tsv_file: Path,
    csv_dir: Path,
    id_field: str,
    info_fields=None,
    parse_fields=None,
    overwrite_fields=None,
    *,
    debug: bool = False,
) -> str:
    info_fields = info_fields if info_fields else []
    parse_fields = parse_fields if parse_fields else []
    overwrite_fields = overwrite_fields if overwrite_fields else []

    try:
        occurrences = occurrence.read_occurrences(
            tsv_file,
            id_field=id_field,
            info_fields=info_fields,
            parse_fields=parse_fields,
            overwrite_fields=overwrite_fields,
        )

        nlp = pipeline.build()
        occurrence.parse_occurrences(occurrences, nlp)

        csv_file = csv_dir / f"{tsv_file.stem}.csv"
        write_occurrences(occurrences, csv_file, id_field, info_fields, parse_fields)
    except:  # noqa: E722
        if debug:
            print(traceback.format_exc())
        return tsv_file.stem

    return ""


def count_fields(occurrences: list[occurrence.Occurrence]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for occur in occurrences:
        for key, group in groupby(occur.all_traits, lambda t: t[0]):
            counts[key] = max(counts[key], len(list(group)))
    return counts


def write_occurrences(
    occurrences: list[occurrence.Occurrence],
    csv_file: Path,
    id_field: str,
    info_fields,
    parse_fields,
) -> None:
    counts = count_fields(occurrences)

    data = []
    trait_cols = set()
    for occur in occurrences:
        row = {id_field: occur.occurrence_id, "source": occur.source}
        row |= {k: occur.info_fields[k] for k in info_fields}
        row |= {k: occur.parse_fields[k] for k in parse_fields}
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
        id_field,
        "source",
        *info_fields,
        *parse_fields,
        *[t[2] for t in sorted(trait_cols)],
    ]

    df = pd.DataFrame(data)
    df = df.loc[:, columns]
    df.to_csv(csv_file, index=False)
