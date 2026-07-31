import re
from dataclasses import dataclass, field
from typing import Any

from spacy.tokens import Doc

from ranges.pylib import pipeline

INT = re.compile(r"\d+")
FLOAT = re.compile(r" \d+ (?: \.\d* )? | \.\d+", flags=re.VERBOSE)
FRACT = re.compile(r" (\d*) \s+ (\d+ / \d+) ", flags=re.VERBOSE)
UNITS = {
    # Length
    "c.m.": 10.0,
    "centimeters": 10.0,
    "cm": 10.0,
    "cm.": 10.0,
    "cm.s": 10.0,
    "cms": 10.0,
    "'": 304.8,
    "feet": 304.8,
    "foot": 304.8,
    "ft": 304.8,
    "ft.": 304.8,
    '"': 25.4,
    "in": 25.4,
    "in.": 25.4,
    "inch": 25.4,
    "inches": 25.4,
    "ins": 25.4,
    "meter": 1000.0,
    "meters": 1000.0,
    # Mass
    "kg": 1000.0,
    "kg.": 1000.0,
    "kgs": 1000.0,
    "kgs.": 1000.0,
    "kilograms": 1000.0,
    "lb": 453.5924,
    "lb.": 453.5924,
    "lbs": 453.5924,
    "lbs.": 453.5924,
    "mg": 0.001,
    "mg.": 0.001,
    "mgs.": 0.001,
    "mgs": 0.001,
    "ounce": 28.34952,
    "ounces": 28.34952,
    "oz": 28.34952,
    "oz.": 28.34952,
    "ozs": 28.34952,
    "ozs.": 28.34952,
    "pound": 453.5924,
    "pounds": 453.5924,
}
UNITS_RE = re.compile("|".join(UNITS.keys()), flags=re.IGNORECASE)

PIPELINE = pipeline.build()
BODY_MASS = pipeline.body_wt()
LEN_SHORTHAND = pipeline.shorthand()
FEMALE_REPRO = pipeline.female_repro()
MALE_REPRO = pipeline.male_repro()
EMBRYO = pipeline.embryo()
PLACENTAL = pipeline.placental_scar_count()


