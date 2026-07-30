from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MyosorexVariusMod(BaseJanitor):
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
        self.copy("preservedSpecimen", "parts")
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
        self.embryo_count("emb count", "embs L", "embs R")
        self.placental_scar_count("scars")
        self.copy("attribute_source", "source and date for most attributes")
        self.copy("skin_tag_checked", "skin tag checked? (or no skin tag available)")
        self.copy("catalog_checked", "catalog checked? (or no catalog available)")
        self.copy("fieldNotes", "Unnamed: 32")
        self.copy("uploaded_to_arctos", "data uploaded to Arctos?")
        self.copy(
            "occurrenceRemarks",
            "remarks (data discrepancy, need to revisit specimen, etc.)",
        )
