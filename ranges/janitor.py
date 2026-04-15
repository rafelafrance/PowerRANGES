#!/usr/bin/env python3
import argparse
import csv
import re
import textwrap
from glob import glob
from pathlib import Path

import pandas as pd

from ranges.pylib import log

INT = re.compile(r"\d+")
FLOAT = re.compile(r" \d+ (?: \.\d* )? | \.\d+", flags=re.VERBOSE)
FRACT = re.compile(r" (\d*) \s+ (\d+ / \d+) ", flags=re.VERBOSE)
UNITS = {
    # Length
    "c.m.": 10.0,
    "centimeters": 10.0,
    "cm": 10.0,
    "cm.": 10.0,
    "cm.s": 10.0,
    "cms": 10.0,
    "'": 304.8,
    "feet": 304.8,
    "foot": 304.8,
    "ft": 304.8,
    "ft.": 304.8,
    '"': 25.4,
    "in": 25.4,
    "in.": 25.4,
    "inch": 25.4,
    "inches": 25.4,
    "ins": 25.4,
    "meter": 1000.0,
    "meters": 1000.0,
    # Mass
    "kg": 1000.0,
    "kg.": 1000.0,
    "kgs": 1000.0,
    "kgs.": 1000.0,
    "kilograms": 1000.0,
    "lb": 453.5924,
    "lb.": 453.5924,
    "lbs": 453.5924,
    "lbs.": 453.5924,
    "mg": 0.001,
    "mg.": 0.001,
    "mgs.": 0.001,
    "mgs": 0.001,
    "ounce": 28.34952,
    "ounces": 28.34952,
    "oz": 28.34952,
    "oz.": 28.34952,
    "ozs": 28.34952,
    "ozs.": 28.34952,
    "pound": 453.5924,
    "pounds": 453.5924,
}


def main(args: argparse.Namespace) -> None:
    log.started()

    # args.output_dir.mkdir(parents=True, exist_ok=True)
    # to_csv(args)

    anourosorex_yamashinai_mod(args)
    antrozous_pallidus_mod(args)

    log.finished()


def antrozous_pallidus_mod(args: argparse.Namespace) -> None:
    name = "Antrozous pallidus_mod.csv"
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "catalogNumber": in_row["catalognumberint"],
                "recordNumber": in_row["GUID"],
                "scientificName": to_sci_name(in_row["SUBSPECIES"]),
                "infraspecificEpithet": to_sub_spec(in_row["SUBSPECIES"]),
                "county": in_row["COUNTY"],
                "locality": in_row["SPEC_LOCALITY"],
                "preservedSpecimen": in_row["PARTS"],
                "sex": in_row["sex"],
                "totalLengthInMillimeters": to_mm(
                    in_row["total length"], in_row["unit"]
                ),
                "earLengthInMillimeters": to_mm(in_row["ear"], in_row["unit"]),
                "earLengthFromNotchInMillimeters": to_mm(
                    in_row["ear from notch"], in_row["unit"]
                ),
                "earLengthFromCrownInMillimeters": to_mm(
                    in_row["ear from crown"], in_row["unit"]
                ),
                "forearmLengthInMillimeters": to_mm(in_row["forearm"], in_row["unit"]),
                "bodyMassInGrams": to_grams(in_row["weight"], in_row["units"]),
                "lifeStage": in_row["life stage"],
                "reproductiveCondition": in_row["reproductive data"],
                "unformattedMeasurements": in_row["unformatted measurements"],
                "testisSizeLeftInMillimeters": to_mm(
                    in_row["testes L"], in_row["unit"]
                ),
                "testisSizeRightInMillimeters": to_mm(
                    in_row["testes W"], in_row["unit"]
                ),
                "embryoCount": to_int(in_row["emb count"]),
                "embryoCountLeft": to_int(in_row["embs L"]),
                "embryoCountRight": to_int(in_row["embs R"]),
                "embryoCrownRumpLengthInMillimeters": to_mm(
                    in_row["emb CR"], in_row["unit"]
                ),
                "tagChecked": in_row[
                    "tag checked? (or no tag available), initial here"
                ],
                "day": to_int(in_row["Day"]),
                "month": to_int(in_row["Month"]),
                "year": to_int(in_row["Year"]),
            }
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def anourosorex_yamashinai_mod(args: argparse.Namespace) -> None:
    name = "Anourosorex_yamashinai_mod.csv"
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "recordNumber": in_row["MVZ #"],
                "scientificName": to_sci_name(in_row["sci name"]),
                "stateProvince": in_row["state"],
                "county": in_row["county"],
                "locality": in_row["specific"],
                "recordedBy": in_row["collector"],
                "recordedByID": in_row["coll #"],
                "eventDate": in_row["date"],
                "sex": in_row["sex"],
                "preservedSpecimen": in_row["parts"],
                "occurrenceRemarks": in_row[
                    "remarks (data discrepancy, need to revisit specimen, etc.)"
                ],
                "totalLengthInMillimeters": to_mm(in_row["total"], in_row["unit"]),
                "tailLengthInMillimeters": to_mm(in_row["tail"], in_row["unit"]),
                "hindFootLengthInMillimeters": to_mm(in_row["hf"], in_row["unit"]),
                "earLengthInMillimeters": to_mm(in_row["ear"], in_row["unit"]),
                "earLengthFromNotchInMillimeters": to_mm(
                    in_row["Notch"], in_row["unit"]
                ),
                "earLengthFromCrownInMillimeters": to_mm(
                    in_row["Crown"], in_row["unit"]
                ),
                "bodyMassInGrams": to_grams(in_row["wt"], in_row["units"]),
                "reproductiveCondition": in_row["repro comments"],
                "testisSizeLeftInMillimeters": to_mm(
                    in_row["testis L"], in_row["unit"]
                ),
                "testisSizeRightInMillimeters": to_mm(
                    in_row["testis R"], in_row["unit"]
                ),
                "embryoCount": to_int(in_row["emb count"]),
                "embryoCountLeft": to_int(in_row["embs L"]),
                "embryoCountRight": to_int(in_row["embs R"]),
                "embryoCrownRumpLengthInMillimeters": to_mm(
                    in_row["emb CR"], in_row["unit"]
                ),
                "placentalScarCount": to_int(in_row["scars"]),
                "attributeSource": in_row["source and date for most attributes"],
                "skinTagChecked": in_row[
                    "skin tag checked? (or no skin tag available)"
                ],
                "catalogChecked": in_row["catalog checked? (or no catalog available)"],
                "dateScanned": in_row["Unnamed: 33"],
                "arctosUploadDate": in_row["data uploaded to Arctos?"],
            }
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def to_sci_name(value: str) -> str:
    words = value.split()
    return " ".join(words[:2])


