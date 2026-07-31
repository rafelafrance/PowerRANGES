import logging
from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MsbY1Y2TraitsMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurenceID")
        self.copy("msb_id", "MSBID")
        self.copy("catalogNumber", "catalogNumber")
        self.copy("scientificName", "scientificName")
        self.copy("country", "countryCode")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("order", "order")
        self.copy("family", "family")
        self.copy("genus", "genus")
        self.copy("specificEpithet", "specificEpithet")
        self.copy("stateProvince", "state/province")
        self.copy("county", "County")
        self.copy("decimalLatitude", "decLat")
        self.copy("decimalLongitude", "decLon")
        self.copy("eventDate", "eventDate")
        self.copy("day", "day")
        self.copy("month", "month")
        self.copy("year", "year")
        self.copy("occurrenceRemarks", "occurrenceRemarks")
        self.copy("dynamicProperties", "dynamicProperties")

        self.from_slots()

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_all("unformatted_measurements")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")

    def from_slots(self) -> None:
        columns = [
            (f"trait name/type {i}", f"measurement {i}", f"units {i}")
            for i in range(1, 16)
        ]

        self.clean["sex"] = ""
        self.clean["reproductiveCondition"] = ""
        self.clean["unformatted_measurements"] = ""

        for trait, meas, units in columns:
            match self.dirty[trait].strip():
                case "":
                    pass
                case "age":
                    self.clean["age"] = self.dirty[meas]
                case "crown-rump length":
                    self.clean["embryo_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                    self.clean["embryo_length_measured_from"] = "crown-rump"
                case "detected":
                    self.clean["detected"] = self.dirty[meas]
                case "ear length from notch" | "ear from notch":
                    self.clean["ear_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                    self.clean["ear_length_measured_from"] = "notch"
                case "forearm length":
                    self.clean["forearm_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                case "hind foot with claw":
                    self.clean["hind_foot_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                    if self.clean["hind_foot_length"]:
                        self.clean["hind_foot_length_includes"] = "claw"
                case "life stage":
                    self.clean["lifeStage"] = self.dirty[meas]
                case "reproductive data":
                    self.clean["reproductiveCondition"] = self.dirty[meas]
                case "sex":
                    self.clean["sex"] = self.dirty[meas]
                case "tail length":
                    self.clean["tail_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                case "thumb length with claw":
                    self.clean["thumb_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                    if self.clean["thumb_length"]:
                        self.clean["thumb_length_measured_from"] = "claw"
                case "total length":
                    self.clean["total_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                case "tragus length":
                    self.clean["tragus_length"] = self.to_mm(
                        self.dirty[meas], self.dirty[units]
                    )
                case "unformatted measurements":
                    self.clean["unformatted_measurements"] = self.dirty[meas]
                case "weight":
                    self.clean["body_mass"] = self.to_grams(
                        self.dirty[meas], self.dirty[units]
                    )
                case _:
                    logging.error(f"{self.dirty[trait]=}")
                    raise ValueError
