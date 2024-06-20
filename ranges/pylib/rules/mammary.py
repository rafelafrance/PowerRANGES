from collections import defaultdict
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

from ranges.pylib.rules.base import Base


@dataclass(eq=False)
class Mammary(Base):
    # Class vars ----------
    csv: ClassVar[list[Path]] = Path(__file__).parent / "terms" / "mammary_terms.csv"

    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csv, "replace")

    sep: ClassVar[list[str]] = t_const.PLUS + t_const.COLON + t_const.COMMA + ["&"]

    decoder: ClassVar[dict[str, Any]] = {
        "%": {"LOWER": {"IN": ["%"]}},
        ",": {"LOWER": {"IN": list(":,.")}, "OP": "?"},
        "9": {"ENT_TYPE": {"IN": ["number", "none"]}},
        "=": {"ENT_TYPE": "eq"},
        "[+]": {"LOWER": {"IN": sep}},
        "any": {},
        "dev": {"ENT_TYPE": "dev", "OP": "+"},
        "mod": {"ENT_TYPE": "modifier"},
        "mammary": {"ENT_TYPE": "mammaries", "OP": "+"},
        "none": {"ENT_TYPE": "none"},
        "side": {"ENT_TYPE": "side"},
        "state": {"ENT_TYPE": "state", "OP": "+"},
    }
    # ---------------------

    count: int = None
    state: str = None

    def labeled(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        if self.count is not None:
            value["mammary_count"] |= {"mammary_count": self.count}

        if self.state:
            value["mammary"] |= {"mammary": self.state}

        return value

    def to_dwc(self, dwc) -> DarwinCore:
        if self.count is not None:
            dwc.add_dyn(mammaryCount=self.count)

        if self.state is not None:
            dwc.add_dyn(mammaryState=self.state)

        return dwc

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="mammary_terms", path=cls.csv)

        add.trait_pipe(
            nlp,
            name="mammary_bad_patterns",
            compiler=cls.mammary_bad_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="mammary_count_state_patterns",
            compiler=cls.mammary_count_state_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="mammary_count_patterns",
            compiler=cls.mammary_count_patterns(),
            overwrite=["number"],
        )

        add.trait_pipe(
            nlp,
            name="mammary_state_patterns",
            compiler=cls.mammary_state_patterns(),
        )
        # add.debug_tokens(nlp)  # #############################################

        add.cleanup_pipe(nlp, name="mammary_cleanup")

    @classmethod
    def mammary_bad_patterns(cls):
        return [
            Compiler(
                label="bad_mammary_count",
                on_match="mammary_bad_match",
                decoder=cls.decoder,
                patterns=[
                    " 9 % ",
                    " 9 side ",
                ],
            ),
        ]

    @classmethod
    def mammary_count_patterns(cls):
        return [
            Compiler(
                label="mammary",
                keep="mammary",
                on_match="mammary_count_match",
                decoder=cls.decoder,
                patterns=[
                    " 9  mod?                     mammary ",
                    " 9  mod? [+] 9 mod?          mammary ",
                    " 9  mod? [+] 9 mod? = 9 mod? mammary ",
                    " mammary , [+]? mod? 9 ",
                    " mammary , [+]? mod? 9 mod? [+] mod? 9 ",
                    " mammary , [+]? mod? 9 mod? [+] mod? 9 mod? = mod? 9 ",
                ],
            ),
        ]

    @classmethod
    def mammary_state_patterns(cls):
        return [
            Compiler(
                label="mammary",
                keep="mammary",
                on_match="mammary_state_match",
                decoder=cls.decoder,
                patterns=[
                    " none? state  any? any? mammary ",
                    " none? mammary any? any? state ",
                    "       mammary any? any? state , none",
                    " none  mammary ",
                ],
            )
        ]

    @classmethod
    def mammary_count_state_patterns(cls):
        return Compiler(
            label="mammary",
            keep="mammary",
            on_match="mammary_count_state_match",
            decoder=cls.decoder,
            patterns=[
                " 9  mod?                     mammary state  ",
                " 9  mod? [+] 9 mod?          mammary state  ",
                " 9  mod? [+] 9 mod? = 9 mod? mammary state  ",
                " 9  mod?                     state  mammary ",
                " 9  mod? [+] 9 mod?          state  mammary ",
                " 9  mod? [+] 9 mod? = 9 mod? state  mammary ",
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
    def get_state(cls, ent) -> str | None:
        states = [e.text.lower() for e in ent.ents if e.label_ == "state"]
        states = [cls.replace.get(s, s) for s in states]
        neg = next((e.text.lower() for e in ent.ents if e.label_ == "none"), None)
        if neg and states:
            neg = cls.replace.get(neg, neg)
            states = [f"{neg} {s}" for s in states]
        return " ".join(states) if states else None

    @classmethod
    def mammary_count_match(cls, ent):
        return cls.from_ent(ent, count=cls.get_count(ent))

    @classmethod
    def mammary_bad_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def mammary_state_match(cls, ent):
        return cls.from_ent(ent, state=cls.get_state(ent))

    @classmethod
    def mammary_count_state_match(cls, ent):
        return cls.from_ent(
            ent,
            count=cls.get_count(ent),
            state=cls.get_state(ent),
        )


@registry.misc("mammary_count_match")
def mammary_count_match(ent):
    return Mammary.mammary_count_match(ent)


@registry.misc("mammary_bad_match")
def mammary_bad_match(ent):
    return Mammary.mammary_bad_match(ent)


@registry.misc("mammary_state_match")
def mammary_state_match(ent):
    return Mammary.mammary_state_match(ent)


@registry.misc("mammary_count_state_match")
def mammary_count_state_match(ent):
    return Mammary.mammary_count_state_match(ent)
