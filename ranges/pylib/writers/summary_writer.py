from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd


def write_summary(
    summary_path: Path,
    occurrences: list[dict[str, Any]],
    summarize_by: str,
) -> None:
    summary = defaultdict(lambda: defaultdict(int))
    for occur in occurrences:
        key = occur["info_fields"][summarize_by]
        summary[key]["occurrences"] += 1
        for trait in occur["traits"]:
            summary[key][trait["_trait"]] += 1

    flat = [{summarize_by: k} | v for k, v in summary.items()]

    df = pd.DataFrame(flat).fillna(0)
    df = df.set_index(summarize_by)
    df = df.astype(int)

    cols = sorted(c for c in df.columns if c != "occurrences")
    df = df[*cols, "occurrences"]
    df = df.sort_index()

    df.loc["Total"] = df.sum()

    df = df.replace(0, "")

    df.to_csv(summary_path)
