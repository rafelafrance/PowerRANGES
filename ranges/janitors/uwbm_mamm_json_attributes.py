import json
from dataclasses import dataclass, field

from ranges.janitors.base_janitor import BaseJanitor


@dataclass
class UwbmMammJsonAttributes(BaseJanitor):
    gonad_length_count: int = 0
    gonad_width_count: int = 0
    gonad: dict = field(default_factory=dict)

    def attribute_detail(self) -> None:
        detail = self.dirty["attributedetail"]
        if not detail:
            return
        attrs = json.loads(detail)
        for attr in attrs:
            ear_length_count = 0
            value = attr["attribute_value"]
            units = attr["attribute_units"]
            match attr["attribute_type"]:
                case "age":
                    self.clean["age"] = value
                case "antler points":
                    self.clean["antler_points"] = value
                case "associated species":
                    self.clean["associatedSpecies"] = value
                case "body condition":
                    self.clean["body_condition"] = value
                case "colors":
                    self.clean["colors"] = value
                case "detected":
                    self.clean["detected"] = value
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
                    self.clean["examined_for"] = value
                case "fat deposition":
                    self.clean["fat_deposition"] = value
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
                    self.clean["molt_condition"] = value
                case "not detected":
                    self.clean["not_detected"] = value
                    self.clean["not_detected_method"] = attr["attribute_method"]
                case "numeric age":
                    self.clean["numeric_age"] = value
                case "processing history":
                    self.clean["processing_history"] = value
                case "reproductive data":
                    self.clean["reproductive_condition"] = value
                case "sex":
                    self.clean["sex"] = value
                case "stomach contents":
                    self.clean["stomach_contents"] = value
                case "tail length":
                    self.clean["tail_length"] = self.to_mm(value, units)
                case "tooth length":
                    self.clean["tooth_length"] = self.to_mm(value, units)
                case "total length":
                    self.clean["total_length"] = self.to_mm(value, units)
                case "tragus length":
                    self.clean["tragus_length"] = self.to_mm(value, units)
                case "unformatted measurements":
                    self.clean["unformatted_measurements"] = value
                case "verbatim agent":
                    self.clean["verbatim_agent"] = value
                    self.clean["verbatim_agent_method"] = attr["attribute_method"]
                    self.clean["verbatim_agent_remark"] = attr["attribute_remark"]
                case "verbatim attribute":
                    self.clean["verbatim_attribute"] = value
                case "verbatim preservation date":
                    self.clean["verbatim_preservation_date"] = value
                    self.clean["verbatim_preservation_date_method"] = attr[
                        "attribute_method"
                    ]
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

    def cleaner(self) -> None:
        self.copy("occurrenceID", "occurrence_id")
        self.copy("license", "use_license_url")
        self.copy("collectionID", "collection_object_id")
        self.copy("catalogNumber", "catalog_number")
        self.copy("scientificName", "scientific_name")
        self.copy("country", "country")
        self.copy("stateProvince", "state_prov")
        self.copy("county", "county")

        self.attribute_detail()
        self.gonad_adjustment()

        self.parse_repro_cond("sex", "reproductiveCondition")
        self.parse_all("unformatted_measurements")
