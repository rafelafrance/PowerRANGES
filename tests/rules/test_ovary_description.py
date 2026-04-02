import unittest

from ranges.rules.ovary import Ovary
from tests.setup import parse


class TestOvaryState(unittest.TestCase):
    def test_ovary_description_01(self) -> None:
        self.assertEqual(
            parse("reproductive data=Ovaries and uterus small, immature"),
            [Ovary(description="small, immature", start=18, end=52)],
        )

    def test_ovary_description_02(self) -> None:
        self.assertEqual(
            parse("reproductive data=OVARIES ENLARGED - 7X12 MM"),
            [Ovary(description="enlarged", length=7.0, width=12.0, start=18, end=44)],
        )

    def test_ovary_description_03(self) -> None:
        self.assertEqual(
            parse(
                "reproductive data=ovaries and uterine horns covered with copious fat ;"
            ),
            [Ovary(description="covered with copious fat", start=18, end=68)],
        )

    def test_ovary_description_04(self) -> None:
        self.assertEqual(
            parse("; ovaries mod size;"),
            [Ovary(description="mod size", start=2, end=18)],
        )

    def test_ovary_description_05(self) -> None:
        self.assertEqual(
            parse("reproductive data= +corp. alb both ovaries;"),
            [Ovary(both_sides="+corp. alb", start=19, end=42)],
        )

    def test_ovary_description_06(self) -> None:
        self.assertEqual(
            parse("ovaries: R 2 c. alb, L sev c. alb;"),
            [
                Ovary(left_side="sev c. alb", right_side="2 c. alb", start=0, end=33),
            ],
        )

    def test_ovary_description_07(self) -> None:
        self.assertEqual(
            parse("ovaries immature;"),
            [Ovary(description="immature", start=0, end=16)],
        )

    def test_ovary_description_08(self) -> None:
        self.assertEqual(
            parse("reproductive data=Ovary, fallopian tubes dark red."),
            [Ovary(description="fallopian tubes dark red", start=18, end=49)],
        )

    def test_ovary_description_09(self) -> None:
        self.assertEqual(
            parse(
                "reproductive data=Left ovary=3x1.5mm, pale pink in color; uterus thin"
            ),
            [
                Ovary(
                    left_side="pale pink",
                    length=3.0,
                    width=1.5,
                    start=18,
                    end=47,
                ),
            ],
        )

    def test_ovary_description_10(self) -> None:
        self.assertEqual(
            parse(", ovaries immature (no lg folls) ;"),
            [Ovary(description="immature", start=2, end=18)],
        )

    def test_ovary_description_11(self) -> None:
        self.assertEqual(
            parse("reproductive data=Ovaries and uterus small, immature"),
            [Ovary(description="small, immature", start=18, end=52)],
        )

    def test_ovary_description_12(self) -> None:
        self.assertEqual(
            parse("ovaries mod size;"),
            [Ovary(description="mod size", start=0, end=16)],
        )

    def test_ovary_description_13(self) -> None:
        self.assertEqual(
            parse("reproductive data=Ovaries minute."),
            [Ovary(description="minute", start=18, end=32)],
        )

    def test_ovary_description_14(self) -> None:
        self.assertEqual(
            parse("; both ovaries sev c.alb.;"),
            [Ovary(both_sides="sev c.alb", start=2, end=24)],
        )

    def test_ovary_description_15(self) -> None:
        self.assertEqual(
            parse("reproductive data=pelvis fused, ovaries inactive;"),
            [Ovary(description="inactive", start=32, end=48)],
        )

    def test_ovary_description_16(self) -> None:
        self.assertEqual(
            parse("reproductive data=right ovary destroyed ;"),
            [Ovary(right_side="destroyed", start=18, end=39)],
        )

    def test_ovary_description_17(self) -> None:
        self.assertEqual(
            parse("reproductive data=large ovaries ;"),
            [Ovary(description="large", start=18, end=31)],
        )

    def test_ovary_description_18(self) -> None:
        self.assertEqual(
            parse("ovaries somewhat enlarged"),
            [Ovary(description="somewhat enlarged", start=0, end=25)],
        )

    def test_ovary_description_19(self) -> None:
        self.assertEqual(
            parse("ovaries imm."), [Ovary(description="imm.", start=0, end=12)]
        )

    def test_ovary_description_20(self) -> None:
        self.assertEqual(
            parse("ovaries: both w/sev c. alb;"),
            [Ovary(both_sides="sev c. alb", start=0, end=26)],
        )

    def test_ovary_description_21(self) -> None:
        self.assertEqual(
            parse("corpus luteum visible in both ovaries"),
            [Ovary(both_sides="corpus luteum visible", start=0, end=37)],
        )

    def test_ovary_description_22(self) -> None:
        self.assertEqual(
            parse("reproductive data=only 1 fully developed ovary ;"),
            [Ovary(description="1 fully developed", start=23, end=46)],
        )

    def test_ovary_description_23(self) -> None:
        self.assertEqual(
            parse("ovaries shrunken"),
            [Ovary(description="shrunken", start=0, end=16)],
        )

    def test_ovary_description_24(self) -> None:
        self.assertEqual(
            parse("inactive ovary"),
            [Ovary(description="inactive", start=0, end=14)],
        )

    def test_ovary_description_26(self) -> None:
        self.assertEqual(
            parse("Cyst on ovary"),
            [Ovary(description="cyst", start=0, end=13)],
        )

    def test_ovary_description_27(self) -> None:
        self.assertEqual(
            parse("; 4 bodies in L ovary;"),
            [Ovary(left_side="4 bodies", start=2, end=21)],
        )

    def test_ovary_description_28(self) -> None:
        self.assertEqual(
            parse("Mod. fat, ovaries black"),
            [Ovary(description="black", start=10, end=23)],
        )

    def test_ovary_description_29(self) -> None:
        self.assertEqual(
            parse("ovary not seen"),
            [Ovary(description="not seen", start=0, end=14)],
        )

    def test_ovary_description_30(self) -> None:
        self.assertEqual(
            parse("ovaries pink, fat"),
            [Ovary(description="pink", start=0, end=12)],
        )

    def test_ovary_description_31(self) -> None:
        self.assertEqual(
            parse("Left side of ovaries large and cancerous"),
            [Ovary(left_side="large and cancerous", start=0, end=40)],
        )

    def test_ovary_description_32(self) -> None:
        self.assertEqual(
            parse("ovaries well developed,"),
            [Ovary(description="well developed", start=0, end=22)],
        )

    def test_ovary_description_33(self) -> None:
        self.assertEqual(
            parse("ovaries pink and smooth, fat around base of tail and oviduct"),
            [Ovary(description="pink and smooth", start=0, end=23)],
        )

    def test_ovary_description_34(self) -> None:
        self.assertEqual(
            parse("Yng. 7 blastocysts and 2 ovaries preserved (where?)"),
            [],
        )

    def test_ovary_description_35(self) -> None:
        self.assertEqual(
            parse("both ov w/ few sm foll;"),
            [Ovary(both_sides="few sm foll", start=0, end=22)],
        )

    def test_ovary_description_36(self) -> None:
        self.assertEqual(
            parse("stomach, jaw, claw, ovaries, womb too large to preserve"),
            [],
        )

    def test_ovary_description_37(self) -> None:
        self.assertEqual(
            parse("Rov 3 cl, Lov 4 cl, both ov sm-med foll;"),
            [
                Ovary(
                    both_sides="sm-med foll",
                    left_side="4 cl",
                    right_side="3 cl",
                    start=0,
                    end=39,
                )
            ],
        )
