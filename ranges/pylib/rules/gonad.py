from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from spacy.tokens import Token
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class Gonad(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "gonad_terms.csv",
    ]

    units: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    overwrite: ClassVar[list[str]] = ["number", *units]

    keys: ClassVar[list[str]] = """
        gonad gonad_len gonad_len_mm gonad_width gonad_width_mm """.split()

    decoder: ClassVar[dict[str, dict]] = {
        "'": {"LOWER": {"IN": t_const.QUOTE}, "OP": "?"},
        ",": {"LOWER": {"IN": list(":;,.-=<>")}, "OP": "?"},
        "9": {"ENT_TYPE": "number"},
        "key": {"ENT_TYPE": {"IN": keys}, "OP": "+"},
        "mm": {"ENT_TYPE": {"IN": units}, "OP": "*"},
        "x": {"LOWER": {"IN": t_const.CROSS}},
    }

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    # ---------------------

    description: str = None
    length: float = None
    width: float = None
    units_inferred: bool = None

    def to_dict(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        if self.description is not None:
            value["gonad_description"] |= {"gonad_description": self.description}

        if self.length is not None:
            value["gonad_size"] |= {"gonad_length_mm": self.length}

        if self.width is not None:
            value["gonad_size"] |= {"gonad_width_mm": self.width}

        if self.units_inferred is not None:
            value["gonad_size"] |= {"gonad_size_units_inferred": self.units_inferred}

        return value

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}

        if self.description is not None:
            value |= {"gonadDescription": self.description}

        if self.length is not None:
            value |= {"gonadLength": self.length}

        if self.width is not None:
            value |= {"gonadWidth": self.width}

        if self.units_inferred is not None:
            value |= {"gonadUnitsInferred": self.units_inferred}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="gonad_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="gonad_numbered_size_patterns",
            compiler=cls.gonad_numbered_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="gonad_keyed_size_patterns",
            compiler=cls.gonad_keyed_size_patterns(),
            overwrite=["number"],
        )

        # add.debug_tokens(nlp)  # ###########################################
        add.cleanup_pipe(nlp, name="gonad_cleanup")

    @classmethod
    def gonad_numbered_size_patterns(cls):
        return [
            Compiler(
                label="gonad",
                keep="gonad",
                on_match="gonad_numbered_size_match",
                decoder=cls.decoder,
                patterns=[
                    " key 9 ' , ' 9 mm ",
                ],
            ),
        ]

    @classmethod
    def gonad_keyed_size_patterns(cls):
        return [
            Compiler(
                label="gonad",
                keep="gonad",
                on_match="gonad_keyed_size_match",
                decoder=cls.decoder,
                patterns=[
                    " key ' , ' 9 mm ",
                ],
            ),
        ]

    @classmethod
    def in_millimeters(cls, number, units: Token | str | None):
        if hasattr(units, "text"):
            units = units.text.lower()
        elif isinstance(units, str):
            units = units.lower()

        factor = cls.factor_mm.get(units, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def get_units(cls, ent, key):
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        if not units and key in ("gonad_len_mm", "gonad_width_mm"):
            units = "mm"
        return units

    @classmethod
    def get_key(cls, ent):
        return next((e.label_ for e in ent.ents if e.label_ in cls.keys), None)

    @classmethod
    def get_numbers(cls, ent, units):
        return [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]

    @classmethod
    def gonad_numbered_size_match(cls, ent):
        key = cls.get_key(ent)
        units = cls.get_units(ent, key)
        nums = cls.get_numbers(ent, units)
        return cls.gonad_labeled_size_match(ent, nums[1:], units, key)

    @classmethod
    def gonad_keyed_size_match(cls, ent):
        key = cls.get_key(ent)
        units = cls.get_units(ent, key)
        nums = cls.get_numbers(ent, units)
        return cls.gonad_labeled_size_match(ent, nums, units, key)

    @classmethod
    def gonad_labeled_size_match(cls, ent, nums, units, key):
        data = {}

        if key.startswith("gonad_len"):
            data["length"] = nums[0]
        elif key.startswith("gonad_width"):
            data["width"] = nums[0]
        else:
            one_pair = 2
            two_pairs = 4
            data["length"] = nums[0]
            data["width"] = nums[1] if len(nums) > 1 else None
            data["length2"] = nums[2] if len(nums) > one_pair else None
            data["width2"] = nums[3] if len(nums) >= two_pairs else None

        data["units_inferred"] = True if not units else None

        descr = next(
            (e.text.lower() for e in ent.ents if e.label_ == "description"), None
        )
        data["description"] = descr

        return cls.from_ent(ent, **data)


@registry.misc("gonad_numbered_size_match")
def gonad_numbered_size_match(ent):
    return Gonad.gonad_numbered_size_match(ent)


@registry.misc("gonad_keyed_size_match")
def gonad_keyed_size_match(ent):
    return Gonad.gonad_keyed_size_match(ent)
