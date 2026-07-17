#!/usr/bin/env python3
import argparse
import csv
import logging
import textwrap
from glob import glob
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from ranges.janitors.anourosorex_yamashinai_mod import AnourosorexYamashinaiMod
from ranges.janitors.antrozous_pallidus_mod import AntrozousPallidusMod
from ranges.janitors.cas_y1_y2_trait_data_only import CasY1Y2TraitDataOnly
from ranges.janitors.csulb_sciuridae_traits import CsulbSciuridaeTraits
from ranges.janitors.dmns_ranges_traits_dmns import DmnsRangesTraits
from ranges.janitors.eptesicus_mod import EptesicusMod
from ranges.janitors.fmnh_test_ranges_traits import (
    FmnhTestRangesTraits,
    fmnh_multi_row_cleaner,
)
from ranges.janitors.lacm_ranges_specimens_updated_new_data_dec2025 import (
    LACMRangesSpecimensUpdatedNewDataDec2025,
)
from ranges.pylib import log

CSVS = {
    "Anourosorex_yamashinai_mod.csv": (AnourosorexYamashinaiMod,),
    "Antrozous pallidus_mod.csv": (AntrozousPallidusMod,),
    "CAS Y1&Y2 Trait Data Only (1).csv": (CasY1Y2TraitDataOnly,),
    "CSULB_Sciuridae_Traits.csv": (CsulbSciuridaeTraits,),
    "DMNS_Ranges_Traits_DMNS_Y1_mod.csv": (DmnsRangesTraits,),
    "DMNS_Ranges_Traits_DMNS_Y2_mod.csv": (DmnsRangesTraits,),
    "Eptesicus_mod.csv": (EptesicusMod,),
    "FMNH_Test_Ranges_Traits (1).csv": (FmnhTestRangesTraits, fmnh_multi_row_cleaner),
    "LACM_Ranges_specimens_updated_new_data_Dec2025.csv": (
        LACMRangesSpecimensUpdatedNewDataDec2025,
    ),
    "Microtus_mod.csv": None,
    "MSB-Y1-Y2-traits_mod.csv": None,
    "mustela_mod.csv": None,
    "Myosorex_varius_mod.csv": None,
    "Myotis_mod.csv": None,
    "Neotoma_mod.csv": None,
    "Notiosorex_crawfordi_mod.csv": None,
    "Peromyscus_Master.csv": None,
    "Reithrodontomys_mod.csv": None,
    "Sorex_Master.csv": None,
    "Soriculus_Master.csv": None,
    "Suncus_Master.csv": None,
    "Tamias speciosus_mod.csv": None,
    "TAMU_RANGESALL_TraitsOnly2Sept2025_mod.csv": None,
    "Thomomys bottae_mod.csv": None,
    "TTU-NSF-Ranges-Data Corrections Next to Data-7-28-2025_mod.csv": None,
    "UMMZ_ranges_y2_final_mod.csv": None,
    "UWBM_Mamm_JSON_Attributes.csv": None,
    "UWYMZ_Y1_mod.csv": None,
    "UWYMZ_Y2_mod.csv": None,
}


def main(args: argparse.Namespace) -> None:
    log.started()

    # args.output_dir.mkdir(parents=True, exist_ok=True)
    # to_csv(args)

    for name, janitor in CSVS.items():
        if not janitor:
            continue
        logging.info(name)

        janitor_class = janitor[0]

        cleaner = janitor[1] if len(janitor) > 1 else per_row_cleaner

        in_name = args.csv_dir / name

        with in_name.open() as in_csv:
            reader = csv.DictReader(in_csv)
            dirty = [dict(r) for r in reader]

        cleaned = cleaner(dirty, janitor_class)

        df = pd.DataFrame(cleaned)
        path = args.output_dir / name
        df.to_csv(path, index=False)

    log.finished()


def per_row_cleaner(dirty: list[dict], janitor_class: Any) -> list[dict]:
    cleaned = []
    for row in tqdm(dirty):
        janitor = janitor_class(dirty=row)
        janitor.cleaner()
        cleaned.append(janitor.clean)
    return cleaned


# def peromyscus_master(args: argparse.Namespace) -> None:
#     name = "Peromyscus_Master.csv"
#     logging.info(name)
#     in_name = args.csv_dir / name