@dataclass
class BaseJanitor:
    dirty: dict[str, Any] = field(default_factory=dict)
    clean: dict[str, Any] = field(default_factory=dict)
    ear_length_count: int = 0  # Can have multiple measurements
    testis_length_count: int = 0  # Can have multiple measurements
    testis_width_count: int = 0  # Can have multiple measurements

    def cleaner(self) -> None: ...

    # --------------------------------------------------------------------------------
    # Per field actions

    def body_mass(self, mass: str, units: str = "") -> None:
        self.clean["body_mass"] = self.to_grams(
            self.dirty[mass], self.dirty.get(units, "")
        )

    def calcar_length(self, length: str, units: str = "") -> None:
        self.clean["calcar_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    def copy(self, clean_label: str, dirty_label: str) -> None:
        if not clean_label:
            msg = "No clean label."
            raise ValueError(msg)

        self.clean[clean_label] = self.dirty[dirty_label]

    def ear_length(self, length: str, units: str = "", measured_from: str = "") -> None:
        ear_label = "ear_length"
        measure_label = "ear_length_measured_from"
        self.ear_length_count += 1
        if self.ear_length_count > 1:
            ear_label += f"_{self.ear_length_count}"
            measure_label += f"_{self.ear_length_count}"
        self.clean[ear_label] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )
        self.clean[measure_label] = measured_from

    def embryo_count(
        self,
        count: str,
        left: str = "",
        right: str = "",
        *,
        only_if_filled: bool = False,
    ) -> None:
        count = self.to_int(self.dirty.get(count, ""))
        left = self.to_int(self.dirty.get(left, ""))
        right = self.to_int(self.dirty.get(right, ""))
        if only_if_filled:
            self.clean["embryo_count"] = count or self.clean.get("embryo_count", "")
            self.clean["embryo_count_left"] = left or self.clean.get(
                "embryo_count_left", ""
            )
            self.clean["embryo_count_right"] = right or self.clean.get(
                "embryo_count_right", ""
            )
        else:
            self.clean["embryo_count"] = count
            self.clean["embryo_count_left"] = left
            self.clean["embryo_count_right"] = right

    def embryo_length(
        self,
        length: str,
        units: str = "",
        measured_from: str = "",
        *,
        only_if_filled: bool = False,
    ) -> None:
        length = self.to_mm(self.dirty[length], self.dirty.get(units, ""))
        if not only_if_filled or (only_if_filled and length):
            self.clean["embryo_length"] = length
            self.clean["embryo_length_measured_from"] = measured_from

    def event_date(self, date_: str) -> None:
        self.clean["eventDate"] = self.dirty[date_].removesuffix("00:00:00").strip()

    def forearm_length(self, length: str, units: str = "") -> None:
        self.clean["forearm_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    def hind_foot_length(
        self, length: str, units: str = "", includes: str = ""
    ) -> None:
        self.clean["hind_foot_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )
        self.clean["hind_foot_length_includes"] = includes

    def placental_scar_count(
        self, count: str = "", left: str = "", right: str = ""
    ) -> None:
        count = self.to_int(self.dirty.get(count, ""))
        left = self.to_int(self.dirty.get(left, ""))
        right = self.to_int(self.dirty.get(right, ""))
        self.clean["placental_scars_present"] = bool(count + left + right)
        self.clean["placental_scar_count"] = count
        self.clean["placental_scars_left"] = left
        self.clean["placental_scars_right"] = right

    def placental_scars_present(self, present: str) -> None:
        value = self.dirty[present]
        true = re.match(r"true|yes", value, flags=re.IGNORECASE)
        false = re.match(r"false|no", value, flags=re.IGNORECASE)
        self.clean["placental_scars_present"] = ""
        if true:
            self.clean["placental_scars_present"] = "True"
        if false:
            self.clean["placental_scars_present"] = "False"

    def tail_length(self, length: str, units: str = "") -> None:
        self.clean["tail_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    def tarsus_length(self, length: str, units: str = "") -> None:
        self.clean["tarsus_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    def testis_length(self, length: str, units: str = "") -> None:
        self.testis_length_count += 1
        label = "testis_length"
        label += f"_{self.testis_length_count}" if self.testis_length_count > 1 else ""
        self.clean[label] = self.to_mm(self.dirty[length], self.dirty.get(units, ""))

    def testis_width(self, width: str, units: str = "") -> None:
        self.testis_width_count += 1
        label = "testis_width"
        label += f"_{self.testis_width_count}" if self.testis_width_count > 1 else ""
        self.clean[label] = self.to_mm(self.dirty[width], self.dirty.get(units, ""))

    def thumb_length(self, length: str, units: str = "", includes: str = "") -> None:
        self.clean["thumb_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )
        self.clean["thumb_length_includes"] = includes

    def total_length(self, length: str, units: str = "") -> None:
        self.clean["total_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    def tragus_length(self, length: str, units: str = "") -> None:
        self.clean["tragus_length"] = self.to_mm(
            self.dirty[length], self.dirty.get(units, "")
        )

    # --------------------------------------------------------------------------------
    # Converters

    @staticmethod
    def as_int(value: str) -> int | None:
        value = re.sub(r",", "", value)
        m = INT.search(value)
        return int(m[0]) if m else None

    @staticmethod
    def to_int(value: str) -> str:
        num = BaseJanitor.as_int(value)
        return "" if num is None else str(num)

    @staticmethod
    def value_with_units(value: str) -> str:
        units_match = UNITS_RE.match(value)
        float_match = FLOAT.match(value)
        units = units_match.group(0) if units_match else ""
        flt = float_match.group(0) if float_match else ""
        converted = BaseJanitor.convert_units(flt, units)
        return converted

    @staticmethod
    def to_grams(value: str, units: str = "g", decimals: int = 1) -> str:
        return BaseJanitor.convert_units(value, units, decimals)

    @staticmethod
    def to_mm(value: str, units: str = "mm", decimals: int = 1) -> str:
        return BaseJanitor.convert_units(value, units, decimals)

    @staticmethod
    def convert_units(value: str, units: str, decimals: int = 1) -> str:
        num = BaseJanitor.as_float(value)

        if num is None:
            return ""

        factor = UNITS.get(units.lower(), 1.0)
        num *= factor
        num = round(num, decimals)
        return str(num)

    @staticmethod
    def as_float(value: str) -> float | None:
        value = re.sub(r",", "", value)

        # Handle numbers formatted like: 4 1/4
        if m := FRACT.search(value):
            whole = BaseJanitor.as_float(m[1]) or 0.0
            num, denom = m[2].split("/")
            num = BaseJanitor.as_float(num) or 0.0
            denom = BaseJanitor.as_float(denom)
            if denom is None:
                return None
            return whole + (num / denom)

        m = FLOAT.search(value)
        return float(m[0]) if m else None

    @staticmethod
    def to_float(value: str, decimals: int = 1) -> str:
        flt = BaseJanitor.as_float(value)
        return f"{flt:0.{decimals}f}" if flt is not None else ""

    # --------------------------------------------------------------------------------
    # Rule parsers

    def parse_all(self, field: str) -> None:
        text = self.clean[field]
        doc = PIPELINE(text)
        self.get_traits(doc)

    def parse_body_mass(self, field: str) -> None:
        text = self.clean[field]
        doc = BODY_MASS(text)
        self.get_traits(doc)

    def parse_embryo(self, field: str) -> None:
        text = self.clean[field]
        doc = EMBRYO(text)
        self.get_traits(doc)

    def parse_placental_scar_count(self, field: str) -> None:
        text = self.clean[field]
        doc = PLACENTAL(text)
        self.get_traits(doc)

    def parse_repro_cond(self, sex_field: str, field: str) -> None:
        sex = self.clean[sex_field].lower()
        text = self.clean[field]
        if sex.startswith("f"):
            doc = FEMALE_REPRO(text)
        elif sex.startswith("m"):
            doc = MALE_REPRO(text)
        else:
            doc = PIPELINE(text)

        self.get_traits(doc)

    def parse_shorthand(self, field: str) -> None:
        text = self.clean[field]
        doc = LEN_SHORTHAND(text)
        traits = [e._.trait for e in doc.ents]
        shorts = {}
        shorts = traits[0].for_csv() if traits and hasattr(traits[0], "for_csv") else {}
        self.clean |= shorts

    def get_traits(self, doc: Doc) -> None:
        traits = [e._.trait for e in doc.ents]
        all_ = {}
        for trait in traits:
            if hasattr(trait, "for_csv"):
                new = trait.for_csv()
                all_ |= {k: v for k, v in new.items() if not self.clean.get(k)}
        self.clean |= all_
