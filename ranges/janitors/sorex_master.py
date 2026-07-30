from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class SorexMaster(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("mvz_number", "MVZ #")
        self.copy("scientificName", "sci name")
        self.copy("country", "country")
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
        self.testis_width("testis W", "unit")
        self.embryo_count("emb count", "embs L", "embs R")
        self.embryo_length("emb CR", "unit", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("fur", "fur")
        self.copy("attribute_source", "source and date for most attributes")
        self.copy("skin_tag_checked", "skin tag checked? (or no skin tag available)")
        self.copy("catalog_checked", "catalog checked? (or no catalog available)")
        self.copy("library_catalog", "Unnamed: 35")
        self.copy("arctos_uploaded", "data uploaded to Arctos?")
        self.copy(
            "remarks", "remarks (data discrepancy, need to revisit specimen, etc.)"
        )

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_all("remarks")
