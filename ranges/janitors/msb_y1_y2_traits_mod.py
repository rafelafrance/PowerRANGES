import logging
from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MsbY1Y2TraitsMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurenceID")
        self.copy("scientificName", "scientificName")

        self.from_slots()

        self.parse_repro_cond("sex", "reproductive data")
        self.parse_all("unformatted_measurements")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")

    def from_slots(self) -> None:
        columns = [
            (f"trait name/type {i}", f"measurement {i}", f"units {i}")
            for i in range(1, 16)
        ]

        self.data["sex"] = ""
        self.data["reproductive data"] = ""
        self.data["unformatted_measurements"] = ""

        for trait, meas, units in columns:
            self.dirty[trait] = meas
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
                    pass
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
                    pass
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
                    pass
                case "weight":
                    self.clean["body_mass"] = self.to_grams(
                        self.dirty[meas], self.dirty[units]
                    )
                case _:
                    logging.error(f"{self.dirty[trait]=}")
                    raise ValueError
