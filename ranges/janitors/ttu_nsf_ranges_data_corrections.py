from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class TtunsfRangesDataCorrections(BaseJanitor):
    @staticmethod
    def trim_date(value: str) -> str:
        return value.removesuffix("00:00:00").strip()

    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("sex", "SEX")
        self.copy("lifeStage", "AGE")
        self.copy("pregnancy_state", "Pregnant")
        self.copy("lactation_state", "Lactation")

        self.total_length("TOTAL")
        self.tail_length("TAIL")
        self.hind_foot_length("FOOT")
        self.ear_length("EAR")
        self.body_mass("WEIGHT")
        self.tragus_length("TRAGUS")
        self.forearm_length("FOREARM")
        self.embryo_count("EmbryoCount")
        self.parse_placental_scar_count("Scars")
        self.parse_embryo("EmbryoMeasures")

        self.parse_repro_cond("sex", "ReproductiveCondition_Reprocond")
        self.parse_repro_cond("sex", "ReproComments")
        self.parse_all("Non_ReproComments")
