#!/usr/bin/env python3
import argparse
import csv
import logging
import re
import textwrap
from collections import defaultdict
from glob import glob
from pathlib import Path

import pandas as pd
from spacy.tokens import Doc

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

    anourosorex_yamashinai_mod(args)
    antrozous_pallidus_mod(args)
    cas_y1_y2_trait_data_only(args)
    csulb_sciuridae_traits(args)
    dmns_ranges_traits_dmns_y1_mod(args)
    dmns_ranges_traits_dmns_y2_mod(args)
    eptesicus_mod(args)
    fmnh_test_ranges_traits(args)
    lacm_ranges_specimens_updated_new_data_dec2025(args)
    microtus_mod(args)
    msb_y1_y2_traits_mod(args)
    mustela_mod(args)
    myosorex_varius_mod(args)
    myotis_mod(args)

    log.finished()


def myotis_mod(args: argparse.Namespace) -> None:
    name = "Myotis_mod.csv"
    logging.info(name)

    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["scientific_name"].split()
            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "catalog_number_int": in_row["catalognumberint"],
                "catalogNumber": in_row["GUID"],
                "scientificName": in_row["SPECIES"],
                "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
                "county": in_row["COUNTY"],
                "locality": in_row["SPEC_LOCALITY"],
                "preservedSpecimen": in_row["PARTS"],
                "stateProvince": in_row["STATE_PROV"],
                "eventDate": in_row["VERBATIM_DATE"],
                "recordedByID": in_row["COLLECTOR_NUMBER"],
                "sex": in_row["sex"],
                "total_length": to_mm(in_row["total_length"], in_row["unit"]),
                "tail_length": to_mm(in_row["tail_length"], in_row["unit"]),
                "hind_foot_length_from_claw": to_mm(
                    in_row["hind_foot_length_from_claw"], in_row["unit"]
                ),
                "ear_length_from_notch": to_mm(
                    in_row["ear_from_notch"], in_row["unit"]
                ),
                "ear_length_from_crown": to_mm(
                    in_row["ear_from_crown"], in_row["unit"]
                ),
                "tragus_length": to_mm(in_row["tragus"], in_row["unit"]),
                "forearm_length": to_mm(in_row["forearm"], in_row["unit"]),
                "body_mass": to_grams(in_row["weight"], in_row["units"]),
                "lifeStage": in_row["lifestage"],
                "reproductiveCondition": in_row["reproductive data"],
                "unformatted_measurements": in_row["unformatted measurements"],
                "testis_length": in_row["testes L"],
                "testis_width": in_row["testes W"],
                "embryo_count": in_row["emb count"],
                "embryo_count_left": in_row["embs L"],
                "embryo_count_right": in_row["embs R"],
                "embryo_size_length": in_row["emb CR"],
                "placental_scar_count": in_row["scars"],
                "tag_checked": in_row['"tag checked? (or no tag available)"'],
                "initial_here": in_row['" initial here"'],
                "day": in_row["Day"],
                "month": in_row["Month"],
                "year": in_row["Year"],
                "review_needed": in_row["REVIEW NEEDED"],
            }
            out_row |= parse_all(in_row["reproductive data"], out_row)

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def myosorex_varius_mod(args: argparse.Namespace) -> None:
    name = "Myosorex_varius_mod.csv"
    logging.info(name)

    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["sci name"].split()

            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "mvz_num": in_row["MVZ #"],
                "scientificName": " ".join(sci_name[:2]) if len(sci_name) > 1 else "",
                "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
                "stateProvince": in_row["state"],
                "county": in_row["county"],
                "locality": in_row["specific"],
                "recordedBy": in_row["collector"],
                "recordedByID": in_row["coll #"],
                "eventDate": in_row["date"],
                "sex": in_row["sex"],
                "preservedSpecimen": in_row["parts"],
                "total_length": to_mm(in_row["total"], in_row["unit"]),
                "tail_length": to_mm(in_row["tail"], in_row["unit"]),
                "hindfoot_length": to_mm(in_row["hf"], in_row["unit"]),
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "ear_length_from_notch": to_mm(in_row["Notch"], in_row["unit"]),
                "ear_length_from_crown": to_mm(in_row["Crown"], in_row["unit"]),
                "body_mass": to_grams(in_row["wt"], in_row["units"]),
                "testis_length": to_mm(in_row["testis L"], ""),
                "testis_length_2nd": to_mm(in_row["testis R"], ""),
                "embryo_count": to_int(in_row["emb count"]),
                "embryo_count_left": to_int(in_row["embs L"]),
                "embryo_count_right": to_int(in_row["embs R"]),
                "placental_scar_count": to_int(in_row["scars"]),
                "attribute_source": in_row["source and date for most attributes"],
                "skin_tag_checked": in_row[
                    "skin tag checked? (or no skin tag available)"
                ],
                "catalog_checked": in_row["catalog checked? (or no catalog available)"],
                "fieldNotes": in_row["Unnamed: 32"],
                "uploaded_to_arctos": in_row["data uploaded to Arctos?"],
                "occurrenceRemarks": in_row[
                    "remarks (data discrepancy, need to revisit specimen, etc.)"
                ],
            }
            out_row |= parse_all(in_row["repro comments"], out_row)

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def mustela_mod(args: argparse.Namespace) -> None:
    name = "mustela_mod.csv"
    logging.info(name)

    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["subspecies"].split()

            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "mvz_num": in_row["mvz_num"],
                "scientificName": " ".join(sci_name[:2]) if len(sci_name) > 1 else "",
                "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
                "recordedBy": in_row["collectors"],
                "country": in_row["country"],
                "stateProvince": in_row["state_prov"],
                "county": in_row["county"],
                "locality": in_row["spec_locality"],
                "eventDate": in_row["ended_date"],
                "preservedSpecimen": in_row["parts"],
                "total_length": to_mm(in_row["total_length"], in_row["length_units"]),
                "tail_length": to_mm(in_row["tail_length"], in_row["length_units"]),
                "hind_foot_with_claw": to_mm(
                    in_row["hind_foot_with_claw"], in_row["length_units"]
                ),
                "ear_length_from_notch": to_mm(
                    in_row["ear_from_notch"], in_row["length_units"]
                ),
                "ear_length_from_crown": to_mm(
                    in_row["ear_from_crown"], in_row["length_units"]
                ),
                "weight": to_grams(in_row["weight"], in_row["weight_units"]),
                "lifeStage": in_row["lifestage"],
                "reproductiveCondition": in_row["reproductive_data"],
                "testis_length": in_row["testes_length"],
                "testes_width": in_row["testes_width"],
                "embryo_count": in_row["embryo_count"],
                "embryo_count_left": in_row["embryo_count_left"],
                "embryo_count_right": in_row["embryo_count_right"],
                "embryo_size_length": in_row["crown_rump_length"],
                "placental_scar_count": in_row["scars"],
                "unformatted_measurements": in_row["unformatted_measurements"],
                "initials": in_row["initials"],
                "day": in_row["day"],
                "month": in_row["month"],
                "year": in_row["year"],
                "review_needed": in_row["review_needed"],
            }
            out_row |= parse_all(in_row["reproductive_data"], out_row)
            out_row |= parse_all(in_row["unformatted_measurements"], out_row)

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def msb_y1_y2_traits_mod(args: argparse.Namespace) -> None:
    name = "MSB-Y1-Y2-traits_mod.csv"
    logging.info(name)

    columns = [
        (f"trait name/type {i}", f"measurement {i}", f"units {i}") for i in range(1, 16)
    ]

    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occurenceID": in_row["occurenceID"],
                "msb_id": in_row["MSBID"],
                "catalogNumber": in_row["catalogNumber"],
                "scientificName": in_row["scientificName"],
                "country": in_row["countryCode"],
                "institutionCode": in_row["institutionCode"],
                "order": in_row["order"],
                "family": in_row["family"],
                "genus": in_row["genus"],
                "specificEpithet": in_row["specificEpithet"],
                "stateProvince": in_row["state/province"],
                "county": in_row["County"],
                "decimalLatitude": in_row["decLat"],
                "decimalLongitude": in_row["decLon"],
                "eventDate": in_row["eventDate"],
                "day": in_row["day"],
                "month": in_row["month"],
                "year": in_row["year"],
                "occurrenceRemarks": in_row["occurrenceRemarks"],
                "dynamicProperties": in_row["dynamicProperties"],
            }
            for trait, meas, units in columns:
                match in_row[trait].strip():
                    case "":
                        pass
                    case "age":
                        out_row["age"] = in_row[meas]
                    case "crown-rump length":
                        out_row["embryo_size_length"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "detected":
                        out_row["detected"] = in_row[meas]
                    case "ear length from notch" | "ear from notch":
                        out_row["ear_length_from_notch"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "forearm length":
                        out_row["forearm_length"] = to_mm(in_row[meas], in_row[units])
                    case "hind foot with claw":
                        out_row["hind_foot_length_from_claw"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "life stage":
                        out_row["lifeStage"] = in_row[meas]
                    case "reproductive data":
                        doc = PIPELINE(in_row[meas])
                        out_row |= get_traits(doc)
                    case "sex":
                        out_row["sex"] = in_row[meas]
                    case "tail length":
                        out_row["tail_length"] = to_mm(in_row[meas], in_row[units])
                    case "thumb length with claw":
                        out_row["thumb_length_with_claw"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "total length":
                        out_row["total_length"] = to_mm(in_row[meas], in_row[units])
                    case "tragus length":
                        out_row["tragus_length"] = to_mm(in_row[meas], in_row[units])
                    case "unformatted measurements":
                        doc = PIPELINE(in_row[meas])
                        out_row |= get_traits(doc)
                    case "weight":
                        out_row["body_mass"] = to_grams(in_row[meas], in_row[units])
                    case _:
                        logging.error(f"{in_row[trait]=}")
                        raise ValueError

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def microtus_mod(args: argparse.Namespace) -> None:
    name = "Microtus_mod.csv"
    logging.info(name)
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["subspecies"].split()

            words = in_row["collector number"].split()
            coll_no = " ".join(w for w in words if re.search(r"\d", w))

            out_row = {
                "occurenceID": in_row["occurrenceID"],
                "catalogNumber": in_row["catalognumberint"],
                "occurrence_id_2": in_row["guid"],
                "scientificName": " ".join(sci_name[:2]) if len(sci_name) > 1 else "",
                "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
                "recordedBy": in_row["collectors"],
                "stateProvince": in_row["state_prov"],
                "country": in_row["county"],
                "locality": in_row["spec_locality"],
                "coll_no": coll_no,
                "verbatimEventDate": in_row["verbatim_date"],
                "preservedSpecimen": in_row["parts"],
                "sex": in_row["sex"],
                "total_length": to_mm(in_row["total length"], in_row["unit"]),
                "tail_length": to_mm(in_row["tail length"], in_row["unit"]),
                "hind_foot_length_from_claw": to_mm(
                    in_row["hind foot with claw"], in_row["unit"]
                ),
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "ear_length_from_notch": to_mm(
                    in_row["ear from notch"], in_row["unit"]
                ),
                "ear_length_from_crown": to_mm(
                    in_row["ear from crown"], in_row["unit"]
                ),
                "body_mass": to_grams(in_row["weight"], in_row["units"]),
                "lifeStage": in_row["life stage"],
                "reproductiveCondition": in_row["reproductive data"],
                "testis_length": in_row["testes L"],
                "testis_width": in_row["testes W"],
                "embryo_count": in_row["emb count"],
                "embryo_count_left": in_row["embs L"],
                "embryo_count_right": in_row["embs R"],
                "embryo_size_length": in_row["emb CR"],
                "placental_scar_count": in_row["scars"],
                "unformatted_measurements": in_row["unformatted measurements"],
                "tag_checked": in_row[
                    "tag checked? (or no tag available), initial here"
                ],
                "day": in_row["Day"],
                "month": in_row["Month"],
                "year": in_row["Year"],
                "review_needed": in_row["REVIEW NEEDED"],
            }

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def lacm_ranges_specimens_updated_new_data_dec2025(args: argparse.Namespace) -> None:
    name = "LACM_Ranges_specimens_updated_new_data_Dec2025.csv"
    logging.info(name)
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["scientificName"]
            sci_name = sci_name.removesuffix(in_row["AutAuthorString"]).strip()

            out_row = {
                "catalogNumber": in_row["catalogNumber"],
                "institutionCode": in_row["institutionCode"],
                "accession_number": in_row["ColAccessionNumber"],
                "designation_tab": in_row["MamDesignation_tab"],
                "order": in_row["order"],
                "subOrder": in_row["ClaSuborder"],
                "family": in_row["family"],
                "subFamily": in_row["ClaSubfamily"],
                "genus": in_row["genus"],
                "subGenus": in_row["ClaSubgenus"],
                "specificEpithet": in_row["specificEpithet"],
                "infraspecificEpithet": in_row["ClaSubspecies"],
                "scientificName": sci_name,
                "scientificNameAuthorship": in_row["AutAuthorString"],
                "taxonRank": in_row["ClaRank"],
                "id_remarks": in_row["MamIDRemarks"],
                "identifier": in_row["MamIdentifier"],
                "sex": in_row["MamSex"],
                "preparation": in_row["MamPreparation"],
                "measurements": in_row["MamMeasurements"],
                "body_mass": in_row["MamWeightG"],
                "environment": in_row["MamEnvironment"],
                "recordedBy": in_row["MamCollector"],
                "eventDate": in_row["eventDate"],
                "verbatimElevation": in_row["MamElevation"],
                "maximumElevationInMeters": in_row["MamElevationMax"],
                "minimumElevationInMeters": in_row["MamElevationMin"],
                "preparator": in_row["MamPreparator"],
                "prep_field_number": in_row["MamPrepFieldNo"],
                "occurrenceRemarks": in_row["occurrenceRemarks"],
                "laf_number": in_row["MamLAFNo"],
                "reproductiveCondition": in_row["MamReproductive"],
                "occurenceID": in_row["occurrenceID"],
                "ocean": in_row["LocOcean_tab"],
                "country": in_row["countryCode"],
                "stateProvince": in_row["state/province"],
                "county": in_row["County"],
                "municipality": in_row["LocNearestNamedPlace_tab"],
                "locality": in_row["LocPreciseLocation"],
                "decimalLatitude": in_row["decLat"],
                "decimalLongitude": in_row["decLon"],
                "sex_transcribed": in_row["MamSex_transcribed"],
                "lifeStage": in_row["MamPhyAge_transcribed"],
                "total_length": to_mm(in_row["MamTotalLength"], in_row["length_units"]),
                "tail_lenth": to_mm(in_row["MamTailLength"], in_row["length_units"]),
                "hindfoot_length": to_mm(in_row["MamHindFoot"], in_row["length_units"]),
                "ear_length": to_mm(in_row["MamEar"], in_row["length_units"]),
                "body_mass_transcribed": in_row["MamWeight_transcribed"],
                "body_mass_units": in_row["MamWeight_transcribed_unit"],
                "reproductive_condition_transcribed": in_row["MamReprod_transcribed"],
            }

            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def fmnh_test_ranges_traits(args: argparse.Namespace) -> None:
    name = "FMNH_Test_Ranges_Traits (1).csv"
    logging.info(name)
    spelling = {
        "_ear_length_": "ear_length",
        "ear length": "ear_length",
        "ear_length": "ear_length",
        "ear_length_": "ear_length",
        "hindfood length": "hindfoot_length",
        "hindfood_length": "hindfoot_length",
        "hindfoot lemgth": "hindfoot_length",
        "hindfoot length": "hindfoot_length",
        "hindfoot": "hindfoot_length",
        "hindfoot_lemgth": "hindfoot_length",
        "hindfoot_length": "hindfoot_length",
        "hindfoot_length_": "hindfoot_length",
        "hindoot length": "hindfoot_length",
        "hindoot_length": "hindfoot_length",
        "tail lenght": "tail_length",
        "tail lengtgh": "tail_length",
        "tail length": "tail_length",
        "tail lenth": "tail_length",
        "tail_lenght": "tail_length",
        "tail_lengtgh": "tail_length",
        "tail_length": "tail_length",
        "tail_length_": "tail_length",
        "tail_lenth": "tail_length",
        "taill length": "tail_length",
        "taill_length": "tail_length",
        "taillength": "tail_length",
        "total length": "total_length",
        "total_length": "total_length",
        "total_length_": "total_length",
    }
    in_name = args.csv_dir / name
    row = defaultdict(dict)
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            key = in_row["occurrenceID"]
            row[key]["occurrenceID"] = in_row["occurrenceID"]
            row[key]["catalogNumber"] = in_row["catalogNumber"]

            sci_name = in_row["scientificName"].split()
            row[key]["scientificName"] = (
                " ".join(sci_name[:2]) if len(sci_name) > 1 else ""
            )
            row[key]["infraspecificEpithet"] = sci_name[2] if len(sci_name) > 2 else ""

            row[key]["country"] = in_row["countryCode"]
            row[key]["institutionCode"] = in_row["institutionCode"]

            row[key]["collectionCode"] = in_row["collectionCode"]
            row[key]["order"] = in_row["order"]
            row[key]["family"] = in_row["family"]
            row[key]["genus"] = in_row["genus"]
            row[key]["specificEpithet"] = in_row["specificEpithet"]
            row[key]["stateProvince"] = in_row["state/province"]
            row[key]["county"] = in_row["County"]
            row[key]["decimalLatitude"] = in_row["decLat"]
            row[key]["decimalLongitude"] = in_row["decLon"]

            row[key]["eventDate"] = in_row["eventDate"][:10].removesuffix("-")
            row[key]["day"] = in_row["day"]
            row[key]["month"] = in_row["month"]
            row[key]["year"] = in_row["year"]

            row[key]["occurrenceRemarks"] = in_row["occurrenceRemarks"]
            row[key]["dynamicProperties"] = in_row["dynamicProperties"]

            trait = in_row["trait name/type"].lower().strip()
            if trait:
                trait = spelling[trait]
                row[key][trait] = to_mm(in_row["measurement"], in_row["units"])

    df = pd.DataFrame(list(row.values()))
    path = args.output_dir / name
    df.to_csv(path, index=False)


def eptesicus_mod(args: argparse.Namespace) -> None:
    name = "Eptesicus_mod.csv"
    logging.info(name)
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            sci_name = in_row["SUBSPECIES"].split()
            words = in_row["COLLECTOR_NUMBER"].split()
            collector = " ".join(w for w in words if not re.search(r"\d", w))
            coll_no = " ".join(w for w in words if re.search(r"\d", w))
            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "catalogNumber": in_row["catalognumberint"],
                "occurrence_id_2": in_row["GUID"],
                "scientificName": " ".join(sci_name[:2]) if len(sci_name) > 1 else "",
                "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
                "county": in_row["COUNTY"],
                "locality": in_row["SPEC_LOCALITY"],
                "stateProvince": in_row["STATE_PROV"],
                "recordedBy": collector,
                "recordedByID": coll_no,
                "preservedSpecimen": in_row["PARTS"],
                "sex": in_row["sex"],
                "total_length": to_mm(in_row["total length"], in_row["unit"]),
                "tail_length": to_mm(in_row["tail length"], in_row["unit"]),
                "hind_foot_length_from_claw": to_mm(
                    in_row["hind foot with claw"], in_row["unit"]
                ),
                "ear_length_from_notch": to_mm(
                    in_row["ear from notch"], in_row["unit"]
                ),
                "ear_length_from_crown": to_mm(
                    in_row["ear from crown"], in_row["unit"]
                ),
                "tragus_length": to_mm(in_row["tragus"], in_row["unit"]),
                "forearm_length": to_mm(in_row["forearm"], in_row["unit"]),
                "body_mass": to_grams(in_row["weight"], in_row["units"]),
                "lifeStage": in_row["life stage"],
                "reproductiveCondition": in_row["reproductive data"],
                "unformatted_measurements": in_row["unformatted measurements"],
                "testis_length": in_row["testes L"],
                "testis_width": in_row["testes W"],
                "embryo_count": in_row["emb count"],
                "embryo_count_left": in_row["embs L"],
                "embryo_count_right": in_row["embs R"],
                "placental_scar_count": to_int(in_row["scars"]),
                "day": in_row["Day"],
                "month": in_row["Month"],
                "year": in_row["Year"],
            }
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def dmns_ranges_traits_dmns(args: argparse.Namespace, name: str) -> None:
    logging.info(name)
    columns = [
        ("trait name/type", "measurement", "units"),
        ("trait name/type2", "measurement2", "units2"),
        ("trait name/type3", "measurement3", "units3"),
        ("trait name/type4", "measurement4", "units4"),
    ]
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "dmnsID": in_row["DMNSID"],
                "catalogNumber": in_row["catalogNumber"],
                "scientificName": in_row["scientificName"],
                "country": in_row["countryCode"],
                "institutionCode": in_row["institutionCode"],
                "collectionCode": in_row["collectionCode"],
                "collection_code_1": in_row["collectionCode.1"],
                "order": in_row["order"],
                "family": in_row["family"],
                "genus": in_row["genus"],
                "specificEpithet": in_row["specificEpithet"],
                "stateProvince": in_row["state/province"],
                "county": in_row["County"],
                "decimalLatitude": in_row["decLat"],
                "decimalLongitude": in_row["decLon"],
                "eventDate": in_row["eventDate"].removesuffix(" 00:00:00"),
                "day": in_row["day"],
                "month": in_row["month"],
                "year": in_row["year"],
                "occurrenceRemarks": in_row["occurrenceRemarks"],
                "dynamicProperties": in_row["dynamicProperties"],
            }
            for trait, meas, units in columns:
                match in_row[trait].strip():
                    case "":
                        pass
                    case "age":
                        out_row["age"] = in_row[meas]
                    case "age class":
                        out_row["lifeStage"] = in_row[meas]
                    case "calcar length":
                        out_row["calcar_length"] = to_mm(in_row[meas], in_row[units])
                    case "ear length from notch" | "ear from notch":
                        out_row["ear_length_from_notch"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "hind foot with claw":
                        out_row["hind_foot_length_from_claw"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "reproductive data":
                        doc = PIPELINE(in_row[meas])
                        out_row |= get_traits(doc)
                    case "sex":
                        out_row["sex"] = in_row[meas]
                    case "tarsus length":
                        out_row["tarsus_length"] = to_mm(in_row[meas], in_row[units])
                    case "tail length":
                        out_row["tail_length"] = to_mm(in_row[meas], in_row[units])
                    case "thumb with claw":
                        out_row["thumb_length_with_claw"] = to_mm(
                            in_row[meas], in_row[units]
                        )
                    case "total length":
                        out_row["total_length"] = to_mm(in_row[meas], in_row[units])
                    case "tragus length":
                        out_row["tragus_length"] = to_mm(in_row[meas], in_row[units])
                    case "weight":
                        out_row["body_mass"] = to_grams(in_row[meas], in_row[units])
                    case _:
                        logging.error(f"{in_row[trait]=}")
                        raise ValueError
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def dmns_ranges_traits_dmns_y2_mod(args: argparse.Namespace) -> None:
    name = "DMNS_Ranges_Traits_DMNS_Y1_mod.csv"
    dmns_ranges_traits_dmns(args, name)


def dmns_ranges_traits_dmns_y1_mod(args: argparse.Namespace) -> None:
    name = "DMNS_Ranges_Traits_DMNS_Y1_mod.csv"
    dmns_ranges_traits_dmns(args, name)


def csulb_sciuridae_traits(args: argparse.Namespace) -> None:
    name = "CSULB_Sciuridae_Traits.csv"
    logging.info(name)
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occurrenceID": in_row["occurrenceID"],
                "catalogNumber": in_row["catalogNumber"],
                "scientificName": in_row["scientificName"],
                "countryCode": in_row["countryCode"],
                "institutionCode": in_row["institutionCode"],
                "sex": in_row["sex"],
                "LifeStage": in_row["age_class"],
                "total_length": to_mm(in_row["tot_length"], in_row["length_units"]),
                "tail_length": to_mm(in_row["tail_length"], in_row["length_units"]),
                "hind_foot_length": to_mm(
                    in_row["hind_foot_length"], in_row["length_units"]
                ),
                "ear_length": to_mm(in_row["ear_length"], in_row["length_units"]),
                "body_mass": to_grams(in_row["weight"], in_row["weight_units"]),
                "reproductiveCondition": in_row["repro"],
                "collectionCode": in_row["collectionCode"],
                "order": in_row["order"],
                "family": in_row["family"],
                "genus": in_row["genus"],
                "specificEpithet": in_row["specificEpithet"],
                "stateProvince": in_row["stateProvince"],
                "county": in_row["County"],
                "decimalLatitude": in_row["decLat"],
                "decimalLongitude": in_row["decLon"],
                "eventDate": in_row["eventDate"],
                "day": in_row["day"],
                "month": in_row["month"],
                "year": in_row["year"],
                "occurrenceRemarks": in_row["occurrenceRemarks"],
                "dynamicProperties": in_row["dynamicProperties"],
            }
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def cas_y1_y2_trait_data_only(args: argparse.Namespace) -> None:
    name = "CAS Y1&Y2 Trait Data Only (1).csv"
    logging.info(name)
    in_name = args.csv_dir / name
    out_data = []
    with in_name.open() as in_csv:
        reader = csv.DictReader(in_csv)
        for in_row in reader:
            out_row = {
                "occurenceID": in_row["occuranceID"],
                "catalogNumber": in_row["catalog#"],
                "scientificName": in_row["scientific name"],
                "countryCode": in_row["country code"],
                "institutionCode": in_row["institution code"],
                "sex": in_row["sex"],
                "LifeStage": in_row["age class"],
                "reproductiveCondition": in_row["reproductive condition"],
            }
            out_row |= parse_body_mass(in_row["weight"])
            out_row |= parse_shorthand(in_row["trait data (SL-Tail-Hind Foot-Ear)"])
            out_row |= parse_repro_cond(in_row["sex"], in_row["reproductive condition"])
            out_row |= parse_all(in_row["other trait remarks"], out_row)
            out_row["lengths"] = in_row["trait data (SL-Tail-Hind Foot-Ear)"]
            out_row["weight"] = in_row["weight"]
            out_row["other_traits"] = in_row["other trait remarks"]
            out_data.append(out_row)

    df = pd.DataFrame(out_data)
    path = args.output_dir / name
    df.to_csv(path, index=False)


def antrozous_pallidus_mod(args: argparse.Namespace) -> None:
    name = "Antrozous pallidus_mod.csv"
    logging.info(name)
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
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "ear_length_from_notch": to_mm(
                    in_row["ear from notch"], in_row["unit"]
                ),
                "ear_length_from_crown": to_mm(
                    in_row["ear from crown"], in_row["unit"]
                ),
                "embryo_count": to_int(in_row["emb count"]),
                "embryo_count_left": to_int(in_row["embs L"]),
                "embryo_count_right": to_int(in_row["embs R"]),
                "embryo_size_length": to_mm(in_row["emb CR"], in_row["unit"]),
                "forearm_length": to_mm(in_row["forearm"], in_row["unit"]),
                "lifeStage": in_row["life stage"],
                "reproductiveCondition": in_row["reproductive data"],
                "testis_length": to_mm(in_row["testes L"], in_row["unit"]),
                "testis_width": to_mm(in_row["testes W"], in_row["unit"]),
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
    logging.info(name)
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
                "ear_length": to_mm(in_row["ear"], in_row["unit"]),
                "embryo_count": to_int(in_row["emb count"]),
                "embryo_count_left": to_int(in_row["embs L"]),
                "embryo_count_right": to_int(in_row["embs R"]),
                "embryo_size_length": to_mm(in_row["emb CR"], in_row["unit"]),
                "hind_foot_length": to_mm(in_row["hf"], in_row["unit"]),
                "placental_scar_count": to_int(in_row["scars"]),
                "tail_length": to_mm(in_row["tail"], in_row["unit"]),
                "testis_length_2nd": to_mm(in_row["testis R"], in_row["unit"]),
                "testis_length": to_mm(in_row["testis L"], in_row["unit"]),
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


def get_traits(doc: Doc, curr: dict | None = None) -> dict:
    curr = curr or {}
    traits = [e._.trait for e in doc.ents]
    all_ = {}
    for trait in traits:
        if hasattr(trait, "for_csv"):
            new = trait.for_csv()
            all_ |= {k: v for k, v in new.items() if not curr.get(k)}
    return all_


def parse_all(text: str, curr: dict) -> dict:
    doc = PIPELINE(text)
    return get_traits(doc, curr)


def parse_repro_cond(sex: str, text: str) -> dict:
    doc = FEMALE_REPRO(text) if sex.lower().startswith("f") else MALE_REPRO(text)
    return get_traits(doc)


def parse_shorthand(text: str) -> dict:
    doc = LEN_SHORTHAND(text)
    traits = [e._.trait for e in doc.ents]
    shorts = {}
    shorts = traits[0].for_csv() if traits and hasattr(traits[0], "for_csv") else {}
    return shorts


def parse_body_mass(text: str) -> dict:
    doc = BODY_MASS(text)
    return get_traits(doc)


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
        logging.info(f"Converting {path}")
        df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
        out_csv = args.csv_dir / f"{path.stem}.csv"
        df.to_csv(out_csv, index=False)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            Normalize data from previous extractions.

            All happy datasets are alike;
            each unhappy dataset is unhappy in its own way.
            """
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