def to_sub_spec(value: str) -> str:
    words = value.split()
    return words[2] if len(words) > 2 else ""


def as_int(value: str) -> int | None:
    value = re.sub(r",", "", value)
    m = INT.search(value)
    return int(m[0]) if m else None


def to_int(value: str) -> str:
    num = as_int(value)
    return "" if num is None else str(num)


def to_grams(value: str, units: str = "g", dec: int = 1) -> str:
    return convert_units(value, units, dec)


def to_mm(value: str, units: str = "mm", dec: int = 1) -> str:
    return convert_units(value, units, dec)


def convert_units(value: str, units: str, dec: int) -> str:
    num = as_float(value)

    if num is None:
        return ""

    factor = UNITS.get(units.lower(), 1.0)
    num *= factor
    num = round(num, dec)
    return str(num)


def as_float(value: str) -> float | None:
    value = re.sub(r",", "", value)

    # Handle numbers formatted like: 4 1/4
    if m := FRACT.search(value):
        whole = as_float(m[1]) or 0.0
        num, denom = m[2].split("/")
        num = as_float(num) or 0.0
        denom = as_float(denom)
        if denom is None:
            return None
        return whole + (num / denom)

    m = FLOAT.search(value)
    return float(m[0]) if m else None


def to_float(value: str, dec: int = 1) -> str:
    flt = as_float(value)
    return f"{flt:0.{dec}f}" if flt is not None else ""


def to_csv(args: argparse.Namespace) -> None:
    args.csv_dir.mkdir(parents=True, exist_ok=True)
    for path in args.glob:
        print(path)
        df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
        out_csv = args.csv_dir / f"{path.stem}.csv"
        df.to_csv(out_csv, index=False)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """Normalize data from previous extractions.""",
        ),
    )

    arg_parser.add_argument(
        "--glob",
        required=True,
        action="append",
        metavar="GLOB",
        help="""Input this CSV. Wild cards must be quoted""",
    )

    arg_parser.add_argument(
        "--csv-dir",
        required=True,
        metavar="PATH",
        type=Path,
        help="""Store CSV files to this directory.""",
    )

    arg_parser.add_argument(
        "--output-dir",
        required=True,
        metavar="PATH",
        type=Path,
        help="""Output files to this directory.""",
    )

    args = arg_parser.parse_args()

    all_paths = []
    for path in args.glob:
        paths = glob(path)  # noqa: PTH207
        all_paths += paths
    args.glob = [Path(f) for f in sorted(all_paths)]

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
