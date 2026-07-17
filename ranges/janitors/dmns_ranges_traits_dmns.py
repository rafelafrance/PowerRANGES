import logging
from dataclasses import dataclass

from ranges.janitors.base import Janitor


@dataclass
class DmnsRangesTraits(Janitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("dmnsID", "DMNSID")
        self.copy("catalogNumber", "catalogNumber")
        self.copy("scientificName", "scientificName")
        self.copy("countryCode", "countryCode")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("collectionCode_1", "collectionCode.1")
        self.copy("order", "order")
        self.copy("family", "family")
        self.copy("genus", "genus")
        self.copy("specificEpithet", "specificEpithet")
        self.copy("stateProvince", "state/province")
        self.copy("county", "County")
        self.copy("decimalLatitude", "decLat")
        self.copy("decimalLongitude", "decLon")
        self.event_date("eventDate")
        self.copy("day", "day")
        self.copy("month", "month")
        self.copy("year", "year")
        self.copy("occurrenceRemarks", "occurrenceRemarks")
        self.copy("dynamicProperties", "dynamicProperties")
        self.variable_traits()

    def variable_traits(self) -> None:
        columns = [
            ("trait name/type", "measurement", "units"),
            ("trait name/type2", "measurement2", "units2"),
            ("trait name/type3", "measurement3", "units3"),
            ("trait name/type4", "measurement4", "units4"),
        ]

        for trait, meas, units in columns:
            match self.dirty[trait].strip():
                case "":
                    pass
                case "age":
                    self.copy("age", meas)
                case "age class":
                    self.copy("lifeState", meas)
                case "calcar length":
                    self.calcar_length(meas, units)
                case "ear length from notch" | "ear from notch":
                    self.ear_length(meas, units, measured_from="notch")
                case "hind foot with claw":
                    self.hind_foot_length(meas, units, includes="claw")
                case "reproductive data":
                    self.parse_all(self.dirty[trait])
                case "sex":
                    self.copy("sex", meas)
                case "tarsus length":
                    self.tarsus_length(meas, units)
                case "tail length":
                    self.tail_length(meas, units)
                case "thumb with claw":
                    self.thumb_length(meas, units)
                case "total length":
                    self.total_length(meas, units)
                case "tragus length":
                    self.tragus_length(meas, units)
                case "weight":
                    self.body_mass(meas, units)
                case _:
                    logging.error(f"{self.dirty[trait]=}")
                    raise ValueError
