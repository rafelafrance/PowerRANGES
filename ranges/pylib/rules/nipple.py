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

SEP = t_const.PLUS + t_const.COLON + t_const.COMMA + ["&"]

DECODER = {
    "%": {"LOWER": {"IN": ["%"]}},
    ",": {"LOWER": {"IN": list(":,.")}, "OP": "?"},
    "9": {"ENT_TYPE": {"IN": ["number", "none"]}},
    "=": {"LOWER": {"IN": t_const.EQ}},
    "[+]": {"LOWER": {"IN": SEP}},
    "any": {},
    "dev": {"ENT_TYPE": "dev", "OP": "+"},
    "enlarged": {"ENT_TYPE": "enlarged", "OP": "+"},
    "mod": {"ENT_TYPE": {"IN": ["visible", "modifier"]}},
    "nipple": {"ENT_TYPE": "nip", "OP": "+"},
    "none": {"ENT_TYPE": "none", "OP": "+"},
    "not_enlarged": {"ENT_TYPE": "not_enlarged", "OP": "+"},
    "side": {"ENT_TYPE": "side"},
    "visible": {"ENT_TYPE": "visible"},
}


@dataclass(eq=False)
class Nipple(Base):
    # Class vars ----------
    csv: ClassVar[list[Path]] = Path(__file__).parent / "terms" / "nipple_terms.csv"
    # ---------------------

    count: int = None
    state: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        if self.count is not None:
            dwc.add_dyn(nippleCount=self.count)

        if self.state is not None:
            dwc.add_dyn(nippleState=self.state)

        return dwc

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="nipple_terms", path=cls.csv)

        add.trait_pipe(
            nlp,
            name="nipple_bad_patterns",
            compiler=cls.nipple_bad_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="nipple_count_enlarged_patterns",
            compiler=cls.nipple_count_enlarged_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="nipple_count_patterns",
            compiler=cls.nipple_count_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="nipple_state_patterns",
            compiler=cls.nipple_state_patterns(),
        )
        # add.debug_tokens(nlp)  # #############################################

        add.cleanup_pipe(nlp, name="nipple_cleanup")
        # add.debug_ents(nlp)  # #############################################

    @classmethod
    def nipple_bad_patterns(cls):
        return [
            Compiler(
                label="bad_nipple_count",
                on_match="nipple_bad_match",
                decoder=DECODER,
                patterns=[
                    " 9 % ",
                    " 9 side ",
                ],
            ),
        ]

    @classmethod
    def nipple_count_patterns(cls):
        return [
            Compiler(
                label="nipple",
                keep="nipple",
                on_match="nipple_count_match",
                decoder=DECODER,
                patterns=[
                    " 9  mod?                     nipple ",
                    " 9  mod? [+] 9 mod?          nipple ",
                    " 9  mod? [+] 9 mod? = 9 mod? nipple ",
                    " nipple , [+]? mod? 9 ",
                    " nipple , [+]? mod? 9 mod? [+] mod? 9 ",
                    " nipple , [+]? mod? 9 mod? [+] mod? 9 mod? = mod? 9 ",
                ],
            ),
        ]

    @classmethod
    def nipple_state_patterns(cls):
        return [
            Compiler(
                label="nipple",
                keep="nipple",
                on_match="nipple_state_match",
                decoder=DECODER,
                patterns=[
                    " nipple ,   enlarged ",
                    " nipple ,   visible ",
                    " enlarged , nipple ",
                    " nipple ,   none ",
                    " none ,     nipple ",
                    " nipple ,   not_enlarged ",
                    " not_enlarged , nipple ",
                    " not_enlarged , none nipple ",
                    " nipple , dev , none ",
                    " enlarged any? any? nipple ",
                    " nipple   any? any? enlarged ",
                ],
            )
        ]

    @classmethod
    def nipple_count_enlarged_patterns(cls):
        return Compiler(
            label="nipple",
            keep="nipple",
            on_match="nipple_count_enlarged_match",
            decoder=DECODER,
            patterns=[
                " 9  mod?                     nipple enlarged",
                " 9  mod? [+] 9 mod?          nipple enlarged",
                " 9  mod? [+] 9 mod? = 9 mod? nipple enlarged ",
                " 9  mod?                     nipple not_enlarged",
                " 9  mod? [+] 9 mod?          nipple not_enlarged",
                " 9  mod? [+] 9 mod? = 9 mod? nipple not_enlarged ",
                " 9  mod?                     nipple visible",
                " 9  mod? [+] 9 mod?          nipple visible",
                " 9  mod? [+] 9 mod? = 9 mod? nipple visible ",
            ],
        )

    @classmethod
    def get_count(cls, ent) -> int:
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

        return int(count)

    @classmethod
    def get_enlarged(cls, ent) -> str:
        if any(e.label_ == "enlarged" for e in ent.ents):
            return "enlarged"

        if any(e.label_ == "not_enlarged" for e in ent.ents):
            return "not enlarged"

        if any(e.label_ == "visible" for e in ent.ents):
            return "enlarged"

        return "not enlarged"

    @classmethod
    def nipple_count_match(cls, ent):
        return cls.from_ent(ent, count=cls.get_count(ent))

    @classmethod
    def nipple_bad_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def nipple_state_match(cls, ent):
        return cls.from_ent(ent, state=cls.get_enlarged(ent))

    @classmethod
    def nipple_count_enlarged_match(cls, ent):
        return cls.from_ent(
            ent,
            count=cls.get_count(ent),
            state=cls.get_enlarged(ent),
        )


@registry.misc("nipple_count_match")
def nipple_count_match(ent):
    return Nipple.nipple_count_match(ent)


@registry.misc("nipple_bad_match")
def nipple_bad_match(ent):
    return Nipple.nipple_bad_match(ent)


@registry.misc("nipple_state_match")
def nipple_state_match(ent):
    return Nipple.nipple_state_match(ent)


@registry.misc("nipple_count_enlarged_match")
def nipple_count_enlarged_match(ent):
    return Nipple.nipple_count_enlarged_match(ent)
