import re
from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class EptesicusMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "SUBSPECIES")
        self.copy("sex", "sex")
        self.copy("lifeStage", "life stage")

        self.total_length("total length", "unit")
        self.tail_length("tail length", "unit")
        self.hind_foot_length("hind foot with claw", "unit", includes="claw")
        self.ear_length("ear from notch", "unit", measured_from="notch")
        self.ear_length("ear from crown", "unit", measured_from="crown")
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

    def collector(self) -> None:
        words = self.dirty["COLLECTOR_NUMBER"].split()
        self.clean["recordedBy"] = " ".join(w for w in words if not re.search(r"\d", w))
        self.clean["recordNumber"] = " ".join(w for w in words if re.search(r"\d", w))
