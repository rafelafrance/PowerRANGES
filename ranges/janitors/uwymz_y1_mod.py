import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from ranges.janitors.base import Janitor
from ranges.pylib import pipeline

PIPELINE = pipeline.build()


@dataclass
class UwymzY1Mod(Janitor): ...


def uwymz_y1_mod_multi_row_cleaner(rows: list[dict], _janitor_class: Any) -> list[dict]:
    janitor = UwymzY1Mod()

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
        cleaned[key]["attribute_meth"] = dirty["attribute_meth"]
        cleaned[key]["determiner"] = dirty["determiner"]
        cleaned[key]["remarks"] = dirty["remarks"]

        value = dirty["attribute_value"]
        units = dirty["attribute_units"]

        match dirty["attribute"]:
            case "":
                pass
            case "ear from notch":
                cleaned[key]["ear_length"] = janitor.to_mm(value, units)
                cleaned[key]["ear_length_measured_from"] = "notch"
            case "hind foot with claw" | "hind foot with tail":
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
            case "weight":
                cleaned[key]["body_mass"] = janitor.to_grams(value, units)
            case _:
                logging.error(f"{dirty['attribute']=}")
                raise ValueError

    return list(cleaned.values())
