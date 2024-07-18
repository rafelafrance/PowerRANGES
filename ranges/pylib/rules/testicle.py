from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import registry
from spacy.tokens import Token
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import RejectMatch
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class Testicle(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
        Path(__file__).parent / "terms" / "testicle_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, str]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    units: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    sides: ClassVar[list[str]] = ["left", "right", "both"]

    overwrite: ClassVar[list[str]] = ["number"]

    decoder: ClassVar[dict[str, dict]] = {
        ",": {"LOWER": {"IN": list(":;,.-=\"()>'")}, "OP": "*"},
        "-": {"LOWER": {"IN": list(':;,.-="<>')}, "OP": "*"},
        "9": {"ENT_TYPE": "number"},
        "abbrev": {"ENT_TYPE": "abbrev", "OP": "*"},
        "abdominal": {"ENT_TYPE": "abdominal", "OP": "+"},
        "alone": {"ENT_TYPE": "descr_alone", "OP": "+"},
        "and": {"ENT_TYPE": "and", "OP": "+"},
        "descended": {"ENT_TYPE": "descended", "OP": "+"},
        "descr": {"ENT_TYPE": "description", "OP": "+"},
        "fully": {"ENT_TYPE": "fully", "OP": "+"},
        "g": {"ENT_TYPE": {"IN": ["metric_mass", "imperial_mass"]}},
        "left": {"ENT_TYPE": {"IN": sides}, "OP": "+"},
        "mm": {"ENT_TYPE": {"IN": units}, "OP": "*"},
        "non": {"ENT_TYPE": "non", "OP": "+"},
        "partially": {"ENT_TYPE": "partially", "OP": "+"},
        "right": {"ENT_TYPE": {"IN": sides}, "OP": "+"},
        "scrotal": {"ENT_TYPE": "scrotal", "OP": "+"},
        "side": {"ENT_TYPE": {"IN": sides}, "OP": "*"},
        "size": {"ENT_TYPE": "size", "OP": "+"},
        "testes": {"ENT_TYPE": {"IN": ["testes", "abbrev"]}, "OP": "+"},
        "x": {"LOWER": {"IN": t_const.CROSS + t_const.DASH}},
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    description: str = None
    length: float = None
    width: float = None
    length2: float = None
    width2: float = None
    units_inferred: bool = None

    def as_dict(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        if self.description is not None:
            value["testicle_description"] |= {"testicle_description": self.description}

        if self.length is not None:
            value["testicle_size"] |= {"testicle_length_mm": self.length}

        if self.length2 is not None:
            value["testicle_size"] |= {"testicle_length_2nd_mm": self.length2}

        if self.width is not None:
            value["testicle_size"] |= {"testicle_width_mm": self.width}

        if self.width2 is not None:
            value["testicle_size"] |= {"testicle_width_2nd_mm": self.width2}

        if self.units_inferred is not None:
            value["testicle_size"] |= {
                "testicle_size_units_inferred": self.units_inferred
            }

        if "testicle_description" in value:
            value["testicle_description"]["_parser"] = self.__class__.__name__

        if "testicle_size" in value:
            value["testicle_size"]["_parser"] = self.__class__.__name__

        return value

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}

        if self.description is not None:
            value |= {"testicleDescription": self.description}

        if self.length is not None:
            value |= {"testicleLength": self.length}

        if self.length2 is not None:
            value |= {"testicleLength2": self.length2}

        if self.width is not None:
            value |= {"testicleWidth": self.width}

        if self.width2 is not None:
            value |= {"testicleWidth2": self.width2}

        if self.units_inferred is not None:
            value |= {"testicleUnitsInferred": self.units_inferred}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="testicle_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="not_testicle_size_patterns",
            compiler=cls.not_testicle_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_description_patterns",
            compiler=cls.testicle_description_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_descr_alone_patterns",
            compiler=cls.testicle_descr_alone_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_double_patterns",
            compiler=cls.testicle_double_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_size_patterns",
            compiler=cls.testicle_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_state_patterns",
            compiler=cls.testicle_state_patterns(),
            overwrite=["number"],
        )

        # add.debug_tokens(nlp)  # ############################################
        add.cleanup_pipe(nlp, name="testicle_description_cleanup")

    @classmethod
    def not_testicle_size_patterns(cls):
        return [
            Compiler(
                label="not_length",
                on_match="not_testicle_size_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 g ",
                ],
            ),
        ]

    @classmethod
    def testicle_description_patterns(cls):
        return [
            Compiler(
                label="description",
                on_match="testicle_description_match",
                decoder=cls.decoder,
                patterns=[
                    " non - fully descended ",
                    " abdominal ",
                    " abdominal , non - descended ",
                    " abdominal descended ",
                    " non - descended ",
                    " fully - descended ",
                    " partially descended ",
                    " size ",
                    " size , non - descended ",
                    " size , descended ",
                    " descended ",
                ],
            ),
        ]

    @classmethod
    def testicle_descr_alone_patterns(cls):
        return [
            Compiler(
                label="descr_alone",
                on_match="descr_alone_match",
                decoder=cls.decoder,
                patterns=[
                    " scrotal ",
                    " non - scrotal ",
                ],
            ),
        ]

    @classmethod
    def testicle_state_patterns(cls):
        return [
            Compiler(
                label="testicle",
                keep="testicle",
                on_match="testicle_state_match",
                decoder=cls.decoder,
                patterns=[
                    " non testes ",
                    "            alone ",
                    "     testes alone ",
                    "     testes descr ",
                    "     testes descr , and , descr ",
                ],
            ),
        ]

    @classmethod
    def testicle_size_patterns(cls):
        return [
            Compiler(
                label="testicle",
                keep="testicle",
                on_match="testicle_size_match",
                decoder=cls.decoder,
                patterns=[
                    " testes , side , 9 mm ",
                    " testes , side , 9 mm , descr ",
                    " testes , side , 9 mm , alone ",
                    " testes , side , 9 mm x 9 mm ",
                    " testes , side , 9 mm x 9 mm and 9 mm x 9 mm ",
                    " testes , side , 9 mm x 9 mm , alone ",
                    " testes , side , 9 mm x 9 mm , descr ",
                    " testes , descr , abbrev , 9 mm ",
                    " testes , descr , abbrev , 9 mm x 9 mm ",
                    " testes , alone , abbrev , 9 mm ",
                    " testes , alone , abbrev , 9 mm x 9 mm ",
                    " alone , abbrev , 9 mm x 9 mm ",
                    " testes , x 9 mm ",
                    " testes ,   9 mm , descr ",
                    " testes ,   9 mm , alone ",
                ],
            ),
        ]

    @classmethod
    def testicle_double_patterns(cls):
        return [
            Compiler(
                label="testicle",
                keep="testicle",
                on_match="testicle_double_match",
                decoder=cls.decoder,
                patterns=[
                    " testes , left , 9 mm , right   9 mm ",
                    " testes , left , 9 mm , right x 9 mm ",
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
    def not_testicle_size_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def testicle_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def descr_alone_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def testicle_state_match(cls, ent):
        data = {}
        descr = [
            cls.replace.get(e.text.lower(), e.text.lower())
            for e in ent.ents
            if e.label_ in ("description", "descr_alone")
        ]
        data["description"] = " ".join(descr) if descr else ent.text.lower()
        return cls.from_ent(ent, **data)

    @classmethod
    def testicle_size_match(cls, ent):
        data = {}
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        descr = [
            cls.replace.get(e.text.lower(), e.text.lower())
            for e in ent.ents
            if e.label_ in ("description", "descr_alone")
        ]
        nums = [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]
        if not nums:
            raise RejectMatch

        one_pair = 2
        two_pairs = 4

        data["length"] = nums[0]
        data["width"] = nums[1] if len(nums) > 1 else None
        data["length2"] = nums[2] if len(nums) > one_pair else None
        data["width2"] = nums[3] if len(nums) >= two_pairs else None

        if descr:
            data["description"] = " ".join(descr)

        data["units_inferred"] = True if units is None else None

        return cls.from_ent(ent, **data)

    @classmethod
    def testicle_double_match(cls, ent):
        data = {}
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        descr = [
            cls.replace.get(e.text.lower(), e.text.lower())
            for e in ent.ents
            if e.label_ in ("description", "descr_alone")
        ]
        nums = [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]

        data["length"] = nums[0]
        data["length2"] = nums[1] if len(nums) > 1 else None

        if descr:
            data["description"] = " ".join(descr)

        data["units_inferred"] = True if units is None else None

        return cls.from_ent(ent, **data)


@registry.misc("testicle_description_match")
def testicle_description_match(ent):
    return Testicle.testicle_description_match(ent)


@registry.misc("descr_alone_match")
def descr_alone_match(ent):
    return Testicle.descr_alone_match(ent)


@registry.misc("testicle_state_match")
def testicle_state_match(ent):
    return Testicle.testicle_state_match(ent)


@registry.misc("testicle_size_match")
def testicle_size_match(ent):
    return Testicle.testicle_size_match(ent)


@registry.misc("not_testicle_size_match")
def not_testicle_size_match(ent):
    return Testicle.not_testicle_size_match(ent)


@registry.misc("testicle_double_match")
def testicle_double_match(ent):
    return Testicle.testicle_double_match(ent)
