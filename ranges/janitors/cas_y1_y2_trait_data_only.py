from dataclasses import dataclass

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class CasY1Y2TraitDataOnly(BaseJanitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occuranceID")
        self.copy("catalogNumber", "catalog#")
        self.copy("scientificName", "scientific name")
        self.copy("countryCode", "country code")
        self.copy("institutionCode", "institution code")
        self.copy("sex", "sex")
        self.copy("lifeStage", "age class")
        self.copy("reproductiveCondition", "reproductive condition")
        self.copy("weight", "weight")
        self.copy("lengths", "trait data (SL-Tail-Hind Foot-Ear)")
        self.copy("remarks", "other trait remarks")

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_body_mass("weight")
        self.parse_shorthand("lengths")
        self.parse_all("remarks")
