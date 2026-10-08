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

        for trait, meas, units in columns:
            self.dirty[trait] = meas
            match self.dirty[trait].strip():
                case "" | "19" | "4129":
                    pass
                case "age":
                    self.copy("age", meas)
                case "age class" | "life stage":
                    self.copy("lifeState", meas)
                case "calcar length":
                    self.calcar_length(meas, units)
                case "curvilinear length":
                    pass
                case "ear length from notch" | "ear from notch":
                    self.ear_length(meas, units, measured_from="notch")
                case "forearm length":
                    self.forearm_length(meas, units)
                case "hind foot with claw":
                    self.hind_foot_length(meas, units, includes="claw")
                case "reproductive data":
                    pass
                case "sex":
                    self.copy("sex", meas)
                case "tarsus length":
                    self.tarsus_length(meas, units)
                case "tail length":
                    self.tail_length(meas, units)
                case "thumb with claw" | "thumb length with claw":
                    self.thumb_length(meas, units, includes="claw")
                case "total length":
                    self.total_length(meas, units)
                case "tragus length":
                    self.tragus_length(meas, units)
                case "weight":
                    self.body_mass(meas, units)
                case _:
                    raise ValueError(f"{self.dirty[trait]=}")
