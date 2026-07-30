from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class FmnhTestRangesTraits(BaseJanitor): ...


def fmnh_multi_row_cleaner(rows: list[dict], _janitor_class: Any) -> list[dict]:
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

    janitor = FmnhTestRangesTraits()

    cleaned = defaultdict(dict)

    for dirty in rows:
        key = dirty["occurrenceID"]
        cleaned[key]["occurrenceID"] = dirty["occurrenceID"]
        cleaned[key]["catalogNumber"] = dirty["catalogNumber"]

        cleaned[key]["scientificName"] = dirty["scientificName"]

        cleaned[key]["country"] = dirty["countryCode"]
        cleaned[key]["institutionCode"] = dirty["institutionCode"]

        cleaned[key]["collectionCode"] = dirty["collectionCode"]
        cleaned[key]["order"] = dirty["order"]
        cleaned[key]["family"] = dirty["family"]
        cleaned[key]["genus"] = dirty["genus"]
        cleaned[key]["specificEpithet"] = dirty["specificEpithet"]
        cleaned[key]["stateProvince"] = dirty["state/province"]
        cleaned[key]["county"] = dirty["County"]
        cleaned[key]["decimalLatitude"] = dirty["decLat"]
        cleaned[key]["decimalLongitude"] = dirty["decLon"]

        cleaned[key]["eventDate"] = dirty["eventDate"][:10].removesuffix("-")
        cleaned[key]["day"] = dirty["day"]
        cleaned[key]["month"] = dirty["month"]
        cleaned[key]["year"] = dirty["year"]

        cleaned[key]["occurrenceRemarks"] = dirty["occurrenceRemarks"]
        cleaned[key]["dynamicProperties"] = dirty["dynamicProperties"]

        trait = dirty["trait name/type"].lower().strip()
        if trait:
            trait = spelling[trait]
            cleaned[key][trait] = janitor.to_mm(dirty["measurement"], dirty["units"])

    return list(cleaned.values())
