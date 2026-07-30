from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class CsulbSciuridaeTraits(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("catalogNumber", "catalogNumber")
        self.copy("scientificName", "scientificName")
        self.copy("countryCode", "countryCode")
        self.copy("institutionCode", "institutionCode")
        self.copy("sex", "sex")
        self.copy("lifeStage", "age_class")
        self.total_length("tot_length", "length_units")
        self.hind_foot_length("hind_foot_length", "length_units")
        self.hind_foot_length("ear_length", "length_units")
        self.body_mass("weight", "weight_units")
        self.copy("reproductiveCondition", "repro")
        self.copy("collectionCode", "collectionCode")
        self.copy("order", "order")
        self.copy("family", "family")
        self.copy("genus", "genus")
        self.copy("specificEpithet", "specificEpithet")
        self.copy("stateProvince", "stateProvince")
        self.copy("county", "County")
        self.copy("decimalLatitude", "decLat")
        self.copy("decimalLongitude", "decLon")
        self.event_date("eventDate")
        self.copy("day", "day")
        self.copy("month", "month")
        self.copy("year", "year")
        self.copy("occurrenceRemarks", "occurrenceRemarks")
        self.copy("dynamicProperties", "dynamicProperties")

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")
