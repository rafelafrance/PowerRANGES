from dataclasses import dataclass

from ranges.janitors.base import Janitor


@dataclass
class CasY1Y2TraitDataOnly(Janitor):
    def cleaner(self) -> None:
        self.copy("occurrenceID", "occuranceID")
        self.copy("catalogNumber", "catalog#")
        self.copy("scientificName", "scientific name")
        self.copy("countryCode", "country code")
        self.copy("institutionCode", "institution code")
        self.copy("sex", "sex")
        self.copy("lifeStage", "age class")
        self.copy("reproductiveCondition", "reproductive condition")
        self.parse_body_mass("weight")
        self.parse_shorthand("trait data (SL-Tail-Hind Foot-Ear)")
        self.parse_repro_cond("sex", "reproductive condition")
        self.parse_all("other trait remarks")
        self.copy("weight", "weight")
        self.copy("lengths", "trait data (SL-Tail-Hind Foot-Ear)")
        self.copy("remarks", "other trait remarks")
