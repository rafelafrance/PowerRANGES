import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from ranges.janitors.base_janitor import BaseJanitor
from ranges.pylib import pipeline

PIPELINE = pipeline.build()


@dataclass
class UwymzY2Mod(BaseJanitor): ...


def uwymz_y2_mod_multi_row_cleaner(rows: list[dict], _janitor_class: Any) -> list[dict]:
    janitor = UwymzY2Mod()

    cleaned = defaultdict(dict)

    for dirty in rows:
        key = dirty["occurrenceID"]
        cleaned[key]["occurrenceID"] = dirty["occurrenceID"]
        cleaned[key]["scientificName"] = dirty["sciName"]
        cleaned[key]["guid"] = dirty["guid"]
        cleaned[key]["guid_prefix"] = dirty["guid_prefix"]
        cleaned[key]["other_id_type"] = dirty["other_id_type"]
        cleaned[key]["other_id_number"] = dirty["other_id_number"]
        cleaned[key]["uuid"] = dirty["uuid"]
        cleaned[key]["attribute_date"] = dirty["attribute_date"]
        cleaned[key]["attribute_method"] = dirty["attribute_method"]
        cleaned[key]["determiner"] = dirty["attribute_determiner"]
        cleaned[key]["remarks"] = dirty["attribute_remark"]

        value = dirty["attribute_value"]
        units = dirty["attribute_units"]

        match dirty["attribute_type"]:
            case "age":
                cleaned[key]["lifeStage"] = value
            case "attribute_remark":
                cleaned[key]["remarks"] = value
            case "colors":
                cleaned[key]["colors"] = value
            case "ear from notch":
                cleaned[key]["ear_length"] = janitor.to_mm(value, units)
                cleaned[key]["ear_length_measured_from"] = "notch"
            case "forearm length":
                cleaned[key]["forearm_length"] = janitor.to_mm(value, units)
            case "hind foot with claw":
                cleaned[key]["hind_foot_length"] = janitor.to_mm(value, units)
                cleaned[key]["hind_foot_length_includes"] = "claw"
            case "reproductive data":
                doc = PIPELINE(value)
                traits = [e._.trait for e in doc.ents]
                all_ = {}
                for trait in traits:
                    if hasattr(trait, "for_csv"):
                        all_ |= trait.for_csv()
                cleaned[key] |= all_
            case "tail length":
                cleaned[key]["tail_length"] = janitor.to_mm(value, units)
            case "total length":
                cleaned[key]["total_length"] = janitor.to_mm(value, units)
            case "tragus length":
                cleaned[key]["tragus_length"] = janitor.to_mm(value, units)
            case "weight" | "weight¬†":
                cleaned[key]["body_mass"] = janitor.to_grams(value, units)
            case "wing span":
                cleaned[key]["wing_span"] = janitor.to_mm(value, units)
            case _:
                logging.error(f"{dirty['attribute_type']=}")
                raise ValueError

    return list(cleaned.values())