#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "institutionCode": dirty["institutionCode"],
#                 "collectionCode": dirty["collectionCode"],
#                 "catalogNumber": dirty["catalognumberint"],
#                 "scientificName": dirty["subspecies"],
#                 "recordedBy": dirty["collectors"],
#                 "stateProvince": dirty["state_prov"],
#                 "county": dirty["county"],
#                 "locality": dirty["spec_locality"],
#                 "recordedByID": dirty["collectornumber"],
#                 "eventDate": dirty["verbatim_date"],
#                 "preservedSpecimen": dirty["parts"],
#                 "sex": dirty["sex"],
#                 "total length": to_mm(dirty["total"], dirty["unit"]),
#                 "tail length": to_mm(dirty["tail"], dirty["unit"]),
#                "hind_foot_length": to_mm(dirty["hind foot with claw"], dirty["unit"]),
#                 "ear_length": to_mm(dirty["earlength"], dirty["unit"]),
#                 "body_mass": to_grams(dirty["wt"], dirty["units"]),
#                 "reproductiveCondition": dirty["repro comments"],
#                 "testis_length": dirty["testes L"],
#                 "testis_width": dirty["testes W"],
#                 "source_and_date": dirty["source and date for most attributes"],
#                 "skin_tag": dirty["skin tag checked? (or no skin tag available)"],
#                "catalog_checked": dirty["catalog checked? (or no catalog available)"],
#                 "unnamed": dirty["Unnamed: 31"],
#                 "arctos_upload": dirty["data uploaded to Arctos?"],
#                 "review_need": dirty["REVIEW NEEDED"],
#             }

#             if dirty["ear_length"]:
#                 clean["ear_length"] = to_mm(dirty["earlength"], dirty["unit"])
#                 clean["ear_length_measured_from"] = ""
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"
#                 out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def notiosorex_crawfordi_mod(args: argparse.Namespace) -> None:
#     name = "Notiosorex_crawfordi_mod.csv"
#     logging.info(name)
#     in_name = args.csv_dir / name

#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "institutionCode": dirty["institutionCode"],
#                 "collectionCode": dirty["collectionCode"],
#                 "catalogNumber": dirty["MVZ #"],
#                 "scientificName": dirty["sci name"],
#                 "stateProvince": dirty["state"],
#                 "county": dirty["county"],
#                 "locality": dirty["specific"],
#                 "recordedBy": dirty["collector"],
#                 "recordedByID": dirty["coll #"],
#                 "eventDate": dirty["date"],
#                 "sex": dirty["sex"],
#                 "preservedSpecimen": dirty["parts"],
#                 "total_length": to_mm(dirty["total"], dirty["unit"]),
#                 "tail_length": to_mm(dirty["tail"], dirty["unit"]),
#                 "hind_foot_length": to_mm(dirty["hf"], dirty["unit"]),
#                 "ear_length": to_mm(dirty["earlength"], dirty["unit"]),
#                 "body_mass": to_grams(dirty["wt"], dirty["units"]),
#                 "reproductiveCondition": dirty["repro comments"],
#                 "testis_length": dirty["testes L"],
#                 "testis_width": dirty["testes W"],
#                 "source_and_date": dirty["source and date for most attributes"],
#                 "skin_tag": dirty["skin tag checked? (or no skin tag available)"],
#                "catalog_checked": dirty["catalog checked? (or no catalog available)"],
#                 "unnamed": dirty["Unnamed: 31"],
#                 "arctos_upload": dirty["data uploaded to Arctos?"],
#                 "review_need": dirty["REVIEW NEEDED"],
#             }

