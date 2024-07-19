from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd

# from pprint import pp

COMPARE = {
    "body_mass": ["body_mass_grams"],
    "ear_length": ["ear_length_mm"],
    "embryo_size": ["embryo_size_length_mm", "embryo_size_width_mm"],
    "forearm_length": ["forearm_length_mm"],
    "gonad_size": ["gonad_length_mm", "gonad_width_mm"],
    "hind_foot_length": ["hind_foot_length_mm"],
    "tail_length": ["tail_length_mm"],
    "tibia_length": ["tibia_length_mm"],
    "total_length": ["total_length_mm"],
    "tragus_length": ["tragus_length_mm"],
}

DUPE_CHECK = 2
ORDER = "trait_reported_order"


@dataclass
class Contestant:
    score: dict
    trait: dict


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

        max_traits = 0
        for traits in grouped.values():
            max_traits = max(max_traits, len(traits))

        filtered = defaultdict(list)
        for name, traits in grouped.items():
            filtered[name] = filter_traits(name, traits, max_traits)

        lst = []
        for name, traits in filtered.items():
            for i, trait in enumerate(traits, 1):
                if i > len(lst):
                    lst.append({ORDER: i} | row)
                new = {k: v for k, v in trait.items() if not k.startswith("_")}
                lst[i - 1] |= new
                trait_cols |= {(name, k) for k in new}

        if not lst:
            lst.append({ORDER: 1} | row)
        elif len(lst) == DUPE_CHECK:
            one = {k: v for k, v in lst[0].items() if k != ORDER}
            two = {k: v for k, v in lst[1].items() if k != ORDER}
            if one == two:
                lst.pop()

        data += lst

    # Sort columns
    trait_cols = sorted(trait_cols)
    columns = [
        id_field,
        ORDER,
        "source",
        *info_fields,
        *parse_fields,
        *[t[1] for t in sorted(trait_cols)],
    ]
    df = pd.DataFrame(data)
    df = df.loc[:, columns]

    df = df.set_index(id_field)
    df.to_csv(csv_file)


def filter_traits(name: str, traits: list[dict], max_traits: int) -> list[dict]:
    players = [get_score(name, t) for t in traits]
    winners = [True for _ in range(len(players))]

    for pair in combinations(range(len(traits)), 2):
        i, j = pair
        if players[i].score == players[j].score:
            if max_traits == DUPE_CHECK:
                choose_looser(i, j, players, winners)
            elif (
                players[i].trait["_field"] == players[j].trait["_field"]
                and players[i].trait["_parser"] != players[j].trait["_parser"]
            ):
                choose_looser(i, j, players, winners)
            elif players[i].trait["_field"] != players[j].trait["_field"]:
                choose_looser(i, j, players, winners)

    return [p.trait for i, p in enumerate(players) if winners[i]]


def choose_looser(i, j, players, winners):
    len1 = len([k for k in players[i].trait if not k.startswith("_")])
    len2 = len([k for k in players[j].trait if not k.startswith("_")])
    if len2 > len1:
        winners[i] = False
    else:
        winners[j] = False


def get_score(name: str, trait: dict) -> Contestant:
    if keys := COMPARE.get(name):
        return Contestant(
            score={k: v for k in keys if (v := trait.get(k) is not None)},
            trait=trait,
        )
    return Contestant(
        score={k: v for k, v in trait.items() if not k.startswith("_")},
        trait=trait,
    )
