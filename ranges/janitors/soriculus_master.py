from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class SoriculusMaster(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("catalogNumber", "catalognumberint")
        self.copy("scientificName", "scientific_name")
        self.copy("stateProvince", "state_prov")
        self.copy("county", "county")
        self.copy("locality", "spec_locality")
        self.copy("recordedBy", "collectors")
        self.copy("other_catalog_numbers", "othercatalognumbers")
        self.copy("eventDate", "ended_date")
        self.copy("sex", "sex")
        self.copy("preservedSpecimen", "parts")
        self.total_length("total", "unit")
        self.tail_length("tail", "unit")
        self.hind_foot_length("hf", "unit")
        self.ear_length("ear", "unit")
        self.ear_length("Notch", "unit", "notch")
        self.ear_length("Crown", "unit", "crown")
        self.body_mass("wt", "units")
        self.copy("reproductiveCondition", "repro comments")
        self.testis_length("testes L", "unit")
        self.testis_width("testes W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("attribute_source", "source and date for most attributes")
        self.copy("skin_tag_checked", "skin tag checked? (or no skin tag available)")
        self.copy("catalog_checked", "catalog checked? (or no catalog available)")
        self.copy("catalog_status", "Unnamed: 33")
        self.copy("unformatted_measurements", "unformatted measurements")
        self.copy("review_needed", "REVIEW NEEDED")
