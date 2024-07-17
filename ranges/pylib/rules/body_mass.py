from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class BodyMass(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
        Path(__file__).parent / "terms" / "body_mass_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    factor: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_g")
    factor: ClassVar[dict[str, str]] = {k: float(v) for k, v in factor.items()}
    keys: ClassVar[list[str]] = """ key_with_units key_leader wt_key """.split()
    units: ClassVar[list[str]] = """
        key_with_units metric_mass imperial_mass
        """.split()
    # ---------------------

    mass: float | list[float] = None
    units_inferred: bool = None
    ambiguous: bool = None
    estimated: bool = None

    def to_dict(self) -> dict[str, dict[str, Any]]:
        value = {
            "body_mass": {
                "body_mass_grams": self.mass,
                "_parser": self.__class__.__name__,
            }
        }

        if self.units_inferred:
            value["body_mass"] |= {"body_mass_units_inferred": True}

        if self.ambiguous:
            value["body_mass"] |= {"body_mass_ambiguous": True}

        if self.estimated:
            value["body_mass"] |= {"body_mass_estimated": True}

        return value

    def to_dwc(self, dwc) -> DarwinCore:
        value = {"bodyMassInGrams": self.mass}

        if self.units_inferred:
            value |= {"bodyMassUnitsInferred": True}

        if self.ambiguous:
            value |= {"bodyMassAmbiguous": True}

        if self.estimated:
            value |= {"bodyMassEstimated": True}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="body_mass_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="not_mass_patterns",
            compiler=cls.not_mass_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="compound_mass_patterns",
            compiler=cls.compound_mass_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="mass_range_patterns",
            compiler=cls.mass_range_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="body_mass_patterns",
            compiler=cls.body_mass_patterns(),
            overwrite=["number"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.cleanup_pipe(nlp, name="body_mass_cleanup")

    @classmethod
    def not_mass_patterns(cls):
        decoder = {
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "[": {"TEXT": "[", "OP": "?"},
            "]": {"TEXT": "]", "OP": "?"},
            "g": {"ENT_TYPE": {"IN": ["metric_mass", "imperial_mass"]}},
            "key": {"ENT_TYPE": "wt_key", "OP": "+"},
            "key_g": {"ENT_TYPE": "key_with_units", "OP": "+"},
            "other": {"ENT_TYPE": "other_wt", "OP": "+"},
            "leader": {"ENT_TYPE": "key_leader", "OP": "*"},
            '"': {"TEXT": {"IN": t_const.QUOTE}, "OP": "?"},
        }
        return [
            Compiler(
                label="not_body_mass",
                on_match="not_body_mass_match",
                decoder=decoder,
                patterns=[
                    ' other key_g       " : " [ 99 ] ',
                    ' other leader      " : " [ 99 ] g+ ] ',
                    ' other leader* key " : " [ 99 ] g* ] ',
                ],
            ),
        ]

    @classmethod
    def body_mass_patterns(cls):
        decoder = {
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "[": {"TEXT": "[", "OP": "?"},
            "]": {"TEXT": "]", "OP": "?"},
            "g": {"ENT_TYPE": {"IN": ["metric_mass", "imperial_mass"]}},
            "key": {"ENT_TYPE": "wt_key", "OP": "+"},
            "key_g": {"ENT_TYPE": "key_with_units", "OP": "+"},
            "leader": {"ENT_TYPE": "key_leader", "OP": "*"},
            '"': {"TEXT": {"IN": t_const.QUOTE}, "OP": "?"},
        }
        return [
            Compiler(
                label="body_mass",
                keep="body_mass",
                on_match="body_mass_match",
                decoder=decoder,
                patterns=[
                    ' key g      " : " [ 99 ] ',
                    ' key_g      " : " [ 99 ] ',
                    ' leader     " : " [ 99 ] g+ ] ',
                    ' leader key " : " [ 99 ] g* ] ',
                ],
            ),
        ]

    @classmethod
    def compound_mass_patterns(cls):
        decoder = {
            ",": {"TEXT": {"IN": t_const.COMMA}, "OP": "?"},
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "key": {"ENT_TYPE": "wt_key", "OP": "+"},
            "lbs": {"ENT_TYPE": "imperial_mass", "OP": "+"},
            "ozs": {"ENT_TYPE": "imperial_mass", "OP": "+"},
            "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
        }
        return [
            Compiler(
                label="body_mass",
                keep="body_mass",
                on_match="compound_mass_match",
                decoder=decoder,
                patterns=[
                    "       99 lbs , 99 ozs ",
                    " key : 99 lbs , 99 ozs ",
                    "       99 lbs , 99 to 99 ozs ",
                    " key : 99 lbs , 99 to 99 ozs ",
                ],
            ),
        ]

    @classmethod
    def mass_range_patterns(cls):
        decoder = {
            "99": {"ENT_TYPE": "number", "OP": "+"},
            ":": {
                "TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ},
                "OP": "?",
            },
            "g": {"ENT_TYPE": {"IN": ["metric_mass", "imperial_mass"]}},
            "key": {"ENT_TYPE": "wt_key", "OP": "+"},
            "key_g": {"ENT_TYPE": "key_with_units", "OP": "+"},
            "leader": {"ENT_TYPE": "key_leader", "OP": "*"},
            "to": {"LOWER": {"IN": ["to", *t_const.DASH]}, "OP": "+"},
        }
        return [
            Compiler(
                label="body_mass",
                keep="body_mass",
                on_match="mass_range_match",
                decoder=decoder,
                patterns=[
                    " key_g      : 99 to 99    ",
                    " leader     : 99 to 99 g+ ",
                    " leader key : 99 to 99 g* ",
                ],
            ),
        ]

    @classmethod
    def in_grams(cls, number, units):
        units = units.text.lower() if units else ""
        factor = cls.factor.get(units, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def body_mass_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        estimated = True if ent.text.find("[") > -1 else None

        number = next(e for e in ent.ents if e.label_ == "number")
        mass = cls.in_grams(number, units)

        return cls.from_ent(
            ent,
            mass=mass,
            ambiguous=ambiguous,
            estimated=estimated,
            units_inferred=units_inferred,
        )

    @classmethod
    def compound_mass_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        numbers = [e for e in ent.ents if e.label_ == "number"]

        units = [e for e in ent.ents if e.label_ == "imperial_mass"]

        is_range = 3

        mass = cls.in_grams(numbers[0], units[0])

        if len(numbers) < is_range:
            mass += cls.in_grams(numbers[1], units[1])
            mass = round(mass, 2)
        else:
            mass = [
                round(mass + cls.in_grams(numbers[1], units[1]), 2),
                round(mass + cls.in_grams(numbers[2], units[1]), 2),
            ]

        return cls.from_ent(ent, mass=mass, ambiguous=ambiguous)

    @classmethod
    def mass_range_match(cls, ent):
        ambiguous = [e for e in ent.ents if e.label_ in cls.keys]
        ambiguous = True if len(ambiguous) == 0 else None

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        numbers = [e for e in ent.ents if e.label_ == "number"]

        mass = [cls.in_grams(numbers[0], units), cls.in_grams(numbers[1], units)]

        return cls.from_ent(
            ent, mass=mass, ambiguous=ambiguous, units_inferred=units_inferred
        )

    @classmethod
    def not_body_mass_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("body_mass_match")
def body_mass_match(ent):
    return BodyMass.body_mass_match(ent)


@registry.misc("compound_mass_match")
def compound_mass_match(ent):
    return BodyMass.compound_mass_match(ent)


@registry.misc("mass_range_match")
def mass_range_match(ent):
    return BodyMass.mass_range_match(ent)


@registry.misc("not_body_mass_match")
def not_body_mass_match(ent):
    return BodyMass.not_body_mass_match(ent)
