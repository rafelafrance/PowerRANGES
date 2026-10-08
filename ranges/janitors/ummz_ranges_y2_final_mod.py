from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class UmmzRangesY2FinalMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("sex", "sex")
        self.copy("lifeStage", "ageClass")
        self.copy("lactation_state", "lactation")
        self.copy("pregnancy_state", "pregnancy")

        self.total_length("totalLength", "lengthUnits")
        self.ear_length("earLength", "lengthUnits")
        self.forearm_length("forearmLength", "lengthUnits")
        self.hind_foot_length("hindfootLength", "lengthUnits")
        self.tail_length("tailLength", "lengthUnits")
        self.tragus_length("tragusLength", "lengthUnits")
        self.body_mass("weight", "weightUnits")
        self.ear_length("earFromCrown", "lengthUnits", "crown")
        self.ear_length("earFromNotch", "lengthUnits", "notch")
        self.embryo_count("embryoCount")
        self.thumb_length("thumbLengthWithClaw", "lengthUnits", "claw")

        self.parse_repro_cond("sex", "reproductiveData")
        self.parse_all("addl_comments")
