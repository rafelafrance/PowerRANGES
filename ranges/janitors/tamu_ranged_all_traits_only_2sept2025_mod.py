from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor
from ranges.pylib.flags import EMBRYO


@dataclass
class TamuRangesAllTraitsOnly2Sept2025Mod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "ScientificName")
        self.copy("vagina_state", "Vaginal Perforation")
        self.copy("uterus_condition", "Uterus Condition")
        self.copy("pregnancy_state", "Pregnancy")
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

        self.parse("Reproductive Data", flag=EMBRYO)
        self.parse("occurrenceRemarks")
        self.parse("dynamicProperties")
        self.parse("Embryo Count", prefix="embryo")
        self.parse("Embryo Length", prefix="embryo")
        self.parse("Placental Scars", prefix="placental scars")
        self.parse("Testis Position", prefix="testis")
        self.parse("Testis Length", prefix="testis")
        self.parse("Testis Width", prefix="testis")