#             if dirty["ear_length"]:
#                 clean["ear_length"] = to_mm(dirty["earlength"], dirty["unit"])
#                 clean["ear_length_measured_from"] = ""
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"
#                 out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def neotoma_mod(args: argparse.Namespace) -> None:
#     name = "Neotoma_mod.csv"
#     logging.info(name)
#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             sci_name = dirty["scientific_name"].split()
#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "catalogNumber": dirty["guid"],
#                 "catalog_number_int": dirty["catalognumberint"],
#                 "scientificName": dirty["subspecies"],
#                 "specificEpithet": sci_name[2] if len(sci_name) > 2 else "",
#                 "recordedBy": dirty["collectors"],
#                 "stateProvince": dirty["state_prov"],
#                 "county": dirty["county"],
#                 "locality": dirty["spec_locality"],
#                 "recordedByID": dirty["collector number"],
#                 "eventDate": dirty["verbatim_date"],
#                 "preservedSpecimen": dirty["parts"],
#                 "sex": dirty["sex"],
#                 "total_length": to_mm(dirty["total length"], dirty["unit"]),
#                 "tail_length": to_mm(dirty["tail length"], dirty["unit"]),
#                "hind_foot_length": to_mm(dirty["hind foot with claw"], dirty["unit"]),
#                 "hind_foot_length_includes": "claw",
#                 # "": dirty["ear"],
#                 # "": dirty["ear from notch"],
#                 # "": dirty["ear from crown"],
#                 # "": dirty["unit"],
#                 "body_mass": to_grams(dirty["weight"], dirty["units"]),
#                 "reproductiveCondition": dirty["reproductive data"],
#                 "testis_length": to_mm(dirty["testes L"], dirty["unit"]),
#                 "testis_width": to_mm(dirty["testes W"], dirty["unit"]),
#                 # "": dirty["emb count"],
#                 # "": dirty["embs L"],
#                 # "": dirty["embs R"],
#                 "embryo_length": to_mm(dirty["emb CR"], dirty["unit"]),
#                 "embryo_length_measured_from": "crown-rump",
#                 "placental_scar_count": to_int(dirty["scars"]),
#                 "placental_scars_present": bool(dirty["scars"]),
#                 "unformatted_measurements": dirty["unformatted measurements"],
#                 "tag_checked": dirty[
#                     "tag checked? (or no tag available), initial here"
#                 ],
#                 "day": dirty["Day"],
#                 "month": dirty["Month"],
#                 "year": dirty["Year"],
#                 "review_needed": dirty["REVIEW NEEDED"],
#             }
#             set_embryo_counts(dirty, clean)

#             if dirty["ear_length"]:
#                 clean["ear_length"] = to_mm(dirty["earlength"], dirty["unit"])
#                 clean["ear_length_measured_from"] = ""
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"

#             out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def myotis_mod(args: argparse.Namespace) -> None:
#     name = "Myotis_mod.csv"
#     logging.info(name)

#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             sci_name = dirty["scientific_name"].split()
#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "institutionCode": dirty["institutionCode"],
#                 "collectionCode": dirty["collectionCode"],
#                 "catalog_number_int": dirty["catalognumberint"],
#                 "catalogNumber": dirty["GUID"],
#                 "scientificName": dirty["SPECIES"],
#                 "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
#                 "county": dirty["COUNTY"],
#                 "locality": dirty["SPEC_LOCALITY"],
#                 "preservedSpecimen": dirty["PARTS"],
#                 "stateProvince": dirty["STATE_PROV"],
#                 "eventDate": dirty["VERBATIM_DATE"],
#                 "recordedByID": dirty["COLLECTOR_NUMBER"],
#                 "sex": dirty["sex"],
#                 "total_length": to_mm(dirty["total_length"], dirty["unit"]),
#                 "tail_length": to_mm(dirty["tail_length"], dirty["unit"]),
#                 "hind_foot_length": to_mm(
#                     dirty["hind_foot_length_from_claw"], dirty["unit"]
#                 ),
#                 "hind_foot_length_includes": "claw",
#                 "tragus_length": to_mm(dirty["tragus"], dirty["unit"]),
#                 "forearm_length": to_mm(dirty["forearm"], dirty["unit"]),
#                 "body_mass": to_grams(dirty["weight"], dirty["units"]),
#                 "lifeStage": dirty["lifestage"],
#                 "reproductiveCondition": dirty["reproductive data"],
#                 "unformatted_measurements": dirty["unformatted measurements"],
#                 "testis_length": dirty["testes L"],
#                 "testis_width": dirty["testes W"],
#                 # "embryo_count": dirty["emb count"],
#                 # "embryo_count_side_1": dirty["embs L"],
#                 # "embryo_count_side_2": dirty["embs R"],
#                 "embryo_length": dirty["emb CR"],
#                 "embryo_length_measured_from": "crown-rump",
#                 "placental_scar_count": dirty["scars"],
#                 "tag_checked": dirty['"tag checked? (or no tag available)"'],
#                 "initial_here": dirty['" initial here"'],
#                 "day": dirty["Day"],
#                 "month": dirty["Month"],
#                 "year": dirty["Year"],
#                 "review_needed": dirty["REVIEW NEEDED"],
#             }
#             set_embryo_counts(dirty, clean)

