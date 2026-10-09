from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class LACMRangesSpecimensUpdatedNewDataDec2025(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "scientificName")
        self.copy("sex", "MamSex")
        self.copy("lifeStage", "MamPhyAge_transcribed")

        self.total_length("MamTotalLength", "length_units")
        self.tail_length("MamTailLength", "length_units")
        self.hind_foot_length("MamHindFoot", "length_units")
        self.ear_length("MamEar", "length_units")
        self.body_mass("MamWeight_transcribed", "MamWeight_transcribed_unit")

        self.parse_repro_cond("MamSex", "MamReproductive")
        self.parse_repro_cond("MamSex_transcribed", "MamReprod_transcribed")
        self.parse_all("occurrenceRemarks")
