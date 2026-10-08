from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class PeromyscusMaster(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "subspecies")
        self.copy("sex", "sex")

        self.total_length("total length", "unit")
        self.tail_length("tail length", "unit")
        self.hind_foot_length("hind foot with claw", "unit", "claw")
        self.ear_length("ear", "unit")
        self.ear_length("ear from notch", "unit", "notch")
        self.ear_length("ear from crown", "unit", "crown")
        self.body_mass("weight", "units")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")

        self.parse_repro_cond("sex", "reproductive data")
        self.parse_all("unformatted measurements")
