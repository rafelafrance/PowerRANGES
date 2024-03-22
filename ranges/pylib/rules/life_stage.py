import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class LifeStage(Base):
    # Class vars ----------
    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_time_terms.csv",
        Path(t_terms.__file__).parent / "numeric_terms.csv",
        Path(__file__).parent / "terms" / "life_stage_terms.csv",
    ]
    eq: ClassVar[list[str]] = t_const.COLON + t_const.DASH + t_const.EQ
    dash: ClassVar[list[str]] = t_const.DASH + t_const.SLASH

    eq_re: ClassVar[re.Pattern] = re.compile(rf'^\s*({"|".join(eq)})\s*')
    dash_re: ClassVar[re.Pattern] = re.compile(rf'\s*({"|".join(dash)})\s*')

    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    life_stage: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(lifeStage=self.life_stage)

    @classmethod
    def pipe(cls, nlp):
        add.term_pipe(nlp, name="life_stage_terms", path=cls.csvs)
        add.trait_pipe(
            nlp,
            name="life_stage_patterns",
            compiler=cls.life_stage_patterns(),
            overwrite=""" number ordinal ordinal_suffix time_units """.split(),
        )
        # add.debug_tokens(nlp)  # ############################################
        add.cleanup_pipe(nlp, name="life_stage_cleanup")

    @classmethod
    def life_stage_patterns(cls):
        return Compiler(
            label="life_stage",
            keep="life_stage",
            on_match="life_stage_match",
            decoder={
                "99": {"ENT_TYPE": "number", "OP": "+"},
                "-": {"TEXT": {"IN": cls.dash}, "OP": "?"},
                "=": {"TEXT": {"IN": cls.eq}, "OP": "?"},
                "intrinsic": {"ENT_TYPE": "intrinsic", "OP": "+"},
                "key": {"ENT_TYPE": "key", "OP": "+"},
                "ordinal": {"ENT_TYPE": "ordinal", "OP": "+"},
                "prefix": {"ENT_TYPE": "key_prefix", "OP": "+"},
                "th": {"LOWER": {"IN": ["nd", "rd", "st", "th"]}},
                "time": {"ENT_TYPE": "time_units", "OP": "?"},
                "word": {"IS_ALPHA": True},
            },
            patterns=[
                "       intrinsic ",
                "       intrinsic - intrinsic ",
                "       word      - intrinsic ",
                "       99 th     - time ",
                " key = 99 th     - time ",
                " key = intrinsic ",
                " key = intrinsic - intrinsic ",
                " key = word      - intrinsic ",
                " key = 99 th     - time ",
                " key = ordinal   - time ",
                " key = time      - time ",  # To handle "second"
            ],
        )

    @classmethod
    def life_stage_match(cls, ent):
        life_stage = [t.lower_ for t in ent if t.ent_type_ != "key"]
        life_stage = " ".join(life_stage)
        life_stage = cls.eq_re.sub("", life_stage)
        life_stage = cls.dash_re.sub(r"\1", life_stage, count=1)
        life_stage = re.sub(r"\s\.$", ".", life_stage)
        life_stage = re.sub(r"(\d)\s(th|st|nd|rd)", r"\1\2", life_stage, flags=re.I)
        return cls.from_ent(ent, life_stage=life_stage)


@registry.misc("life_stage_match")
def life_stage_match(ent):
    return LifeStage.life_stage_match(ent)
