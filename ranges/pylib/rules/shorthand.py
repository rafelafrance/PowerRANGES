"""
Parse a shorthand notations like: "11-22-33-44:99g".

There are other separators "/", ":", etc.
There is also an extended form that looks like:
  "11-22-33-44-fa55-hb66:99g" There may be several extended numbers.

  11 = total length (ToL or TL) or sometimes head body length
  22 = tail length (TaL)
  33 = hind foot length (HFL)
  44 = ear length (EL)
  99 = body mass is optional, as are the mass units

Unknown values are filled with "?" or "x".
  E.g.: "11-x-x-44" or "11-?-33-44"

Ambiguous measurements are enclosed in brackets.
  E.g.: 11-[22]-33-[44]:99g
"""
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib import util as t_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


@dataclass
class Bat:
    length: float
    estimated: bool


@dataclass(eq=False)
class Shorthand(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "shorthand_terms.csv",
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.term_data(csvs, "replace")

    inner_re: ClassVar[str] = r"((\d{1,4}(\.\d{,3})?)|[?x]{1,2})"
    float_re: ClassVar[str] = r"(\d{1,4}(\.\d{,3})?)"

    # This separates fields within the shorthand notation
    sep: ClassVar[str] = t_const.DASH + t_const.COLON + t_const.SLASH

    # This separates the last field from the rest
    last: ClassVar[str] = sep + t_const.EQ
    skip: ClassVar[str] = last + t_const.COLON + t_const.QUOTE
    # ---------------------

    total_length: float = None
    total_length_estimated: bool = None

    tail_length: float = None
    tail_length_estimated: bool = None

    hind_foot_length: float = None
    hind_foot_length_estimated: bool = None

    ear_length: float = None
    ear_length_estimated: bool = None

    body_mass: float = None
    body_mass_estimated: bool = None

    # For bats

    forearm_length: float = None
    forearm_length_estimated: bool = None

    tragus_length: float = None
    tragus_length_estimated: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}
        # value = {"bodyMassInGrams": self.mass}

        # if self.units_inferred:
        #     value |= {"bodyMassUnitsInferred": True}

        # if self.shorthand:
        #     value |= {"bodyMassShorthand": True}

        # if self.ambiguous:
        #     value |= {"bodyMassAmbiguous": True}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="shorthand_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="shorthand_cell_patterns",
            compiler=cls.shorthand_cell_patterns(),
            overwrite=["metric_mass"],
            merge=["shorthand_cell"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="shorthand_patterns",
            compiler=cls.shorthand_patterns(),
            overwrite=["metric_mass", "shorthand_cell", "triple_key"],
        )
        add.debug_tokens(nlp)  # ###########################################

        add.cleanup_pipe(nlp, name="shorthand_cleanup")
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def shorthand_cell_patterns(cls):
        decoder = {
            "(": {"TEXT": "("},
            ")": {"TEXT": ")"},
            "[": {"TEXT": "["},
            "]": {"TEXT": "]"},
            "99": {"TEXT": {"REGEX": cls.float_re}},
            "g": {"ENT_TYPE": "metric_mass"},
            "label": {"LOWER": {"REGEX": r"^(fa|tr)$"}},
        }

        return [
            Compiler(
                label="shorthand_cell",
                on_match="shorthand_cell_match",
                decoder=decoder,
                patterns=[
                    " 99 (? label )? ",
                    " [ 99 g? ] ",
                ],
            ),
        ]

    @classmethod
    def shorthand_patterns(cls):
        decoder = {
            '"': {"TEXT": {"IN": t_const.QUOTE}},
            "-": {"TEXT": {"IN": cls.sep}},
            "=": {"TEXT": {"IN": cls.last}},
            ":": {"TEXT": {"IN": t_const.COLON + t_const.COMMA}},
            "99": {"TEXT": {"REGEX": cls.inner_re}},
            "99.0": {"TEXT": {"REGEX": cls.float_re}},
            "99xx": {"LOWER": {"REGEX": r"^\d+(fa|tr)$"}},
            "cell": {"ENT_TYPE": "shorthand_cell"},
            "g": {"ENT_TYPE": "metric_mass"},
            "xx99": {"LOWER": {"REGEX": r"^(fa|tr)\d+$"}},
            "key": {"ENT_TYPE": "triple_key"},
        }

        return [
            Compiler(
                label="shorthand",
                keep="shorthand",
                on_match="shorthand_match",
                decoder=decoder,
                patterns=[
                    " 99 - 99 - 99 - 99               =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - 99          =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - 99   - 99   =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - xx99        =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - xx99 - xx99 =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - 99xx        =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - 99xx - 99xx =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - cell        =? 99.0? g* ",
                    " 99 - 99 - 99 - 99 - cell - cell =? 99.0? g* ",
                    ' "? key "? :? "? 99 - 99 - 99 "? ',
                ],
            ),
        ]

    @classmethod
    def shorthand_match(cls, ent):
        kwargs = {}

        # How may length fields are expected
        full = 4

        # Remove unneeded characters and entities
        tokens = [t for t in ent if t.text not in cls.skip]
        tokens = [t for t in tokens if t.ent_type_ != "triple_key"]

        # Get mass units
        _units = tokens.pop() if tokens[-1].ent_type_ == "metric_mass" else ""

        # Expected order of fields
        fields = """ total_length tail_length hind_foot_length ear_length """.split()

        bats = []

        for i, token in enumerate(tokens):
            # Forearm length can be labeled
            if token.lower_.find("fa") > -1:
                length, estimated = cls.get_values(token.text)
                kwargs["forearm_length"] = length
                kwargs["forearm_length_estimated"] = estimated

            # Tragus length can be labeled
            elif token.lower_.find("tr") > -1:
                length, estimated = cls.get_values(token.text)
                kwargs["tragus_length"] = length
                kwargs["tragus_length_estimated"] = estimated

            # Body mass is always last but it may be missing
            elif i >= full and i == len(tokens) - 1:
                length, estimated = cls.get_values(token.text)
                kwargs["body_mass"] = length
                kwargs["body_mass_estimated"] = estimated

            # Follow the expected order
            else:
                length, estimated = cls.get_values(token.text)
                if i < full:
                    field = fields[i]
                    kwargs[field] = length
                    kwargs[f"{field}_estimated"] = estimated
                else:
                    bats.append(Bat(length, estimated))

        # If there are 6 length fields then it's forearm then tragus length
        if len(bats) > 1:
            kwargs["forearm_length"] = bats[0].length
            kwargs["forearm_length_estimated"] = bats[0].estimated
            kwargs["tragus_length"] = bats[1].length
            kwargs["tragus_length_estimated"] = bats[1].estimated

        # If there are 5 fields, we need to compare the value against ear length
        elif len(bats) == 1:
            # If the length is grater than ear length it's forearm else it's tragus
            if bats[0].length > kwargs.get("ear_length", 0.0):
                kwargs["forearm_length"] = bats[0].length
                kwargs["forearm_length_estimated"] = bats[0].estimated

            else:
                kwargs["tragus_length"] = bats[0].length
                kwargs["tragus_length_estimated"] = bats[0].estimated

        return cls.from_ent(ent, **kwargs)

    @staticmethod
    def get_values(text):
        value = t_util.to_positive_float(text)
        estimated = True if value and text.find("[") > -1 else None
        return value, estimated

    @classmethod
    def shorthand_cell_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("shorthand_cell_match")
def shorthand_cell_match(ent):
    return Shorthand.shorthand_cell_match(ent)


@registry.misc("shorthand_match")
def shorthand_match(ent):
    return Shorthand.shorthand_match(ent)
