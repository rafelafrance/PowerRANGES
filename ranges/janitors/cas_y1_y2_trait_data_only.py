from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class CasY1Y2TraitDataOnly(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occuranceID")
        self.copy("scientificName", "scientific name")
        self.copy("sex", "sex")
        self.copy("lifeStage", "age class")

        self.parse_repro_cond("sex", "reproductive condition")
        self.parse_body_mass("weight")
        self.parse_shorthand("trait data (SL-Tail-Hind Foot-Ear)")
        self.parse_all("other trait remarks")
