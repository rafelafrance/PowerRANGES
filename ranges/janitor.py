#!/usr/bin/env python3
import argparse
import csv
import re
import textwrap
from glob import glob
from pathlib import Path
from pprint import pp

import pandas as pd

from ranges.pylib import log, pipeline

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

PIPELINE = pipeline.build()
FEMALE_REPRO = pipeline.female_repro()
MALE_REPRO = pipeline.male_repro()
LEN_SHORTHAND = pipeline.shorthand()
BODY_MASS = pipeline.body_wt()


def main(args: argparse.Namespace) -> None:
    log.started()

    # args.output_dir.mkdir(parents=True, exist_ok=True)
    # to_csv(args)

    # anourosorex_yamashinai_mod(args)
    # antrozous_pallidus_mod(args)
    cas_y1_y2_trait_data_only(args)

    log.finished()


def cas_y1_y2_trait_data_only(args: argparse.Namespace) -> None:
    name = "CAS Y1&Y2 Trait Data Only (1).csv"
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occuranceID": in_row["occuranceID"],
                "catalogNumber": in_row["catalog#"],
                "scientificName": in_row["scientific name"],
                "countryCode": in_row["country code"],
                "institutionCode": in_row["institution code"],
                "sex": in_row["sex"],
                "LifeStage": in_row["age class"],
            }
            out_row |= parse_body_mass(in_row["weight"])
            out_row |= parse_shorthand(in_row["trait data (SL-Tail-Hind Foot-Ear)"])
            # in_row["reproductive condition"]
            # in_row["other trait remarks"]
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


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
                "day": to_int(in_row["Day"]),
                "month": to_int(in_row["Month"]),
                "year": to_int(in_row["Year"]),
                "sex": in_row["sex"],
                "body_mass_grams": to_grams(in_row["weight"], in_row["units"]),
                "ear_length_measured_from": ear_length_from(
                    in_row["ear from notch"], in_row["ear from crown"]
                ),
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "embryo_count": to_int(in_row["emb count"]),
                "embryo_count_left": to_int(in_row["embs L"]),
                "embryo_count_right": to_int(in_row["embs R"]),
                "embryo_size_length": to_mm(in_row["emb CR"], in_row["unit"]),
                "forearm_length": to_mm(in_row["forearm"], in_row["unit"]),
                "life_stage": in_row["life stage"],
                "reproductiveCondition": in_row["reproductive data"],
                "testicle_length": to_mm(in_row["testes L"], in_row["unit"]),
                "testicle_width": to_mm(in_row["testes W"], in_row["unit"]),
                "total_length": to_mm(in_row["total length"], in_row["unit"]),
                "tag_checked": in_row[
                    "tag checked? (or no tag available), initial here"
                ],
                "unformatted_measurements": in_row["unformatted measurements"],
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
                "reproductiveCondition": in_row["repro comments"],
                "preservedSpecimen": in_row["parts"],
                "occurrenceRemarks": in_row[
                    "remarks (data discrepancy, need to revisit specimen, etc.)"
                ],
                "sex": in_row["sex"],
                "body_mass_grams": to_grams(in_row["wt"], in_row["units"]),
                "ear_length_measured_from": ear_length_from(
                    in_row["Notch"], in_row["Crown"]
                ),
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "embryo_count": to_int(in_row["emb count"]),
                "embryo_count_left": to_int(in_row["embs L"]),
                "embryo_count_right": to_int(in_row["embs R"]),
                "embryo_size_length": to_mm(in_row["emb CR"], in_row["unit"]),
                "hind_foot_length": to_mm(in_row["hf"], in_row["unit"]),
                "placental_scar_count": to_int(in_row["scars"]),
                "tail_length": to_mm(in_row["tail"], in_row["unit"]),
                "testicle_length_2nd": to_mm(in_row["testis R"], in_row["unit"]),
                "testicle_length": to_mm(in_row["testis L"], in_row["unit"]),
                "total_length": to_mm(in_row["total"], in_row["unit"]),
                "arctos_upload_date": in_row["data uploaded to Arctos?"],
                "attribute_source": in_row["source and date for most attributes"],
                "catalog_checked": in_row["catalog checked? (or no catalog available)"],
                "date_scanned": in_row["Unnamed: 33"],
                "skin_tag_checked": in_row[
                    "skin tag checked? (or no skin tag available)"
                ],
            }
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def parse_shorthand(text: str) -> dict:
    doc = LEN_SHORTHAND(text)
    traits = [e._.trait for e in doc.ents]
    shorts = {}
    shorts = traits[0].for_csv() if traits and hasattr(traits[0], "for_csv") else {}
    print(text)
    pp(shorts)
    print()
    return shorts


def parse_body_mass(text: str) -> dict:
    doc = BODY_MASS(text)
    traits = [e._.trait.to_dict() for e in doc.ents]
    body = {}
    if traits and traits[0].get("mass"):
        body = {"body_mass_grams": traits[0]["mass"]}
    return body


def ear_length_from(notch: str, crown: str) -> str:
    if notch:
        return "notch"
    return "crown" if crown else ""


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
