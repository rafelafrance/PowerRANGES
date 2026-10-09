from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class DmnsRangesTraits(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "scientificName")

        self.variable_traits()

        self.parse_repro_cond("sex", "reproductive data")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")

    def variable_traits(self) -> None:
        columns = [
            ("trait name/type", "measurement", "units"),
            ("trait name/type2", "measurement2", "units2"),
            ("trait name/type3", "measurement3", "units3"),
            ("trait name/type4", "measurement4", "units4"),
        ]

        self.dirty["sex"] = ""
        self.dirty["reproductive data"] = ""

        for trait_col, meas_col, units_col in columns:
            trait = self.dirty[trait_col].strip()
            meas = self.dirty[meas_col]
            # units = self.dirty[units_col].strip()
            if not trait:
                continue
            # print(f"{trait=} {meas=} {units=}")
            self.dirty[trait] = meas
            match trait:
                case "" | "19" | "4129":
                    pass
                case "age":
                    self.copy("age", meas_col)
                case "age class" | "life stage":
                    self.copy("lifeStage", meas_col)
                case "calcar length":
                    self.calcar_length(meas_col, units_col)
                case "curvilinear length":
                    pass
                case "ear length from notch" | "ear from notch":
                    self.ear_length(meas_col, units_col, measured_from="notch")
                case "forearm length":
                    self.forearm_length(meas_col, units_col)
                case "hind foot with claw":
                    self.hind_foot_length(meas_col, units_col, includes="claw")
                case "reproductive data":
                    pass
                case "sex":
                    self.copy("sex", meas_col)
                case "tarsus length":
                    self.tarsus_length(meas_col, units_col)
                case "tail length":
                    self.tail_length(meas_col, units_col)
                case "thumb with claw" | "thumb length with claw":
                    self.thumb_length(meas_col, units_col, includes="claw")
                case "total length":
                    self.total_length(meas_col, units_col)
                case "tragus length":
                    self.tragus_length(meas_col, units_col)
                case "weight":
                    self.body_mass(meas_col, units_col)
                case "trait name/type" | "measurement" | "units":
                    pass
                case "trait name/type2" | "measurement2" | "units2":
                    pass
                case "trait name/type3" | "measurement3" | "units3":
                    pass
                case "trait name/type4" | "measurement4" | "units4":
                    pass
                case _:
                    raise ValueError(f"{self.dirty[trait]=}")
