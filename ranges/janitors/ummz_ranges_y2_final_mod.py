from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class UmmzRangesY2FinalMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("index", "index")
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "InstitutionCode")
        self.copy("division", "division")
        self.copy("catalogueNumber", "catalogueNumber")
        self.copy("countryCode", "countryCode")
        self.copy("state", "state")
        self.copy("locality", "locality")
        self.copy("order", "order")
        self.copy("family", "family")
        self.copy("genus", "genus")
        self.copy("specificEpithet", "species")
        self.copy("infraspecificEpithet", "subspecies")
        self.copy("sex", "sex")
        self.total_length("totalLength", "lengthUnits")
        self.ear_length("earLength", "lengthUnits")
        self.forearm_length("forearmLength", "lengthUnits")
        self.hind_foot_length("hindfootLength", "lengthUnits")
        self.tail_length("tailLength", "lengthUnits")
        self.tragus_length("tragusLength", "lengthUnits")
        self.body_mass("weight", "weightUnits")
        self.copy("reproductiveCondition", "reproductiveData")
        self.copy("verbatim_data", "verbatim_data")
        self.copy("lifeStage", "ageClass")
        self.copy("additional_comments", "addl_comments")
        self.ear_length("earFromCrown", "lengthUnits", "crown")
        self.ear_length("earFromNotch", "lengthUnits", "notch")
        self.embryo_count("embryoCount")
        self.copy("lactation_state", "lactation")
        self.copy("pregnancy_state", "pregnancy")
        self.thumb_length("thumbLengthWithClaw", "lengthUnits", "claw")
        self.clean["wing_span"] = self.value_with_units(self.dirty["wingSpan"])

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_all("additional_comments")
