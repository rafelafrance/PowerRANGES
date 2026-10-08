from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MyotisMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "scientific_name")
        self.copy("sex", "sex")
        self.copy("lifeStage", "lifestage")

        self.total_length("total_length", "unit")
        self.tail_length("tail_length", "unit")
        self.hind_foot_length("hind_foot_with_claw", "unit", "claw")
        self.ear_length("ear_from_notch", "unit", "notch")
        self.ear_length("ear_from_crown", "unit", "crown")
        self.tragus_length("tragus", "unit")
        self.forearm_length("forearm", "unit")
        self.body_mass("weight", "units")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")

        self.parse_repro_cond("sex", "reproductive data")
        self.parse_all("unformatted_measurements")
