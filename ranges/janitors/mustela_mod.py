from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class MustelaMod(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("institutionCode", "institutionCode")
        self.copy("collectionCode", "collectionCode")
        self.copy("mvz_num", "mvz_num")
        self.copy("subspecies", "subspecies")
        self.copy("recordedBy", "collectors")
        self.copy("country", "collectors")
        self.copy("stateProvince", "state_prov")
        self.copy("county", "county")
        self.copy("locality", "spec_locality")
        self.copy("eventDate", "ended_date")
        self.copy("preservedSpecimen", "parts")
        self.total_length("total_length", "length_units")
        self.tail_length("tail_length", "length_units")
        self.hind_foot_length("hind_foot_with_claw", "length_units", "claw")
        self.ear_length("ear_from_notch", "length_units", "notch")
        self.ear_length("ear_from_crown", "length_units", "crown")
        self.body_mass("weight", "weight_units")
        self.copy("lifeStage", "lifestage")
        self.copy("reproductiveCondition", "reproductive_data")
        self.testis_length("testes_length", "length_units")
        self.testis_width("testes_width", "length_units")
        self.embryo_count("embryo_count", "embryo_count_left", "embryo_count_right")
        self.embryo_length("crown_rump_length", "length_units", "crown-rump")
        self.placental_scar_count("scars")
        self.copy("unformatted_measurements", "unformatted_measurements")
        self.copy("initials", "initials")
        self.copy("day", "day")
        self.copy("month", "month")
        self.copy("year", "year")
        self.copy("review_needed", "review_needed")
