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
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
        Path(__file__).parent / "terms" / "shorthand_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.term_data(csvs, "replace")

    inner_re: ClassVar[str] = r"((\d{1,4}(\.\d{,3})?)|[?x]{1,2})"

    # This separates fields within the shorthand notation
    sep: ClassVar[str] = t_const.DASH + t_const.COLON + t_const.SLASH

    # This separates the last field from the rest
    last: ClassVar[str] = sep + t_const.EQ
    skip: ClassVar[str] = last + t_const.COLON + t_const.QUOTE

    # Expected order of cells
    order: ClassVar[list[str]] = """
        total_length tail_length hind_foot_length ear_length
        """.split()
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

    forearm_length: float = None
    forearm_length_estimated: bool = None

    tragus_length: float = None
    tragus_length_estimated: bool = None

    def to_dwc(self, dwc) -> DarwinCore:  # noqa: C901 PLR0912
        value = {}

        if self.total_length is not None:
            value |= {"totalLengthInMillimeters": self.total_length}
            if self.total_length_estimated:
                value |= {"totalLengthEstimated": True}

        if self.tail_length is not None:
            value |= {"tailLengthInMillimeters": self.tail_length}
            if self.tail_length_estimated:
                value |= {"tailLengthEstimated": True}

        if self.hind_foot_length is not None:
            value |= {"hindFootLengthInMillimeters": self.hind_foot_length}
            if self.hind_foot_length_estimated:
                value |= {"hindFootLengthEstimated": True}

        if self.ear_length is not None:
            value |= {"earLengthInMillimeters": self.ear_length}
            if self.ear_length_estimated:
                value |= {"earLengthEstimated": True}

        if self.forearm_length is not None:
            value |= {"forearmLengthInMillimeters": self.forearm_length}
            if self.forearm_length_estimated:
                value |= {"forearmLengthEstimated": True}

        if self.tragus_length is not None:
            value |= {"tragusLengthInMillimeters": self.tragus_length}
            if self.tragus_length_estimated:
                value |= {"tragusLengthEstimated": True}

        if self.body_mass is not None:
            value |= {"bodyMassInGrams": self.body_mass}
            if self.body_mass_estimated:
                value |= {"bodyMassEstimated": True}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="shorthand_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="missing_patterns",
            compiler=cls.missing_patterns(),
            overwrite=["metric_mass", "number"],
            # merge=["cell"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="cell_patterns",
            compiler=cls.cell_patterns(),
            overwrite=["metric_mass", "number"],
            # merge=["cell"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="shorthand_patterns",
            compiler=cls.shorthand_patterns(),
            overwrite=["metric_mass", "cell", "number", "missing"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp,
            name="shorthand_triple_patterns",
            compiler=cls.shorthand_triple_patterns(),
            overwrite=["metric_mass", "cell", "triple_key", "number", "missing"],
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.cleanup_pipe(nlp, name="shorthand_cleanup", clear=False)
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def missing_patterns(cls):
        decoder = {
            "missing": {"LOWER": {"REGEX": r"^(x|\?){1,2}$"}},
        }

        return [
            Compiler(
                label="missing",
                on_match="cell_match",
                decoder=decoder,
                patterns=[
                    " missing ",
                ],
            ),
        ]

    @classmethod
    def cell_patterns(cls):
        decoder = {
            "(": {"TEXT": "("},
            ")": {"TEXT": ")"},
            "99": {"ENT_TYPE": "number"},
            "[": {"TEXT": "["},
            "]": {"TEXT": "]"},
            "g": {"ENT_TYPE": "metric_mass"},
            "label": {"LOWER": {"REGEX": r"^(fa|tr)$"}},
            "99fa": {"LOWER": {"REGEX": r"^\d+(fa|tr)$"}},
            "fa99": {"LOWER": {"REGEX": r"^(fa|tr)\d+$"}},
        }

        return [
            Compiler(
                label="cell",
                on_match="cell_match",
                decoder=decoder,
                patterns=[
                    " 99 (? label )? ",
                    " [ 99 g? ] ",
                    " [ 99 g? ] ",
                    " 99fa ",
                    " fa99 ",
                ],
            ),
        ]

    @classmethod
    def shorthand_patterns(cls):
        decoder = {
            "-": {"TEXT": {"IN": cls.sep}},
            "=": {"TEXT": {"IN": cls.last}},
            "99": {"ENT_TYPE": {"IN": ["number", "cell", "missing"]}, "OP": "+"},
            "99.0": {"ENT_TYPE": {"IN": ["number", "cell"]}, "OP": "+"},
            "g": {"ENT_TYPE": "metric_mass"},
        }

        return [
            Compiler(
                label="shorthand",
                keep="shorthand",
                on_match="shorthand_match",
                decoder=decoder,
                patterns=[
                    " 99 - 99 - 99 - 99           =? 99.0 g* ",
                    " 99 - 99 - 99 - 99 - 99      =? 99.0 g* ",
                    " 99 - 99 - 99 - 99 - 99 - 99 =? 99.0 g* ",
                    " 99 - 99 - 99 - 99 ",
                    " 99 - 99 - 99 - 99      - 99.0 ",
                    " 99 - 99 - 99 - 99 - 99 - 99.0 ",
                ],
            ),
        ]

    @classmethod
    def shorthand_triple_patterns(cls):
        decoder = {
            "-": {"TEXT": {"IN": cls.sep}},
            ":": {"TEXT": {"IN": t_const.COLON + t_const.COMMA + t_const.EQ}},
            "99": {"TEXT": {"REGEX": cls.inner_re}},
            "key": {"ENT_TYPE": "triple_key"},
            "length": {"ENT_TYPE": "length"},
            "sex": {"ENT_TYPE": "sex"},
            "tag": {"ENT_TYPE": "tag"},
            '"': {"TEXT": {"IN": t_const.QUOTE}},
        }

        return [
            Compiler(
                label="shorthand",
                keep="shorthand",
                on_match="shorthand_match",
                decoder=decoder,
                patterns=[
                    ' "? key length*     "? :* "? 99 - 99 - 99 "? ',
                    ' "? tag 99* :* sex? "? :* "? 99 - 99 - 99 "? ',
                ],
            ),
        ]

    @classmethod
    def shorthand_match(cls, ent):
        kwargs = {}

        # How may length fields are expected
        full = 4

        # Remove unneeded characters and entities
        cells = [e for e in ent.ents if e.label_ in ("number", "cell", "missing")]

        bats = []

        for i, cell in enumerate(cells):
            cell = cell.text.lower()

            # Forearm length can be labeled
            if cell.find("fa") > -1:
                length, estimated = cls.get_values(cell)
                kwargs["forearm_length"] = length
                kwargs["forearm_length_estimated"] = estimated

            # Tragus length can be labeled
            elif cell.find("tr") > -1:
                length, estimated = cls.get_values(cell)
                kwargs["tragus_length"] = length
                kwargs["tragus_length_estimated"] = estimated

            # Body mass is always last but it may be missing
            elif i >= full and i == len(cells) - 1:
                length, estimated = cls.get_values(cell)
                kwargs["body_mass"] = length
                kwargs["body_mass_estimated"] = estimated

            # Follow the expected order
            else:
                length, estimated = cls.get_values(cell)
                if i < full:
                    field = cls.order[i]
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
    def cell_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("cell_match")
def cell_match(ent):
    return Shorthand.cell_match(ent)


@registry.misc("shorthand_match")
def shorthand_match(ent):
    return Shorthand.shorthand_match(ent)
