from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from ranges.rules.base import Base


@dataclass(eq=False)
class PlacentalScarCount(Base):
    # Class vars ----------y
    csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "placental_scar_count_terms.csv"
    )

    sides: ClassVar[list[str]] = ["both", "left", "right", "side1", "side2"]
    sep: ClassVar[list[str]] = (
        t_const.DASH
        + t_const.PLUS
        + t_const.COLON
        + t_const.COMMA
        + t_const.DOT
        + ["&"]
    )

    decoder: ClassVar[dict[str, Any]] = {
        "(": {"LOWER": {"IN": t_const.OPEN}, "OP": "?"},
        ")": {"LOWER": {"IN": t_const.CLOSE}, "OP": "?"},
        "%": {"LOWER": {"IN": ["%"]}},
        ",": {"LOWER": {"IN": sep}, "OP": "?"},
        "1or2": {"TEXT": {"REGEX": r"^[12]$"}},
        "9": {"ENT_TYPE": {"IN": ["number"]}},
        "=": {"ENT_TYPE": "eq", "OP": "?"},
        "absent": {"ENT_TYPE": "absent", "OP": "+"},
        "adj": {"ENT_TYPE": "adj", "OP": "*"},
        "bad": {"ENT_TYPE": "bad", "OP": "+"},
        "plac_scar": {"ENT_TYPE": "plac_scar", "OP": "+"},
        "side": {"ENT_TYPE": "side", "OP": "+"},
        "side_word": {"LOWER": "side"},
        "on": {"LOWER": {"IN": ["on", "of"]}},
    }

    side: ClassVar[dict[str, str]] = term_util.look_up_table(csv, "side")
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csv, "replace")
    # ---------------------

    present: bool | None = None

    # Count fields
    count: int | None = None
    left: int | None = None
    right: int | None = None

    def for_csv(self) -> dict[str, Any]:
        value = {}

        if self.present is not None:
            value["placental_scars_present"] = self.present

        if self.count is not None:
            value["placental_scar_count"] = self.count

        if self.left is not None:
            value["placental_scars_left"] = self.left

        if self.right is not None:
            value["placental_scars_right"] = self.right

        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="placental_scar_terms", path=cls.csv)

        add.trait_pipe(
            nlp,
            name="placental_scar_bad_patterns",
            compiler=cls.placental_scar_bad_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_side_patterns",
            compiler=cls.placental_scar_side_patterns(),
            overwrite=["number"],
        )

        # add.debug_tokens(nlp)  # #############################################
        add.trait_pipe(
            nlp,
            name="placental_scar_count_at_0_patterns",
            compiler=cls.placental_scar_total_at_0_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_total_at_2_patterns",
            compiler=cls.placental_scar_total_at_2_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_total_missing_patterns",
            compiler=cls.placental_scar_total_missing_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_total_only_patterns",
            compiler=cls.placental_scar_total_only_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_absent_patterns",
            compiler=cls.placental_scar_absent_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="placental_scar_present_patterns",
            compiler=cls.placental_scar_present_patterns(),
            overwrite=["number"],
        )

        add.cleanup_pipe(nlp, name="placental_scar_cleanup")

    @classmethod
    def placental_scar_side_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="side",
                on_match="placental_scar_side_match",
                is_temp=True,
                decoder=cls.decoder,
                patterns=[
                    "    side ",
                    "    side_word 1or2 ",
                    " on side_word 1or2 ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_bad_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="bad_placental_scar_count",
                on_match="placental_scar_bad_match",
                is_temp=True,
                decoder=cls.decoder,
                patterns=[
                    " 9 % ",
                    " bad plac_scar ",
                    " plac_scar bad ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_at_0_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_total_at_0_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 adj plac_scar , 9 ( side ) , 9 ( side ) ",
                    " 9 adj plac_scar , 9          , 9          ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_at_2_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_total_at_2_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 side , 9 side , = 9 plac_scar",
                    " 9      , 9      , = 9 plac_scar",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_missing_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_total_missing_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 side ,  9 side , plac_scar ",
                    " 9      ,  9      , plac_scar ",
                    " plac_scar 9      , 9      ",
                    " plac_scar 9 side , 9 side ",
                    " plac_scar , 9 side          ",
                    " plac_scar = 9 side          ",
                    " 9 plac_scar ,   side   , 9 plac_scar   side ",
                    " 9 plac_scar ,   side   , 9             side ",
                    "   plac_scar , 9 side   ,             9 side ",
                    "   plac_scar , 9 side   ,   plac_scar 9 side ",
                    "   plac_scar ,   side 9 ,   plac_scar   side 9 ",
                    " side 9 , adj plac_scar , side 9 , adj plac_scar ",
                    " 9 side adj plac_scar , 9 side ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_present_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_present_match",
                decoder=cls.decoder,
                patterns=[
                    " plac_scar ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_absent_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_absent_match",
                decoder=cls.decoder,
                patterns=[
                    " absent plac_scar        ",
                    "        plac_scar absent ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_only_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="placental_scar_count",
                on_match="placental_scar_total_only_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 adj plac_scar ",
                    " plac_scar 9 ",
                ],
            ),
        ]

    @classmethod
    def get_sides(cls, ent: Span, counts: list[int]) -> list[str]:
        sides = [e for e in ent.ents if e.label_ == "side"]
        new = []
        if not sides:
            new.append("side1")

        for side in sides:
            side = cls.replace.get(side.text.lower(), side.text)

            if side.endswith("1"):
                new.append("side1")
            elif side.endswith("2"):
                new.append("side2")
            elif side.startswith("l"):
                new.append("left")
            elif side.startswith("r"):
                new.append("right")
            else:
                new.append(cls.side.get(side.lower(), ""))

        if len(counts) >= len(sides):
            new += ["side1", "side2"]

        return new

    @classmethod
    def add_sides(cls, data: dict, counts: list[int], sides: list[str]) -> None:
        total, left, right = None, None, None
        for count, side in zip(counts, sides, strict=False):
            match side:
                case "both":
                    left = count
                    right = count
                case "side1":
                    total = total or 0
                    total += count
                case "side2":
                    total = total or 0
                    total += count
                case "left":
                    left = count
                case "right":
                    right = count
                case _:
                    raise ValueError(f"Unknown side {side=}")

        if total is not None:
            data["count"] = total
        if left is not None:
            data["left"] = left
        if right is not None:
            data["right"] = right

    @classmethod
    def placental_scar_bad_match(cls, ent: Span) -> "PlacentalScarCount":
        return cls.from_ent(ent)

    @classmethod
    def placental_scar_match(
        cls, ent: Span, total_at: int | None = None
    ) -> "PlacentalScarCount":
        if any(e._.trait.is_fraction for e in ent.ents if e.label_ == "number"):
            raise reject_match.RejectMatch
        counts = [int(e._.trait.number) for e in ent.ents if e.label_ == "number"]
        if total_at is not None and len(counts) > 1:
            counts.pop(total_at)

        sides = cls.get_sides(ent, counts)

        data = {}
        cls.add_sides(data, counts, sides)

        data["present"] = any(c != 0 for c in counts)

        return cls.from_ent(ent, **data)

    @classmethod
    def placental_scar_no_counts_match(
        cls, ent: Span, *, present: bool
    ) -> "PlacentalScarCount":
        return cls.from_ent(ent, present=present)

    @classmethod
    def placental_scar_side_match(cls, ent: Span) -> "PlacentalScarCount":
        return cls.from_ent(ent)


@registry.misc("placental_scar_side_match")
def placental_scar_side_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_side_match(ent)


@registry.misc("placental_scar_total_at_0_match")
def placental_scar_total_at_0_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_match(ent, 0)


@registry.misc("placental_scar_total_only_match")
def placental_scar_total_only_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_match(ent, 0)


@registry.misc("placental_scar_total_at_2_match")
def placental_scar_total_at_2_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_match(ent, 2)


@registry.misc("placental_scar_total_missing_match")
def placental_scar_total_missing_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_match(ent)


@registry.misc("placental_scar_present_match")
def placental_scar_present_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_no_counts_match(ent, present=True)


@registry.misc("placental_scar_absent_match")
def placental_scar_absent_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_no_counts_match(ent, present=False)


@registry.misc("placental_scar_bad_match")
def placental_scar_bad_match(ent: Span) -> PlacentalScarCount:
    return PlacentalScarCount.placental_scar_bad_match(ent)
