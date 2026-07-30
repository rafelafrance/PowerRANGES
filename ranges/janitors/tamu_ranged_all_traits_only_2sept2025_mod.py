from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class TamuRangesAllTraitsOnly2Sept2025Mod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("catalogNumber", "catalogNumber")
        self.copy("scientificName", "ScientificName")
        self.copy("countryCode", "countryCode")
        self.copy("institutionCode", "InstituionCode")
        self.copy("collectionCode", "collectionCode")
        self.clean["total_length"] = self.value_with_units(self.dirty["Total Length"])
        self.clean["tail_length"] = self.value_with_units(self.dirty["Tail Length"])
        self.clean["hind_foot_length"] = self.value_with_units(self.dirty["Hind Foot"])
        self.copy("hind_foot_comment", "Hind Foot Comments")
        self.clean["ear_length"] = self.value_with_units(self.dirty["Ear Length"])
        self.copy("ear_length_comment", "Ear Length Comment")
        self.clean["body_mass"] = self.value_with_units(self.dirty["Weight"])
        self.clean["forearm_length"] = self.value_with_units(
            self.dirty["Forearm Length"]
        )
        self.clean["tragus_length"] = self.value_with_units(self.dirty["Tragus Length"])
        self.copy("reproductiveCondition", "Reproductive Data")
        self.copy("vagina_state", "Vaginal Perforation")
        self.copy("uterus_condition", "Uterus Condition")
        self.copy("pregnancy_state", "Pregnancy")
        self.parse_embryo("Embryo Count")
        self.embryo_count(
            "", "Left Embryo Count", "Right Embryo Count", only_if_filled=True
        )
        self.embryo_length("Embryo Length", only_if_filled=True)
        # self.placental_scars_present("Placental Scars")
        self.placental_scar_count(
            "Placental Scar Count",
            "Left Placental Scar Count",
            "Right Placental Scar Count",
        )
        self.copy("lactation_state", "Lacation")
        self.copy("nipple_size", "Nipple Size")
        self.copy("testis_position", "Testis Position")
        self.testis_length("Testis Length")
        self.testis_width("Testis Width")
        self.copy("lifeStage", "Age Class")
        self.copy("locality", "Locality notes")
        self.copy("eventDate", "Time Of Collection")
        self.copy("ectoparasites", "Ectoparasites")
        self.copy("endoparasites", "Endoparasites")
        self.copy("collectionCode", "CollectionCode")
        self.copy("order", "Order")
        self.copy("family", "Family")
        self.copy("genus", "Genus")
        self.copy("specificEpithet", "Species")
        self.copy("stateProvince", "state")
        self.copy("county", "county")
        self.copy("decimalLatitude", "Latitude")
        self.copy("decimalLongitude", "Longitude")
        self.event_date("coll date")
        self.copy("day", "day")
        self.copy("month", "month")
        self.copy("year", "year")
        self.copy("occurrenceRemarks", "occurrenceRemarks")
        self.copy("dynamicProperties", "dynamicProperties")

        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")
