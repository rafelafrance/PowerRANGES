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
class Nipple(Base):
    # Class vars ----------y
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
        "nipple": {"ENT_TYPE": "nip", "OP": "+"},
        "none": {"ENT_TYPE": "none"},
        "side": {"ENT_TYPE": "side"},
        "state": {"ENT_TYPE": "state", "OP": "+"},
    }
    # ---------------------

    count: int = None
    state: str = None

    def to_dict(self) -> dict[str, dict[str, Any]]:
        value = defaultdict(dict)

        if self.count is not None:
            value["nipple_count"] |= {"nipple_count": self.count}
            value["nipple_count"]["_parser"] = self.__class__.__name__

        if self.state:
            value["nipple_state"] |= {"nipple_state": self.state}
            value["nipple_state"]["_parser"] = self.__class__.__name__

        return value

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
            name="nipple_count_state_patterns",
            compiler=cls.nipple_count_state_patterns(),
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

    @classmethod
    def nipple_bad_patterns(cls):
        return [
            Compiler(
                label="bad_nipple_count",
                on_match="nipple_bad_match",
                decoder=cls.decoder,
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
                decoder=cls.decoder,
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
                decoder=cls.decoder,
                patterns=[
                    " none? state  any? any? nipple ",
                    " none? nipple any? any? state ",
                    "       nipple any? any? state , none",
                    " none  nipple ",
                ],
            )
        ]

    @classmethod
    def nipple_count_state_patterns(cls):
        return Compiler(
            label="nipple",
            keep="nipple",
            on_match="nipple_count_state_match",
            decoder=cls.decoder,
            patterns=[
                " 9  mod?                     nipple state  ",
                " 9  mod? [+] 9 mod?          nipple state  ",
                " 9  mod? [+] 9 mod? = 9 mod? nipple state  ",
                " 9  mod?                     state  nipple ",
                " 9  mod? [+] 9 mod?          state  nipple ",
                " 9  mod? [+] 9 mod? = 9 mod? state  nipple ",
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
        elif neg and len(states) == 0:
            states = ["none"]
        return " ".join(states) if states else None

    @classmethod
    def nipple_count_match(cls, ent):
        return cls.from_ent(ent, count=cls.get_count(ent))

    @classmethod
    def nipple_bad_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def nipple_state_match(cls, ent):
        return cls.from_ent(ent, state=cls.get_state(ent))

    @classmethod
    def nipple_count_state_match(cls, ent):
        return cls.from_ent(
            ent,
            count=cls.get_count(ent),
            state=cls.get_state(ent),
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


@registry.misc("nipple_count_state_match")
def nipple_count_state_match(ent):
    return Nipple.nipple_count_state_match(ent)
