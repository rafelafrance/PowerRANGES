from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MyotisMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("catalogNumber", "catalognumberint")
        self.copy("guid", "GUID")
        self.copy("binomialName", "SPECIES")
        self.copy("scientificName", "scientific_name")
        self.copy("county", "COUNTY")
        self.copy("locality", "SPEC_LOCALITY")
        self.copy("preservedSpecimen", "PARTS")
        self.copy("stateProvince", "STATE_PROV")
        self.copy("verbatimEventDate", "VERBATIM_DATE")
        self.copy("collectorNumber", "COLLECTOR_NUMBER")
        self.copy("sex", "sex")
        self.total_length("total_length", "unit")
        self.tail_length("tail_length", "unit")
        self.hind_foot_length("hind_foot_with_claw", "unit", "claw")
        self.ear_length("ear_from_notch", "unit", "notch")
        self.ear_length("ear_from_crown", "unit", "crown")
        self.tragus_length("tragus", "unit")
        self.forearm_length("forearm", "unit")
        self.body_mass("weight", "units")
        self.copy("", "lifestage")
        self.copy("", "reproductive data")
        self.copy("", "unformatted measurements")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("", "tag checked? (or no tag available), initial here")
        self.copy("", "Day")
        self.copy("", "Month")
        self.copy("", "Year")
        self.copy("", "REVIEW NEEDED")
