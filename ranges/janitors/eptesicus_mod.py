import re
from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class EptesicusMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("catalogNumber", "catalognumberint")
        self.copy("guid", "GUID")
        self.copy("scientificName", "SUBSPECIES")
        self.copy("count", "COUNTY")
        self.copy("locality", "SPEC_LOCALITY")
        self.copy("stateProvince", "STATE_PROV")
        self.collector()
        self.copy("preservedSpecimen", "PARTS")
        self.copy("sex", "sex")
        self.total_length("total length", "unit")
        self.tail_length("tail length", "unit")
        self.hind_foot_length("hind foot with claw", "unit", includes="claw")
        self.ear_length("ear from notch", "unit", measured_from="notch")
        self.ear_length("ear from crown", "unit", measured_from="crown")
        self.tragus_length("tragus", "unit")
        self.forearm_length("forearm", "unit")
        self.body_mass("weight", "units")
        self.copy("lifeStage", "life stage")
        self.copy("reproductiveCondition", "reproductive data")
        self.copy("unformatted_measurements", "unformatted measurements")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("tag_checked", "tag checked? (or no tag available), initial here")
        self.copy("day", "Day")
        self.copy("month", "Month")
        self.copy("year", "Year")
        self.copy("review_needed", "REVIEW NEEDED")

    def collector(self) -> None:
        words = self.dirty["COLLECTOR_NUMBER"].split()
        self.clean["recordedBy"] = " ".join(w for w in words if not re.search(r"\d", w))
        self.clean["recordNumber"] = " ".join(w for w in words if re.search(r"\d", w))
