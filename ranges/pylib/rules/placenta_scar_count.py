from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class PlacentalScarCount(Base):
    # Class vars ----------y
    csv: ClassVar[list[Path]] = (
        Path(__file__).parent / "terms" / "placental_scar_count_terms.csv"
    )

    sides: ClassVar[list[str]] = ["both", "left", "right"]
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
        "9": {"ENT_TYPE": {"IN": ["number"]}},
        "=": {"ENT_TYPE": "eq", "OP": "?"},
        "absent": {"ENT_TYPE": "absent", "OP": "+"},
        "adj": {"ENT_TYPE": "adj", "OP": "*"},
        "bad": {"ENT_TYPE": "bad", "OP": "+"},
        "plac_scar": {"ENT_TYPE": "plac_scar", "OP": "+"},
        "side": {"ENT_TYPE": {"IN": sides}, "OP": "+"},
    }
    # ---------------------

    present: bool = None

    # Count fields
    count: int = None
    left: int = None
    right: int = None
    side1: int = None
    side2: int = None
    both: int = None

    def to_dict(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        if self.present is not None:
            value["placental_scars"] |= {"placental_scars_present": self.present}

        if self.count is not None:
            value["placental_scars"] |= {"placental_scar_count": self.count}

        if self.left is not None:
            value["placental_scars"] |= {"placental_scars_left_side": self.left}

        if self.right is not None:
            value["placental_scars"] |= {"placental_scars_right_side": self.right}

        if self.side1 is not None:
            value["placental_scars"] |= {"placental_scars_side_1": self.side1}

        if self.side2 is not None:
            value["placental_scars"] |= {"placental_scars_side_2": self.side2}

        if self.side2 is not None:
            value["placental_scars"] |= {"placental_scars_both_sides": self.side2}

        return value

    def to_dwc(self, dwc) -> DarwinCore:
        value = {}

        if self.present is not None:
            value |= {"placentalScarsPresent": self.present}

        if self.count is not None:
            value |= {"placentalScarCount": self.count}

        if self.left is not None:
            value |= {"placentalScarCountLeft": self.left}

        if self.right is not None:
            value |= {"placentalScarCountRight": self.right}

        if self.side1 is not None:
            value |= {"placentalScarCountSide1": self.side1}

        if self.side2 is not None:
            value |= {"placentalScarCountSide2": self.side2}

        if self.both is not None:
            value |= {"placentalScarCountBothSides": self.both}

        return dwc.add_dyn(**value)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="placental_scar_terms", path=cls.csv)

        add.trait_pipe(
            nlp,
            name="placental_scar_bad_patterns",
            compiler=cls.placental_scar_bad_patterns(),
            overwrite=["number"],
        )

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

        # add.debug_tokens(nlp)  # #############################################

        add.cleanup_pipe(nlp, name="placental_scar_cleanup")

    @classmethod
    def placental_scar_bad_patterns(cls):
        return [
            Compiler(
                label="bad_placental_scar_count",
                on_match="placental_scar_bad_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 % ",
                    " bad plac_scar ",
                    " plac_scar bad ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_at_0_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_total_at_0_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 adj plac_scar , 9 ( side ) , 9 ( side ) ",
                    " 9 adj plac_scar , 9          , 9          ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_at_2_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_total_at_2_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 side , 9 side , = 9 plac_scar",
                    " 9      , 9      , = 9 plac_scar",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_missing_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
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
    def placental_scar_present_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_present_match",
                decoder=cls.decoder,
                patterns=[
                    " plac_scar ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_absent_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_absent_match",
                decoder=cls.decoder,
                patterns=[
                    " absent plac_scar        ",
                    "        plac_scar absent ",
                ],
            ),
        ]

    @classmethod
    def placental_scar_total_only_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_total_only_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 adj plac_scar ",
                    " plac_scar 9 ",
                ],
            ),
        ]

    @classmethod
    def get_counts(cls, ent) -> list[int]:
        if any(e._.trait.is_fraction for e in ent.ents if e.label_ == "number"):
            raise reject_match.RejectMatch
        nums = [int(t._.trait.number) for t in ent if t._.flag == "number"]
        return nums

    @classmethod
    def get_sides(cls, ent) -> list[str]:
        sides = [e.label_ for e in ent.ents if e.label_ in cls.sides]
        sides += ["side1", "side2"]
        return sides

    @classmethod
    def placental_scar_bad_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def placental_scar_match(cls, ent, total_at=None):
        counts = cls.get_counts(ent)
        sides = cls.get_sides(ent)

        total = sum(counts) if total_at is None else counts.pop(total_at)

        data = {"count": total}
        data |= dict(zip(sides, counts, strict=False))
        data["present"] = total > 0

        return cls.from_ent(ent, **data)

    @classmethod
    def placental_scar_no_counts_match(cls, ent, *, present):
        return cls.from_ent(ent, present=present)


@registry.misc("placental_scar_total_at_0_match")
def placental_scar_total_at_0_match(ent):
    return PlacentalScarCount.placental_scar_match(ent, 0)


@registry.misc("placental_scar_total_only_match")
def placental_scar_total_only_match(ent):
    return PlacentalScarCount.placental_scar_match(ent, 0)


@registry.misc("placental_scar_total_at_2_match")
def placental_scar_total_at_2_match(ent):
    return PlacentalScarCount.placental_scar_match(ent, 2)


@registry.misc("placental_scar_total_missing_match")
def placental_scar_total_missing_match(ent):
    return PlacentalScarCount.placental_scar_match(ent)


@registry.misc("placental_scar_present_match")
def placental_scar_present_match(ent):
    return PlacentalScarCount.placental_scar_no_counts_match(ent, present=True)


@registry.misc("placental_scar_absent_match")
def placental_scar_absent_match(ent):
    return PlacentalScarCount.placental_scar_no_counts_match(ent, present=False)


@registry.misc("placental_scar_bad_match")
def placental_scar_bad_match(ent):
    return PlacentalScarCount.placental_scar_bad_match(ent)
