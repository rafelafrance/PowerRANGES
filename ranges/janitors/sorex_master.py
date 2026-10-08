from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class SorexMaster(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "sci name")
        self.copy("sex", "sex")

        self.total_length("total", "unit")
        self.tail_length("tail", "unit")
        self.hind_foot_length("hf", "unit")
        self.ear_length("ear", "unit")
        self.ear_length("Notch", "unit", "notch")
        self.ear_length("Crown", "unit", "crown")
        self.body_mass("wt", "units")
        self.testis_length("testis L", "unit")
        self.testis_width("testis W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")

        self.parse_repro_cond("sex", "repro comments")
        self.parse_all("remarks (data discrepancy, need to revisit specimen, etc.)")