#             if dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(dirty["ear_from_notch"], dirty["unit"])
#                 clean["ear_length_measured_from"] = "notch"
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(dirty["ear_from_crown"], dirty["unit"])
#                 clean["ear_length_measured_from"] = "crown"

#             clean |= parse_all(dirty["reproductive data"], clean)

#             out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def myosorex_varius_mod(args: argparse.Namespace) -> None:
#     name = "Myosorex_varius_mod.csv"
#     logging.info(name)

#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             sci_name = dirty["sci name"].split()

#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "institutionCode": dirty["institutionCode"],
#                 "collectionCode": dirty["collectionCode"],
#                 "mvz_num": dirty["MVZ #"],
#                 "scientificName": " ".join(sci_name[:2]) if len(sci_name) > 1 else "",
#                 "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
#                 "stateProvince": dirty["state"],
#                 "county": dirty["county"],
#                 "locality": dirty["specific"],
#                 "recordedBy": dirty["collector"],
#                 "recordedByID": dirty["coll #"],
#                 "eventDate": dirty["date"],
#                 "sex": dirty["sex"],
#                 "preservedSpecimen": dirty["parts"],
#                 "total_length": to_mm(dirty["total"], dirty["unit"]),
#                 "tail_length": to_mm(dirty["tail"], dirty["unit"]),
#                 "hindfoot_length": to_mm(dirty["hf"], dirty["unit"]),
#                 "body_mass": to_grams(dirty["wt"], dirty["units"]),
#                 "testis_length": to_mm(dirty["testis L"], ""),
#                 "testis_length_2": to_mm(dirty["testis R"], ""),
#                 # "embryo_count": to_int(dirty["emb count"]),
#                 # "embryo_count_side_1": to_int(dirty["embs L"]),
#                 # "embryo_count_side_2": to_int(dirty["embs R"]),
#                 "placental_scar_count": to_int(dirty["scars"]),
#                 "attribute_source": dirty["source and date for most attributes"],
#                 "skin_tag_checked": dirty[
#                     "skin tag checked? (or no skin tag available)"
#                 ],
#                "catalog_checked": dirty["catalog checked? (or no catalog available)"],
#                 "fieldNotes": dirty["Unnamed: 32"],
#                 "uploaded_to_arctos": dirty["data uploaded to Arctos?"],
#                 "occurrenceRemarks": dirty[
#                     "remarks (data discrepancy, need to revisit specimen, etc.)"
#                 ],
#             }
#             if dirty["ear_length"]:
#                 clean["ear_length"] = to_mm(dirty["earlength"], dirty["unit"])
#                 clean["ear_length_measured_from"] = ""
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"

#             clean |= parse_all(dirty["repro comments"], clean)

#             set_embryo_counts(dirty, clean)

#             out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def mustela_mod(args: argparse.Namespace) -> None:
#     name = "mustela_mod.csv"
#     logging.info(name)

#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             sci_name = dirty["subspecies"].split()

