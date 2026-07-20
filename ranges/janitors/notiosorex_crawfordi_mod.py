from dataclasses import dataclass

from ranges.janitors.base import Janitor


@dataclass
class NotiosorexCrawfordiMod(Janitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("mvz_number", "MVZ #")
        self.copy("scientificName", "sci name")
        self.copy("stateProvince", "state")
        self.copy("county", "county")
        self.copy("locality", "specific")
        self.copy("recordedBy", "collector")
        self.copy("recordNumber", "coll #")
        self.copy("eventDate", "date")
        self.copy("sex", "sex")
        self.copy("parts", "parts")
        self.total_length("total", "unit")
        self.tail_length("tail", "unit")
        self.hind_foot_length("hf", "unit")
        self.ear_length("ear", "unit")
        self.ear_length("Notch", "unit", "notch")
        self.ear_length("Crown", "unit", "crown")
        self.body_mass("wt", "units")
        self.copy("reproductiveCondition", "repro comments")
        self.testis_length("testis L", "unit")
        self.testis_length("testis R", "unit")
        self.embryo_count("", "embs L", "embs R")
        self.placental_scar_count("scars")
        self.copy("source_and_date", "source and date for most attributes")
        self.copy("skin_tag_checked", "skin tag checked? (or no skin tag available)")
        self.copy("catalog_checked", "catalog checked? (or no catalog available)")
        self.copy("unnamed", "Unnamed: 31")
        self.copy("arctos_upload", "data uploaded to Arctos?")
        self.copy("review_needed", "REVIEW NEEDED")
