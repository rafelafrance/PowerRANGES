"""
Parse embryo traits: length and count.

These traits are intermixed in text, and Currently, traiter isn't equipped to deal
with this easily.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.rules import terms as t_terms

from ranges.rules.base_length import DOT, SEP, BaseLength, DictFunc

DECODER = {
    "(": {"TEXT": {"IN": t_const.OPEN}, "OP": "?"},
    ")": {"TEXT": {"IN": t_const.CLOSE}, "OP": "?"},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ",": {"TEXT": {"IN": SEP}, "OP": "{,2}"},
    ".": {"TEXT": {"IN": DOT}, "OP": "{,2}"},
    "1or2": {"TEXT": {"REGEX": r"^[12]$"}},
    "9": {"ENT_TYPE": "number"},
    ":": {"TEXT": {"IN": SEP}, "OP": "{,2}"},
    "=": {"TEXT": {"IN": t_const.EQ}},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "emb_key": {"ENT_TYPE": "embryo_key"},
    "key": {"ENT_TYPE": {"IN": ["len_key", "embryo_key"]}},
    "len_key": {"ENT_TYPE": "len_key"},
    "mm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "present": {"ENT_TYPE": {"IN": ["no", "yes"]}, "OP": "+"},
    "side": {"ENT_TYPE": "side", "OP": "+"},
    "side_word": {"LOWER": "side"},
    "word": {"IS_ALPHA": True, "OP": "{,2}"},
    "x": {"LOWER": {"IN": t_const.CROSS}, "OP": "?"},
    "xx": {"LOWER": {"IN": t_const.CROSS}},
}


@dataclass(eq=False)
class Embryo(BaseLength):
    # Class vars ----------
    name: ClassVar[str] = "embryo"

    csvs: ClassVar[list[Path]] = [
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(__file__).parent / "terms" / "embryo_length_terms.csv",
        Path(__file__).parent / "terms" / "embryo_count_terms.csv",
    ]
    side: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "side")

    factor_cm: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "factor_cm")
    factor_mm: ClassVar[dict[str, float]] = {
        k: float(v) * 10.0 for k, v in factor_cm.items()
    }
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csvs, "replace")
    # ---------------------

    # Length fields are in the parent class
    width: float | None = None
    measured_from: str | None = None

    # Count fields
    count: int | None = None
    right: int | None = None
    left: int | None = None
    female: int | None = None
    male: int | None = None

    def for_csv(self) -> dict[str, Any]:
        value = {}

        if self.length is not None:
            value["embryo_length"] = self.length

        if self.measured_from is not None:
            value["embryo_length_measured_from"] = self.measured_from

        if self.count is not None:
            value["embryo_count"] = self.count

        if self.left is not None:
            value["embryo_count_left"] = self.left

        if self.right is not None:
            value["embryo_count_right"] = self.right

        return value

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="embryo_terms", path=cls.csvs)

        cls.bad_embryo_pipe(nlp)
        cls.bad_length_pipe(nlp)
        cls.embryo_side_pipe(nlp)
        cls.embryo_mix_2_3_pipe(nlp)
        cls.embryo_mix_1_2_pipe(nlp)
        # add.debug_tokens(nlp)  # ###########################################
        cls.embryo_mix_3_pipe(nlp)
        cls.embryo_mix_2_pipe(nlp)
        cls.embryo_mix_1_pipe(nlp)
        cls.embryo_mix_0_pipe(nlp)
        cls.embryo_width_pipe(nlp)
        cls.length_pipe(nlp, label=cls.name)
        cls.embryo_count_pipe(nlp)
        cls.embryo_present_pipe(nlp)
        cls.cleanup_pipe(nlp)

    @classmethod
    def bad_embryo_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="bad_embryo_patterns",
            compiler=cls.bad_embryo_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_count_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="embryo_count_patterns",
            compiler=cls.embryo_count_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_side_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="embryo_side_patterns",
            compiler=cls.embryo_side_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_present_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="embryo_present_patterns",
            compiler=cls.embryo_present_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_0_pipe(cls, nlp: Language) -> None:
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_0_patterns",
            compiler=cls.embryo_mix_0_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_1_pipe(cls, nlp: Language) -> None:
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_patterns",
            compiler=cls.embryo_mix_1_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_1_2_pipe(cls, nlp: Language) -> None:
        """Length is at index 1."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_1_2_patterns",
            compiler=cls.embryo_mix_1_2_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_2_pipe(cls, nlp: Language) -> None:
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_patterns",
            compiler=cls.embryo_mix_2_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_2_3_pipe(cls, nlp: Language) -> None:
        """Length is at index 2."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_2_3_patterns",
            compiler=cls.embryo_mix_2_3_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_mix_3_pipe(cls, nlp: Language) -> None:
        """Length is at index 3."""
        add.trait_pipe(
            nlp,
            name="embryo_mix_3_patterns",
            compiler=cls.embryo_mix_3_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_width_pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="embryo_width_patterns",
            compiler=cls.embryo_width_patterns(),
            overwrite=["number"],
        )

    @classmethod
    def embryo_side_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="side",
                on_match="embryo_side_match",
                is_temp=True,
                decoder=DECODER,
                patterns=[
                    " side ",
                    " side_word 1or2 ",
                ],
            ),
        ]

    @classmethod
    def bad_embryo_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="bad_embryo",
                on_match="bad_embryo_match",
                is_temp=True,
                decoder=DECODER,
                patterns=[
                    " 9 / 9",
                ],
            ),
        ]

    @classmethod
    def embryo_count_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_count_match",
                decoder=DECODER,
                patterns=[
                    "              ( 9 ( side ) , 9 ( side ) : key+ ",
                    "   emb_key+ : ( 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) ",
                    "   emb_key+ : ( 9 ( side ) , 9 ( side ) : 9 ",
                    "   emb_key+ : 9  ",
                    "   emb_key+ : 9 ( side ) x 9 ( side ) ",
                    "   emb_key+ : 9 [+] 9 = 9 ",
                    "   emb_key+ : 9 key* , ( 9 ( side ) , 9 ( side ) ",
                    " 9 present+ emb_key+",
                    " 9 word emb_key+ ",
                    " 9 word emb_key+ , ( side ) , 9 ( side ) ",
                    " 9 word emb_key+ : ( 9 ( side ) , word 9 ( side ) ",
                    " 9 word emb_key+ word ( side ) word , 9 word ( side ) ",
                    " 9 word key+ ( side ) , 9 , word ( side ) , 9 ) ",
                    " 9 emb_key+ ( side =? 9 , side =? 9 ",
                    "   emb_key+ : 9 side 9 side =? 9 ",
                ],
            ),
        ]

    @classmethod
    def embryo_present_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_present_match",
                decoder=DECODER,
                patterns=[
                    "           present word emb_key+ ",
                    "emb_key+ :         ( side ) ",
                    "emb_key+ : present ",
                    "emb_key+ : present ( side ) ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_0_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_0_match",
                decoder=DECODER,
                patterns=[
                    " 9 mm+ , key+ , 9 ( side ) ",
                    " 9 mm+ , key+ , 9 ( side ) , 9 ( side ) ",
                    " 9 mm+ , key+ , 9",
                    " emb_key word side , 9 mm+ len_key ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_1_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_1_match",
                decoder=DECODER,
                patterns=[
                    "      9 key+ ( side ) word , 9 mm* , 9 key+ ( side ) ",
                    "      9 key+ word , 9 mm+ ",
                    "      9 key+ word , 9 mm+ , ( 9 ( side ) , 9 ( side ) ",
                    " ( side ) word 9 : key+ , 9 mm* ",
                    " ( side ) word 9 : key+ , 9 mm* , ( side ) word 9 ",
                    " ( side ) word 9 : key+ x , 9 mm* ",
                    " ( side ) word 9 : key+ x , 9 mm* , ( side ) word 9 ",
                    " 9 9 mm+ key+ ",
                    " 9 9 mm+ key+ , 9 ( side ) , 9 ( side ) ",
                    " emb_key+ ( side ) word , 9 , word ( side ) , key* 9 mm+ ) ",
                    " emb_key+ , 9 , ( side ) ( len_key+ , 9 mm* ) , 9 ( side ) ",
                    " emb_key+ , 9 , len_key+ , 9 mm* ",
                    " emb_key+ , 9 , len_key+ , 9 mm* , 9 ( side ) x 9 ( side ) ",
                    " emb_key+ 9 x 9 ( side ) , 9 , ( side ) 9 ) ",
                    " emb_key+ 9 x 9 ( side ) , 9 , word ( side ) ",
                    " 9 emb_key+ . len_key+ , 9 mm+ ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_1_2_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_1_2_match",
                decoder=DECODER,
                patterns=[
                    "      9 key+ word , 9 x 9 mm+ ",
                    " side 9 key+ word , 9 x 9 mm* , side 9 key+ ",
                    "      9 key+ side word , 9 x 9 mm* , key* 9 side ",
                    "      9 key+ side word , 9 x 9 mm* , key* side 9 ",
                    "      9 key+ side word , 9 x 9 mm* , 9 key* side ",
                    "      9 key+ side word , 9 x 9 mm* ",
                    "      9 key+ word      , 9 x 9 mm+ , ( 9 side , 9 side ) ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_2_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_2_match",
                decoder=DECODER,
                patterns=[
                    " 9 key+ : ( side word , 9 , word side ,     9 mm+ ) ",
                    " 9      :   side word , 9 , word side ,     9 mm+   , key+ ",
                    "            side word , 9 , side word , 9 : 9 mm*   , key+ ",
                    "            side word , 9 , side word , 9 , key+ 9 mm+ ",
                    "   key+ : ( side word , 9 , side word , 9 , key* 9 mm+ ) ",
                    "   key+ : ( side ) word , 9 , ( side ) word , 9 , key* 9 mm+ ",
                    "   key+ : ( 9   side   word , 9 , word   side ,   : 9 mm+ ) ",
                    "   key+ :   9 ( side ) word , 9 , word ( side ) , : 9 mm+ ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_2_3_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_2_3_match",
                decoder=DECODER,
                patterns=[
                    " 9 key+          word , 9 word ( side ) , 9 x 9 mm* ",
                    " 9 key+ ( side ) word , 9 word ( side ) , 9 x 9 mm* ",
                    " 9 key+ ( side ) word , ( 9 word )      , 9 x 9 mm* ",
                ],
            ),
        ]

    @classmethod
    def embryo_mix_3_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_mix_3_match",
                decoder=DECODER,
                patterns=[
                    " 9 key+ : ( 9   side   word , 9 , word   side ,   : 9 mm* ) ",
                    " 9 key+ :   9 ( side ) word , 9 , word ( side ) , : 9 mm* ",
                    " 9      :   9 ( side ) word , 9 , word ( side ) , : 9 mm* , key+ ",
                    " key+ : ( 9 side   word , 9 ,   side   word , 9 , : key* 9 mm* ) ",
                    " key+ :   9 ( side ) word , 9 , ( side ) word , 9 , : key* 9 mm* ",
                    " 9 emb_key+ . 9 side . 9 side . key . 9 mm+ ",
                ],
            ),
        ]

    @classmethod
    def embryo_width_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="embryo",
                on_match="embryo_width_match",
                decoder=DECODER,
                patterns=[
                    "key+ : 9 xx 9 mm* ",
                ],
            ),
        ]

    @classmethod
    def get_sides(cls, ent: Span, counts: list[int]) -> list[str]:
        sides = [e for e in ent.ents if e.label_ == "side"]
        new = []

        for side in sides:
            side = cls.replace.get(side.text.lower(), side.text.lower())

            if side.endswith("1"):
                new.append("side1")
            elif side.endswith("2"):
                new.append("side2")
            elif side.startswith("l"):
                new.append("left")
            elif side.startswith("r"):
                new.append("right")
            elif side.startswith("f"):
                new.append("side1")
            elif side.startswith("m"):
                new.append("side2")
            else:
                new.append(cls.side.get(side.lower(), ""))

        if len(counts) > len(sides):
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
    def get_counts(cls, counts: list[Span]) -> list[int]:
        numbers = [int(c._.trait.number) for c in counts if not c._.trait.is_fraction]
        if len(numbers) == 3:
            if numbers[0] == max(numbers):
                return [numbers[1], numbers[2]]
            if numbers[1] == max(numbers):
                return [numbers[0], numbers[2]]
            return [numbers[0], numbers[1]]
        return numbers

    @classmethod
    def embryo_count_match(cls, ent: Span) -> "Embryo":
        counts = [e for e in ent.ents if e.label_ == "number"]
        counts = cls.get_counts(counts)

        sides = cls.get_sides(ent, counts)

        data = {"count": sum(counts)}
        cls.add_sides(data, counts, sides)

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_present_match(cls, ent: Span) -> "Embryo":
        side_ents = [e for e in ent.ents if e.label_ == "side"]
        side = [cls.side.get(s.text.lower(), "") for s in side_ents]

        count = 1 if any(e.label_ == "yes" for e in ent.ents) or side else 0
        count = 1 if side else count

        data = {"count": count}

        if side:
            data[side[0]] = count

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_mix_match(
        cls, ent: Span, length_idx: int, width_idx: int | None = None
    ) -> "Embryo":
        counts = [e for e in ent.ents if e.label_ == "number"]

        length = counts.pop(length_idx)
        width = counts.pop(width_idx - 1) if width_idx else None

        counts = cls.get_counts(counts)

        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        length = cls.in_millimeters(length, units)
        if width:
            width = cls.in_millimeters(width, units)

        sides = cls.get_sides(ent, counts)

        data = {"count": sum(counts)}
        cls.add_sides(data, counts, sides)

        meas_from = "crown" if any(e.label_ == "len_key" for e in ent.ents) else None

        data |= {
            "_prefix": "embryo",
            "length": length,
            "width": width,
            "measured_from": meas_from,
        }

        cls.add_sides(data, counts, sides)

        return cls.from_ent(ent, **data)

    @classmethod
    def embryo_width_match(cls, ent: Span) -> "Embryo":
        length, width = (e for e in ent.ents if e.label_ == "number")

        meas_from = "crown" if any(e.label_ == "len_key" for e in ent.ents) else None
        units = next((e for e in ent.ents if e.label_ in cls.units), None)
        units_inferred = True if units is None else None

        length = cls.in_millimeters(length, units)
        width = cls.in_millimeters(width, units)

        data = {
            "_prefix": "embryo",
            "length": length,
            "width": width,
            "units_inferred": units_inferred,
            "measured_from": meas_from,
        }

        return cls.from_ent(ent, **data)

    @classmethod
    def bad_embryo_match(cls, ent: Span) -> "Embryo":
        return cls.from_ent(ent)

    @classmethod
    def embryo_side_match(cls, ent: Span) -> "Embryo":
        return cls.from_ent(ent)

    @classmethod
    def to_obj(cls, ent: Span, dict_func: DictFunc) -> "Embryo":
        base = cls.class_dict(ent, dict_func)
        meas_from = "crown" if any(e.label_ == "len_key" for e in ent.ents) else None
        if meas_from:
            base["measured_from"] = "crown"
        return cls(**base)


@registry.misc("embryo_side_match")
def embryo_side_match(ent: Span) -> Embryo:
    return Embryo.embryo_side_match(ent)


@registry.misc("embryo_count_match")
def embryo_count_match(ent: Span) -> Embryo:
    return Embryo.embryo_count_match(ent)


@registry.misc("embryo_present_match")
def embryo_present_match(ent: Span) -> Embryo:
    return Embryo.embryo_present_match(ent)


@registry.misc("embryo_length_match")
def embryo_length_match(ent: Span) -> Embryo:
    return Embryo.to_obj(ent, DictFunc.LENGTH)


@registry.misc("embryo_mix_0_match")
def embryo_mix_0_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=0)


@registry.misc("embryo_mix_1_match")
def embryo_mix_1_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=1)


@registry.misc("embryo_mix_0_1_match")
def embryo_mix_0_1_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=0, width_idx=1)


@registry.misc("embryo_mix_1_2_match")
def embryo_mix_1_2_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=1, width_idx=2)


@registry.misc("embryo_mix_2_match")
def embryo_mix_2_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=2)


@registry.misc("embryo_mix_2_3_match")
def embryo_mix_2_3_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=2, width_idx=3)


@registry.misc("embryo_mix_3_match")
def embryo_mix_3_match(ent: Span) -> Embryo:
    return Embryo.embryo_mix_match(ent, length_idx=3)


@registry.misc("embryo_length_bad_match")
def embryo_length_bad_match(ent: Span) -> BaseLength:
    return Embryo.bad_match(ent)


@registry.misc("embryo_width_match")
def embryo_width_match(ent: Span) -> Embryo:
    return Embryo.embryo_width_match(ent)


@registry.misc("bad_embryo_match")
def bad_embryo_match(ent: Span) -> Embryo:
    return Embryo.bad_embryo_match(ent)
