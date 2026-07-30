from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class NeotomaMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("guid", "guid")
        self.copy("catalogNumber", "catalognumberint")
        self.copy("scientificName", "subspecies")
        self.copy("recordedBy", "collectors")
        self.copy("stateProvince", "state_prov")
        self.copy("count", "county")
        self.copy("locality", "spec_locality")
        self.copy("recordNumber", "collector number")
        self.copy("verbatimEventDate", "verbatim_date")
        self.copy("preservedSpecimen", "parts")
        self.copy("sex", "sex")
        self.total_length("total length", "unit")
        self.tail_length("tail length", "unit")
        self.hind_foot_length("hind foot with claw", "unit", "claw")
        self.ear_length("ear", "unit")
        self.ear_length("ear from notch", "unit", "notch")
        self.ear_length("ear from crown", "unit", "crown")
        self.body_mass("weight", "units")
        self.copy("lifeStage", "Unnamed: 21")
        self.copy("reproductiveCondition", "reproductive data")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("unformatted_measurements", "unformatted measurements")
        self.copy("tag_checked", "tag checked? (or no tag available), initial here")
        self.copy("day", "Day")
        self.copy("month", "Month")
        self.copy("year", "Year")
        self.copy("review_needed", "REVIEW NEEDED")
