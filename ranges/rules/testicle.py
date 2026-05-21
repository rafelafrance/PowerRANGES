from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pipes.reject_match import RejectMatch
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.rules import terms as t_terms

from ranges.rules.base import Base


@dataclass(eq=False)
class Testicle(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
        Path(__file__).parent / "terms" / "testicle_terms.csv",
    ]

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }

    units: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    sides: ClassVar[list[str]] = ["left", "right", "both"]

    pos_terms: ClassVar[list[str]] = ["abdominal", "descended", "inguinal"]

    overwrite: ClassVar[list[str]] = ["number"]

    decoder: ClassVar[dict[str, dict]] = {
        ",": {"LOWER": {"IN": list(":;,.-=\"()>'")}, "OP": "*"},
        "-": {"LOWER": {"IN": list(':;,.-="<>')}, "OP": "*"},
        "9": {"ENT_TYPE": "number"},
        "abbrev": {"ENT_TYPE": "abbrev", "OP": "*"},
        "abdominal": {"ENT_TYPE": "abdominal", "OP": "+"},
        "alone": {"ENT_TYPE": "pos_alone", "OP": "+"},
        "and": {"ENT_TYPE": "and", "OP": "+"},
        "descended": {"ENT_TYPE": "descended", "OP": "+"},
        "descr": {"ENT_TYPE": "description", "OP": "+"},
        "fully": {"ENT_TYPE": "fully", "OP": "+"},
        "g": {"ENT_TYPE": {"IN": ["metric_mass", "imperial_mass"]}},
        "ing": {"ENT_TYPE": "inguinal"},
        "left": {"ENT_TYPE": {"IN": sides}, "OP": "+"},
        "mm": {"ENT_TYPE": {"IN": units}, "OP": "*"},
        "non": {"ENT_TYPE": "non", "OP": "+"},
        "partially": {"ENT_TYPE": "partially", "OP": "+"},
        "pos": {"ENT_TYPE": "position", "OP": "+"},
        "right": {"ENT_TYPE": {"IN": sides}, "OP": "+"},
        "scrotal": {"ENT_TYPE": "scrotal", "OP": "+"},
        "side": {"ENT_TYPE": {"IN": sides}, "OP": "*"},
        "size": {"ENT_TYPE": "size", "OP": "+"},
        "testes": {"ENT_TYPE": {"IN": ["testes", "abbrev"]}},
        "x": {"LOWER": {"IN": t_const.CROSS + t_const.DASH}},
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    position: str | None = None
    description: str | None = None
    length: float | None = None
    width: float | None = None
    length2: float | None = None
    width2: float | None = None
    units_inferred: bool | None = None

    def for_csv(self) -> dict[str, Any]:
        value = {}

        if self.description is not None:
            value["testis_description"] = self.description

        if self.position is not None:
            value["testis_position"] = self.position

        if self.length is not None:
            value["testis_length"] = self.length

        if self.length2 is not None:
            value["testis_length_2"] = self.length2

        if self.width is not None:
            value["testis_width"] = self.width

        if self.width2 is not None:
            value["testis_width_2"] = self.width2

        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="testicle_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="not_testicle_size_patterns",
            compiler=cls.not_testicle_size_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_position_patterns",
            compiler=cls.testicle_position_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_description_patterns",
            compiler=cls.testicle_description_patterns(),
            overwrite=["number"],
        )

        # add.debug_tokens(nlp)  # ############################################
        add.trait_pipe(
            nlp,
            name="testicle_pos_alone_patterns",
            compiler=cls.testicle_pos_alone_patterns(),
            overwrite=["number", "description"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_double_patterns",
            compiler=cls.testicle_double_patterns(),
            overwrite=["number", "description"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_size_patterns",
            compiler=cls.testicle_size_patterns(),
            overwrite=["number", "description"],
        )

        add.trait_pipe(
            nlp,
            name="testicle_state_patterns",
            compiler=cls.testicle_state_patterns(),
            overwrite=["number", "description"],
        )

        add.cleanup_pipe(nlp, name="testicle_description_cleanup")

    @classmethod
    def not_testicle_size_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="not_length",
                is_temp=True,
                on_match="not_testicle_size_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 g ",
                ],
            ),
        ]

    @classmethod
    def testicle_position_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="position",
                is_temp=True,
                on_match="testicle_position_match",
                decoder=cls.decoder,
                patterns=[
                    " non - fully descended ",
                    " abdominal ",
                    " abdominal , non - descended ",
                    " abdominal descended ",
                    " ing ",
                    " non - descended ",
                    " fully - descended ",
                    " partially descended ",
                    " descended ",
                ],
            ),
        ]

    @classmethod
    def testicle_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="description",
                is_temp=True,
                on_match="testicle_description_match",
                decoder=cls.decoder,
                patterns=[
                    " size ",
                    " size , non - descended ",
                    " size , descended ",
                ],
            ),
        ]

    @classmethod
    def testicle_pos_alone_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="pos_alone",
                on_match="pos_alone_match",
                is_temp=True,
                decoder=cls.decoder,
                patterns=[
                    " scrotal ",
                    " non - scrotal ",
                ],
            ),
        ]

    @classmethod
    def testicle_state_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="testicle",
                on_match="testicle_state_match",
                decoder=cls.decoder,
                patterns=[
                    " non testes ",
                    "            alone ",
                    "     testes alone ",
                    "     testes descr ",
                    "     testes pos ",
                    "     testes descr , and , descr ",
                    "     testes descr , and , pos ",
                    "     testes pos   , and , descr ",
                    "     testes descr ,       descr ",
                    "     testes descr ,       pos ",
                    "     testes pos   ,       descr ",
                ],
            ),
        ]

    @classmethod
    def testicle_size_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="testicle",
                on_match="testicle_size_match",
                decoder=cls.decoder,
                patterns=[
                    " testes , side , 9 mm ",
                    " testes , side , 9 mm , descr ",
                    " testes , side , 9 mm , pos ",
                    " testes , side , 9 mm , alone ",
                    " testes , side , 9 mm x 9 mm ",
                    " testes , side , 9 mm x 9 mm and 9 mm x 9 mm ",
                    " testes , side , 9 mm x 9 mm , alone ",
                    " testes , side , 9 mm x 9 mm , descr ",
                    " testes , side , 9 mm x 9 mm , pos ",
                    " testes , descr , abbrev , 9 mm ",
                    " testes , pos   , abbrev , 9 mm ",
                    " testes , descr , abbrev , 9 mm x 9 mm ",
                    " testes , pos   , abbrev , 9 mm x 9 mm ",
                    " testes , alone , abbrev , 9 mm ",
                    " testes , alone , abbrev , 9 mm x 9 mm ",
                    " alone , abbrev , 9 mm x 9 mm ",
                    " testes , x 9 mm ",
                    " testes ,   9 mm , pos ",
                    " testes ,   9 mm , descr ",
                    " testes ,   9 mm , alone ",
                ],
            ),
        ]

    @classmethod
    def testicle_double_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="testicle",
                on_match="testicle_double_match",
                decoder=cls.decoder,
                patterns=[
                    " testes , left , 9 mm , right   9 mm ",
                    " testes , left , 9 mm , right x 9 mm ",
                ],
            ),
        ]

    @classmethod
    def in_millimeters(cls, number: Span, units: Span | str | None) -> float:
        units_ = ""
        if isinstance(units, str):
            units_ = units.lower()
        elif units is None:
            units_ = ""
        elif hasattr(units, "text"):
            units_ = units.text.lower()

        factor = cls.factor_mm.get(units_, 1.0)
        value = factor * number._.trait.number
        return round(value, 2)

    @classmethod
    def not_testicle_size_match(cls, ent: Span) -> "Testicle":
        return cls.from_ent(ent)

    @classmethod
    def testicle_position_match(cls, ent: Span) -> "Testicle":
        return cls.from_ent(ent)

    @classmethod
    def testicle_description_match(cls, ent: Span) -> "Testicle":
        return cls.from_ent(ent)

    @classmethod
    def pos_alone_match(cls, ent: Span) -> "Testicle":
        return cls.from_ent(ent)

    @classmethod
    def testicle_state_match(cls, ent: Span) -> "Testicle":
        data = {}
        pos, descr = cls.get_pos_and_descr(ent, fill=True)
        data["position"] = pos
        data["description"] = descr
        return cls.from_ent(ent, **data)

    @classmethod
    def testicle_size_match(cls, ent: Span) -> "Testicle":
        data = {}
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        pos, descr = cls.get_pos_and_descr(ent)

        nums = [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]
        if not nums:
            raise RejectMatch

        one_pair = 2
        two_pairs = 4

        data["length"] = nums[0]
        data["width"] = nums[1] if len(nums) > 1 else None
        data["length2"] = nums[2] if len(nums) > one_pair else None
        data["width2"] = nums[3] if len(nums) >= two_pairs else None

        data["position"] = pos
        data["description"] = descr

        data["units_inferred"] = True if units is None else None

        return cls.from_ent(ent, **data)

    @classmethod
    def testicle_double_match(cls, ent: Span) -> "Testicle":
        data = {}
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        pos, descr = cls.get_pos_and_descr(ent)

        nums = [cls.in_millimeters(e, units) for e in ent.ents if e.label_ == "number"]

        data["length"] = nums[0]
        data["length2"] = nums[1] if len(nums) > 1 else None

        data["position"] = pos
        data["description"] = descr

        data["units_inferred"] = True if units is None else None

        return cls.from_ent(ent, **data)

    @classmethod
    def get_pos_and_descr(
        cls, ent: Span, *, fill: bool = False
    ) -> tuple[str | None, str | None]:
        pos = [
            cls.replace.get(e.text.lower(), e.text.lower())
            for e in ent.ents
            if e.label_ in ("position", "pos_alone")
        ]
        pos = " ".join(pos) if pos else None
        descr = [
            cls.replace.get(e.text.lower(), e.text.lower())
            for e in ent.ents
            if e.label_ in ("description", "descr_alone")
        ]
        descr = " ".join(descr) if descr else None
        if fill and pos is None and descr is None:
            descr = ent.text.lower()

        return pos, descr


@registry.misc("testicle_position_match")
def testicle_position_match(ent: Span) -> Testicle:
    return Testicle.testicle_position_match(ent)


@registry.misc("testicle_description_match")
def testicle_description_match(ent: Span) -> Testicle:
    return Testicle.testicle_description_match(ent)


@registry.misc("pos_alone_match")
def pos_alone_match(ent: Span) -> Testicle:
    return Testicle.pos_alone_match(ent)


@registry.misc("testicle_state_match")
def testicle_state_match(ent: Span) -> Testicle:
    return Testicle.testicle_state_match(ent)


@registry.misc("testicle_size_match")
def testicle_size_match(ent: Span) -> Testicle:
    return Testicle.testicle_size_match(ent)


@registry.misc("not_testicle_size_match")
def not_testicle_size_match(ent: Span) -> Testicle:
    return Testicle.not_testicle_size_match(ent)


@registry.misc("testicle_double_match")
def testicle_double_match(ent: Span) -> Testicle:
    return Testicle.testicle_double_match(ent)
