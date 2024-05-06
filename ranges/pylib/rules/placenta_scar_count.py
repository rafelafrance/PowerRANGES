from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import RejectMatch
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class PlacentalScarCount(Base):
    # Class vars ----------y
    csv: ClassVar[list[Path]] = (
        Path(__file__).parent / "terms" / "placental_scar_count_terms.csv"
    )

    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csv, "replace")

    sep: ClassVar[list[str]] = t_const.PLUS + t_const.COLON + t_const.COMMA + ["&"]

    decoder: ClassVar[dict[str, Any]] = {
        "%": {"LOWER": {"IN": ["%"]}},
        ",": {"LOWER": {"IN": list(":,.")}, "OP": "?"},
        "9": {"ENT_TYPE": {"IN": ["number"]}},
        "=": {"ENT_TYPE": "eq"},
        "[+]": {"LOWER": {"IN": sep}},
        "adj": {"ENT_TYPE": "adj", "OP": "*"},
        "plac_scar": {"ENT_TYPE": "plac_scar", "OP": "+"},
        "side": {"ENT_TYPE": "side", "OP": "+"},
    }
    # ---------------------

    present: bool = None

    # Count fields
    count: int = None
    left: int = None
    right: int = None
    female: int = None
    male: int = None
    side1: int = None
    side2: int = None

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

        if self.female is not None:
            value |= {"placentalScarCountFemale": self.female}

        if self.male is not None:
            value |= {"placentalScarCountMale": self.male}

        if self.side1 is not None:
            value |= {"placentalScarCountSide1": self.side1}

        if self.side2 is not None:
            value |= {"placentalScarCountSide2": self.side2}

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
            name="placental_scar_count_patterns",
            compiler=cls.placental_scar_count_patterns(),
            overwrite=["number"],
        )

        add.debug_tokens(nlp)  # #############################################

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
                ],
            ),
        ]

    @classmethod
    def placental_scar_count_patterns(cls):
        return [
            Compiler(
                label="placental_scar_count",
                keep="placental_scar_count",
                on_match="placental_scar_count_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 adj plac_scar ",
                    " 9 adj plac_scar , 9 side , 9 side ",
                ],
            ),
        ]

    @classmethod
    def get_count(cls, ent) -> int:
        nums = [t._.trait.number for t in ent if t._.flag == "number"]

        if len(nums) == 0:
            return 0

        if len(nums) == 1:
            count = nums[0]
        elif len(nums) == 2:  # noqa: PLR2004
            count = sum(nums)
        else:
            count = nums[-1]

        if count != int(count):
            raise RejectMatch

        return int(count)

    @classmethod
    def placental_scar_bad_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def placental_scar_count_match(cls, ent):
        count = cls.get_count(ent)
        if count < 1:
            count = None
        present = count > 0
        return cls.from_ent(ent, count=count, present=present)


@registry.misc("placental_scar_count_match")
def placental_scar_count_match(ent):
    return PlacentalScarCount.placental_scar_count_match(ent)


@registry.misc("placental_scar_bad_match")
def placental_scar_bad_match(ent):
    return PlacentalScarCount.placental_scar_bad_match(ent)
