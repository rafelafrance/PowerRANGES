from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class CsulbSciuridaeTraits(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "scientificName")
        self.copy("sex", "sex")
        self.copy("lifeStage", "age_class")

        self.total_length("tot_length", "length_units")
        self.hind_foot_length("hind_foot_length", "length_units")
        self.hind_foot_length("ear_length", "length_units")
        self.body_mass("weight", "weight_units")

        self.parse_repro_cond("sex", "repro")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")
