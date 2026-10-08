from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class TamuRangesAllTraitsOnly2Sept2025Mod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "ScientificName")
        self.copy("vagina_state", "Vaginal Perforation")
        self.copy("uterus_condition", "Uterus Condition")
        self.copy("pregnancy_state", "Pregnancy")
        self.copy("embryo_count_raw", "Embryo Count")
        self.copy("lactation_state", "Lacation")
        self.copy("nipple_size", "Nipple Size")
        self.copy("testis_position", "Testis Position")
        self.copy("lifeStage", "Age Class")

        self.clean["total_length"] = self.value_with_units(self.dirty["Total Length"])
        self.clean["tail_length"] = self.value_with_units(self.dirty["Tail Length"])
        self.clean["hind_foot_length"] = self.value_with_units(self.dirty["Hind Foot"])
        self.clean["ear_length"] = self.value_with_units(self.dirty["Ear Length"])
        self.clean["body_mass"] = self.value_with_units(self.dirty["Weight"])
        self.clean["forearm_length"] = self.value_with_units(
            self.dirty["Forearm Length"]
        )
        self.clean["tragus_length"] = self.value_with_units(self.dirty["Tragus Length"])
        self.clean["embryo_length"] = self.value_with_units(self.dirty["Embryo Length"])

        self.placental_scar_count(
            "Placental Scar Count",
            "Left Placental Scar Count",
            "Right Placental Scar Count",
        )
        self.testis_length("Testis Length")
        self.testis_width("Testis Width")

        self.parse_repro_cond("sex", "Reproductive Data")
        self.parse_embryo("embryo_count_raw")
        self.parse_all("occurrenceRemarks")
        self.parse_all("dynamicProperties")