#             clean = {
#                 "occurrenceID": dirty["occurrenceID"],
#                 "institutionCode": dirty["institutionCode"],
#                 "collectionCode": dirty["collectionCode"],
#                 "mvz_num": dirty["mvz_num"],
#                 "scientificName": dirty["subspecies"],
#                 "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
#                 "recordedBy": dirty["collectors"],
#                 "country": dirty["country"],
#                 "stateProvince": dirty["state_prov"],
#                 "county": dirty["county"],
#                 "locality": dirty["spec_locality"],
#                 "eventDate": dirty["ended_date"],
#                 "preservedSpecimen": dirty["parts"],
#                 "total_length": to_mm(dirty["total_length"], dirty["length_units"]),
#                 "tail_length": to_mm(dirty["tail_length"], dirty["length_units"]),
#                 # "hind_foot_with_claw": to_mm(
#                 #     dirty["hind_foot_with_claw"], dirty["length_units"]
#                 # ),
#                 "weight": to_grams(dirty["weight"], dirty["weight_units"]),
#                 "lifeStage": dirty["lifestage"],
#                 "reproductiveCondition": dirty["reproductive_data"],
#                 "testis_length": dirty["testes_length"],
#                 "testis_width": dirty["testes_width"],
#                 # "embryo_count": dirty["embryo_count"],
#                 # "embryo_count_side_1": dirty["embryo_count_left"],
#                 # "embryo_count_side_2": dirty["embryo_count_right"],
#                 "embryo_length": dirty["crown_rump_length"],
#                 "placental_scar_count": dirty["scars"],
#                 "unformatted_measurements": dirty["unformatted_measurements"],
#                 "initials": dirty["initials"],
#                 "day": dirty["day"],
#                 "month": dirty["month"],
#                 "year": dirty["year"],
#                 "review_needed": dirty["review_needed"],
#             }
#             clean["hind_foot_length"] = to_mm(
#                 dirty["hind_foot_with_claw"], dirty["length_unit"]
#             )
#             if clean["hind_foot_length"]:
#                 clean["hind_foot_length_includes"] = "claw"
#             set_embryo_counts(
#                 dirty,
#                 clean,
#                 count_label="embryo_count",
#                 left_label="embryo_count_left",
#                 right_label="embryo_count_right",
#             )
#             if dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"
#             clean |= parse_all(dirty["reproductive_data"], clean)
#             clean |= parse_all(dirty["unformatted_measurements"], clean)

#             out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def msb_y1_y2_traits_mod(args: argparse.Namespace) -> None:
#     name = "MSB-Y1-Y2-traits_mod.csv"
#     logging.info(name)

#     columns = [
#       (f"trait name/type {i}", f"measurement {i}", f"units {i}") for i in range(1, 16)
#     ]

#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             clean = {
#                 "occurenceID": dirty["occurenceID"],
#                 "msb_id": dirty["MSBID"],
#                 "catalogNumber": dirty["catalogNumber"],
#                 "scientificName": dirty["scientificName"],
#                 "country": dirty["countryCode"],
#                 "institutionCode": dirty["institutionCode"],
#                 "order": dirty["order"],
#                 "family": dirty["family"],
#                 "genus": dirty["genus"],
#                 "specificEpithet": dirty["specificEpithet"],
#                 "stateProvince": dirty["state/province"],
#                 "county": dirty["County"],
#                 "decimalLatitude": dirty["decLat"],
#                 "decimalLongitude": dirty["decLon"],
#                 "eventDate": dirty["eventDate"],
#                 "day": dirty["day"],
#                 "month": dirty["month"],
#                 "year": dirty["year"],
#                 "occurrenceRemarks": dirty["occurrenceRemarks"],
#                 "dynamicProperties": dirty["dynamicProperties"],
#             }
#             for trait, meas, units in columns:
#                 match dirty[trait].strip():
#                     case "":
#                         pass
#                     case "age":
#                         clean["age"] = dirty[meas]
#                     case "crown-rump length":
#                         clean["embryo_length"] = to_mm(dirty[meas], dirty[units])
#                         clean["embryo_length_measured_from"] = "crown-rump"
#                     case "detected":
#                         clean["detected"] = dirty[meas]
#                     case "ear length from notch" | "ear from notch":
#                         clean["ear_length"] = to_mm(dirty[meas], dirty[units])
#                         clean["ear_length_measured_from"] = "notch"
#                     case "forearm length":
#                         clean["forearm_length"] = to_mm(dirty[meas], dirty[units])
#                     case "hind foot with claw":
#                         clean["hind_foot_length"] = to_mm(dirty[meas], dirty[units])
#                         if clean["hind_foot_length"]:
#                             clean["hind_foot_length_includes"] = "claw"
#                     case "life stage":
#                         clean["lifeStage"] = dirty[meas]
#                     case "reproductive data":
#                         doc = PIPELINE(dirty[meas])
#                         clean |= get_traits(doc)
#                     case "sex":
#                         clean["sex"] = dirty[meas]
#                     case "tail length":
#                         clean["tail_length"] = to_mm(dirty[meas], dirty[units])
#                     case "thumb length with claw":
#                         clean["thumb_length"] = to_mm(dirty[meas], dirty[units])
#                         if clean["thumb_length"]:
#                             clean["thumb_length_measured_from"] = "claw"
#                     case "total length":
#                         clean["total_length"] = to_mm(dirty[meas], dirty[units])
#                     case "tragus length":
#                         clean["tragus_length"] = to_mm(dirty[meas], dirty[units])
#                     case "unformatted measurements":
#                         doc = PIPELINE(dirty[meas])
#                         clean |= get_traits(doc)
#                     case "weight":
#                         clean["body_mass"] = to_grams(dirty[meas], dirty[units])
#                     case _:
#                         logging.error(f"{dirty[trait]=}")
#                         raise ValueError

