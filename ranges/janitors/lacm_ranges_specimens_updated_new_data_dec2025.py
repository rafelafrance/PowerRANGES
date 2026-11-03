from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor
from ranges.pylib.flags import EMBRYO


@dataclass
class LACMRangesSpecimensUpdatedNewDataDec2025(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrenceID")
        self.copy("scientificName", "scientificName")
        self.copy("sex", "MamSex")
        self.copy("lifeStage", "MamPhyAge_transcribed")
        self.copy("eventDate", "eventDate")

        self.total_length("MamTotalLength", "length_units")
        self.tail_length("MamTailLength", "length_units")
        self.hind_foot_length("MamHindFoot", "length_units")
        self.ear_length("MamEar", "length_units")
        self.body_mass("MamWeight_transcribed", "MamWeight_transcribed_unit")

        self.parse("MamReproductive", flag=EMBRYO)
        self.parse("MamReprod_transcribed", flag=EMBRYO)
        self.parse("occurrenceRemarks")
        self.parse("MamMeasurements")
