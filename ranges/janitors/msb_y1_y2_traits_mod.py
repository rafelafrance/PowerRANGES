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
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")

    def from_slots(self) -> None:
        columns = [
            (f"trait name/type {i}", f"measurement {i}", f"units {i}")
            for i in range(1, 16)
        ]

        self.dirty["sex"] = ""
        self.dirty["reproductive data"] = ""
        self.dirty["unformatted measurements"] = ""

        for trait_col, meas_col, units_col in columns:
            trait = self.dirty[trait_col].strip()
            meas = self.dirty[meas_col]
            # units = self.dirty[units_col].strip()
            if not trait:
                continue
            # print(f"{trait=} {meas=} {units=}")
            self.dirty[trait] = meas
            match trait:
                case "":
                    pass
                case "age":
                    self.clean["age"] = self.dirty[meas_col]
                case "crown-rump length":
                    self.clean["embryo_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                    self.clean["embryo_length_measured_from"] = "crown-rump"
                case "detected":
                    pass
                case "ear length from notch" | "ear from notch":
                    self.clean["ear_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                    self.clean["ear_length_measured_from"] = "notch"
                case "forearm length":
                    self.clean["forearm_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                case "hind foot with claw":
                    self.clean["hind_foot_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                    if self.clean["hind_foot_length"]:
                        self.clean["hind_foot_length_includes"] = "claw"
                case "life stage":
                    self.clean["lifeStage"] = self.dirty[meas_col]
                case "reproductive data":
                    pass
                case "sex":
                    self.clean["sex"] = self.dirty[meas_col]
                case "tail length":
                    self.clean["tail_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                case "thumb length with claw":
                    self.clean["thumb_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                    if self.clean["thumb_length"]:
                        self.clean["thumb_length_measured_from"] = "claw"
                case "total length":
                    self.clean["total_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                case "tragus length":
                    self.clean["tragus_length"] = self.to_mm(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                case "unformatted measurements":
                    pass
                case "weight":
                    self.clean["body_mass"] = self.to_grams(
                        self.dirty[meas_col], self.dirty[units_col]
                    )
                case _:
                    logging.error(f"{self.dirty[trait_col]=}")
                    raise ValueError
