import json
from dataclasses import dataclass, field

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class UwbmMammJsonAttributes(BaseJanitor):
    gonad_length_count: int = 0
    gonad_width_count: int = 0
    gonad: dict = field(default_factory=dict)

    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrence_id")
        self.copy("scientificName", "scientific_name")

        self.attribute_detail()
        self.gonad_adjustment()

        self.parse_repro_cond("sex", "reproductive data")
        self.parse_all("unformatted measurements")

    def attribute_detail(self) -> None:
        self.dirty["sex"] = ""
        self.dirty["reproductive data"] = ""
        self.dirty["unformatted measurements"] = ""

        detail = self.dirty["attributedetail"]
        if not detail:
            return
        attrs = json.loads(detail)

        ear_length_count = 0
        for attr in attrs:
            trait = attr["attribute_type"]
            value = attr["attribute_value"]
            units = attr["attribute_units"]
            self.dirty[trait] = value

            match trait:
                case "age":
                    self.clean["age"] = value
                case "antler points":
                    pass
                case "associated species":
                    pass
                case "body condition":
                    pass
                case "colors":
                    self.clean["colors"] = value
                case "detected":
                    pass
                case "ear from crown":
                    key = "ear_length"
                    key2 = "ear_length_measured_from"
                    if ear_length_count:
                        key = f"ear_length_{ear_length_count}"
                        key2 = f"ear_length_measured_from_{ear_length_count}"
                    self.clean[key] = self.to_mm(value, units)
                    self.clean[key2] = "crown"
                    ear_length_count += 1
                case "ear from notch":
                    key = "ear_length"
                    key2 = "ear_length_measured_from"
                    if ear_length_count:
                        key = f"ear_length_{ear_length_count}"
                        key2 = f"ear_length_measured_from_{ear_length_count}"
                    self.clean[key] = self.to_mm(value, units)
                    self.clean[key2] = "notch"
                    ear_length_count += 1
                case "examined for":
                    pass
                case "fat deposition":
                    pass
                case "forearm length":
                    self.clean["forearm_length"] = self.to_mm(value, units)
                case "gonad length":
                    self.gonad_length_count += 1
                    key = "gonad_length"
                    if self.gonad_length_count > 1:
                        key = f"gonad_length_{self.gonad_length_count}"
                    self.gonad[key] = self.to_mm(value, units)
                case "gonad width":
                    self.gonad_width_count += 1
                    key = "gonad_width"
                    if self.gonad_width_count > 1:
                        key = f"gonad_width_{self.gonad_width_count}"
                    self.gonad[key] = self.to_mm(value, units)
                case "hind foot with claw":
                    self.clean["hind_foot_length"] = self.to_mm(value, units)
                    self.clean["hind_foot_length_includes"] = "claw"
                case "life stage":
                    self.clean["lifeStage"] = value
                case "molt condition":
                    pass
                case "not detected":
                    pass
                case "numeric age":
                    self.clean["numeric_age"] = value
                case "processing history":
                    pass
                case "reproductive data":
                    pass
                case "sex":
                    self.clean["sex"] = value
                case "stomach contents":
                    pass
                case "tail length":
                    self.clean["tail_length"] = self.to_mm(value, units)
                case "tooth length":
                    self.clean["tooth_length"] = self.to_mm(value, units)
                case "total length":
                    self.clean["total_length"] = self.to_mm(value, units)
                case "tragus length":
                    self.clean["tragus_length"] = self.to_mm(value, units)
                case "unformatted measurements":
                    pass
                case "verbatim agent":
                    pass
                case "verbatim attribute":
                    pass
                case "verbatim preservation date":
                    pass
                case "weight":
                    self.clean["body_mass"] = self.to_grams(value, units)
                case "wing span":
                    self.clean["wing_span"] = self.to_mm(value, units)
                case _:
                    raise ValueError(attr["attribute_type"])

    def gonad_adjustment(self) -> None:
        sex = self.clean.get("sex", "").lower()
        male = sex.startswith("m")
        female = sex.startswith("f")
        length = self.gonad.get("gonad_length", "")
        length2 = self.gonad.get("gonad_length_2", "")
        width = self.gonad.get("gonad_width", "")
        width2 = self.gonad.get("gonad_width_2", "")
        if length and (male or female):
            key = "testis_length" if male else "ovary_length"
            self.clean[key] = length
        if length2 and (male or female):
            key = "testis_length_2" if male else "ovary_length_2"
            self.clean[key] = length2
        if width and (male or female):
            key = "testis_width" if male else "ovary_width"
            self.clean[key] = width
        if width2 and (male or female):
            key = "testis_width_2" if male else "ovary_width_2"
            self.clean[key] = width2