#             out_data.append(clean)

#     df = pd.DataFrame(out_data)
#     path = args.output_dir / name
#     df.to_csv(path, index=False)


# def microtus_mod(args: argparse.Namespace) -> None:
#     name = "Microtus_mod.csv"
#     logging.info(name)
#     in_name = args.csv_dir / name
#     out_data = []
#     with in_name.open() as in_csv:
#         reader = csv.DictReader(in_csv)
#         for dirty in reader:
#             sci_name = dirty["subspecies"].split()

#             words = dirty["collector number"].split()
#             coll_no = " ".join(w for w in words if re.search(r"\d", w))

#             clean = {
#                 "occurenceID": dirty["occurrenceID"],
#                 "catalogNumber": dirty["guid"],
#                 "catalognumberint": dirty["catalognumberint"],
#                 "scientificName": dirty["subspecies"],
#                 "infraspecificEpithet": sci_name[2] if len(sci_name) > 2 else "",
#                 "recordedBy": dirty["collectors"],
#                 "stateProvince": dirty["state_prov"],
#                 "country": dirty["county"],
#                 "locality": dirty["spec_locality"],
#                 "coll_no": coll_no,
#                 "verbatimEventDate": dirty["verbatim_date"],
#                 "preservedSpecimen": dirty["parts"],
#                 "sex": dirty["sex"],
#                 "total_length": to_mm(dirty["total length"], dirty["unit"]),
#                 "tail_length": to_mm(dirty["tail length"], dirty["unit"]),
#                 # "hind_foot_length": to_mm(
#                 #     dirty["hind foot with claw"], dirty["unit"]
#                 # ),
#                 # "hind_foot_length_includes": "claw",
#                 "body_mass": to_grams(dirty["weight"], dirty["units"]),
#                 "lifeStage": dirty["life stage"],
#                 "reproductiveCondition": dirty["reproductive data"],
#                 "testis_length": dirty["testes L"],
#                 "testis_width": dirty["testes W"],
#                 # "embryo_count": dirty["emb count"],
#                 # "embryo_count_side_1": dirty["embs L"],
#                 # "embryo_count_side_2": dirty["embs R"],
#                 "embryo_length": dirty["emb CR"],
#                 "embryo_length_measured_from": "crown-rump",
#                 "placental_scar_count": dirty["scars"],
#                 "unformatted_measurements": dirty["unformatted measurements"],
#                 "tag_checked": dirty[
#                     "tag checked? (or no tag available), initial here"
#                 ],
#                 "day": dirty["Day"],
#                 "month": dirty["Month"],
#                 "year": dirty["Year"],
#                 "review_needed": dirty["REVIEW NEEDED"],
#             }
#             set_embryo_counts(dirty, clean)

#             hf = dirty["hind foot with claw"], dirty["unit"]
#             clean["hind_foot_length"] = hf
#             if hf:
#                 clean["hind_foot_length_includes"] = "claw"

#             if dirty["ear_length"]:
#                 clean["ear_length"] = to_mm(dirty["earlength"], dirty["unit"])
#                 clean["ear_length_measured_from"] = ""
#             elif dirty["ear_length_from_crown"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_crown"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "crown"
#             elif dirty["ear_from_notch"]:
#                 clean["ear_length"] = to_mm(
#                     dirty["ear_length_from_notch"], dirty["unit"]
#                 )
#                 clean["ear_length_measured_from"] = "notch"

#             out_data.append(clean)


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
