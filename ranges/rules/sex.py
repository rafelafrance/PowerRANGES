from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler

from ranges.rules.base import Base


@dataclass(eq=False)
class Sex(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "sex_terms.csv",
    ]
    colon: ClassVar[list] = t_const.COLON + t_const.DASH + t_const.EQ

    sex_labels: ClassVar[list[str]] = ["sex", "sex_unknown", "sex_abbrev"]

    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    sex: str | None = None

    def as_dict(self) -> dict[str, dict[str, Any]]:
        return {
            "sex": {
                "sex": self.sex,
                "_parser": self.__class__.__name__,
            }
        }

    def to_dwc(self, dwc: DarwinCore) -> DarwinCore:
        return dwc.add(sex=self.sex)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sex_terms", path=cls.csvs)
        # add.debug_tokens(nlp)  # ##################################################
        add.trait_pipe(
            nlp,
            name="sex_patterns",
            compiler=cls.sex_patterns(),
            overwrite=["sex"],
        )
        add.cleanup_pipe(nlp, name="sex_cleanup")

    @classmethod
    def sex_patterns(cls) -> Compiler:
        return Compiler(
            label="sex",
            on_match="sex_match",
            decoder={
                ":": {"TEXT": {"IN": cls.colon}, "OP": "?"},
                "[?]": {"TEXT": {"IN": t_const.Q_MARK}},
                "abbrev": {"ENT_TYPE": "sex_abbrev"},
                "key": {"ENT_TYPE": "sex_key", "OP": "+"},
                "sex": {"ENT_TYPE": "sex"},
                "unknown": {"ENT_TYPE": "sex_unknown", "OP": "+"},
            },
            patterns=[
                " key : sex     [?]? ",
                " key : unknown [?]? ",
                " key : abbrev  [?]? ",
                "       sex     [?]? ",
            ],
        )

    @classmethod
    def sex_match(cls, ent: Span) -> "Sex":
        sex = " ".join(t.lower_ for t in ent if t.ent_type_ in cls.sex_labels)
        sex = cls.replace.get(sex, sex)
        q_mark = "?" if "?" in ent.text else ""
        return cls.from_ent(ent, sex=sex + q_mark)


@registry.misc("sex_match")
def sex_match(ent: Span) -> Sex:
    return Sex.sex_match(ent)
