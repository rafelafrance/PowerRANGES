from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

# from pprint import pp


def write_csv(  # noqa: C901
    csv_file: Path,
    occurrences: list[dict[str, Any]],
    id_field: str,
    info_fields=None,
    parse_fields=None,
) -> None:
    info_fields = info_fields if info_fields else []
    parse_fields = parse_fields if parse_fields else []

    data = []
    trait_cols = set()

    for occur in occurrences:
        row = {id_field: occur[id_field], "source": occur["source"]}
        row |= {k: occur["info_fields"][k] for k in info_fields}
        row |= {k: occur["parse_fields"][k] for k in parse_fields}

        grouped = defaultdict(list)
        for trait in occur["traits"]:
            grouped[trait["_trait"]].append(trait)

        filtered = defaultdict(list)
        for name, traits in grouped.items():
            for i, trait in enumerate(traits):
                if i > 0 and any(same_data_fields(trait, t) for t in filtered[name]):
                    continue
                if i > 0 and any(same_data_parsers(trait, t) for t in filtered[name]):
                    continue
                filtered[name].append(trait)

        lst = []
        for name, traits in filtered.items():
            for i, trait in enumerate(traits, 1):
                if i > len(lst):
                    lst.append({"trait_reported_order": i} | row)
                new = {k: v for k, v in trait.items() if not k.startswith("_")}
                lst[i - 1] |= new
                trait_cols |= {(name, k) for k in new}

        if not lst:
            lst.append({"trait_reported_order": 1} | row)

        data += lst

    # Sort columns
    trait_cols = sorted(trait_cols)
    columns = [
        id_field,
        "trait_reported_order",
        "source",
        *info_fields,
        *parse_fields,
        *[t[1] for t in sorted(trait_cols)],
    ]
    df = pd.DataFrame(data)
    df = df.loc[:, columns]

    df = df.set_index(id_field)
    df.to_csv(csv_file)


def same_data_fields(trait1, trait2):
    if trait1["_field"] == trait2["_field"]:
        return False
    vals1 = {k: v for k, v in trait1.items() if not k.startswith("_")}
    vals2 = {k: v for k, v in trait2.items() if not k.startswith("_")}
    return vals1 == vals2


def same_data_parsers(trait1, trait2):
    if trait1["_field"] != trait2["_field"]:
        return False
    if trait1["_parser"] == trait2["_parser"]:
        return False
    vals1 = {k: v for k, v in trait1.items() if not k.startswith("_")}
    vals2 = {k: v for k, v in trait2.items() if not k.startswith("_")}
    return vals1 == vals2
