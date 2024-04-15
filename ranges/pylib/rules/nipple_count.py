from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import RejectMatch
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class NippleCount(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "nipple_terms.csv",
        Path(__file__).parent / "terms" / "nipple_count_terms.csv",
    ]
    # ---------------------

    count: int = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(nippleCount=self.count)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="nipple_count_terms", path=cls.csvs)

        add.trait_pipe(
            nlp,
            name="bad_nipple_count_patterns",
            compiler=cls.bad_nipple_count_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="nipple_count_patterns",
            compiler=cls.nipple_count_patterns(),
            overwrite=["number"],
        )
        # add.debug_tokens(nlp)  # #############################################
        add.cleanup_pipe(nlp, name="nipple_count_cleanup")

    @classmethod
    def bad_nipple_count_patterns(cls):
        return [
            Compiler(
                label="bad_nipple_count",
                on_match="bad_nipple_count_match",
                decoder={
                    "9": {"ENT_TYPE": {"IN": ["number", "none"]}},
                    "%": {"LOWER": {"IN": ["%"]}},
                    "side": {"ENT_TYPE": "side"},
                },
                patterns=[
                    " 9 % ",
                    " 9 side ",
                ],
            ),
        ]

    @classmethod
    def nipple_count_patterns(cls):
        sep = t_const.PLUS + t_const.COLON + t_const.COMMA + ["&"]

        return [
            Compiler(
                label="nipple_count",
                keep="nipple_count",
                on_match="nipple_count_match",
                decoder={
                    "9": {"ENT_TYPE": {"IN": ["number", "none"]}},
                    "[+]": {"LOWER": {"IN": sep}},
                    "=": {"LOWER": {"IN": t_const.EQ}},
                    "mod": {"ENT_TYPE": {"IN": ["visible", "modifier"]}},
                    "nipple": {"ENT_TYPE": "nipple"},
                },
                patterns=[
                    " 9  mod?                     nipple ",
                    " 9  mod? [+] 9 mod?          nipple ",
                    " 9  mod? [+] 9 mod? = 9 mod? nipple ",
                    " nipple [+]? mod? 9 ",
                    " nipple [+]? mod? 9 mod? [+] mod? 9 ",
                    " nipple [+]? mod? 9 mod? [+] mod? 9 mod? = mod? 9 ",
                ],
            ),
        ]

    @classmethod
    def nipple_count_match(cls, ent):
        nums = [t._.trait.number for t in ent if t._.flag == "number"]

        if len(nums) == 0:
            raise RejectMatch

        if len(nums) == 1:
            count = nums[0]
        elif len(nums) == 2:  # noqa: PLR2004
            count = sum(nums)
        else:
            count = nums[-1]

        if count != int(count):
            raise RejectMatch

        return cls.from_ent(ent, count=int(count))

    @classmethod
    def bad_nipple_count_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("nipple_count_match")
def nipple_count_match(ent):
    return NippleCount.nipple_count_match(ent)


@registry.misc("bad_nipple_count_match")
def bad_nipple_count_match(ent):
    return NippleCount.bad_nipple_count_match(ent)
