import unittest

from ranges.pylib.rules.ovary import Ovary
from tests.setup import parse


class TestOvariesState(unittest.TestCase):
    def test_ovary_state_01(self):
        self.assertEqual(
            parse("reproductive data=Ovaries and uterus small, immature"),
            [Ovary(description="small, immature", start=18, end=52)],
        )

    def test_ovary_state_02(self):
        self.assertEqual(
            parse("reproductive data=OVARIES ENLARGED - 7X12 MM"),
            [Ovary(description="enlarged", length=7.0, width=12.0, start=18, end=44)],
        )

    def test_ovary_state_03(self):
        self.assertEqual(
            parse(
                "reproductive data=ovaries and uterine horns "
                "covered with copious fat ;"
            ),
            [Ovary(description="covered with copious fat", start=18, end=68)],
        )

    def test_ovary_state_04(self):
        self.assertEqual(
            parse("; ovaries mod size;"),
            [Ovary(description="mod size", start=2, end=18)],
        )

    def test_ovary_state_05(self):
        self.assertEqual(
            parse("reproductive data= +corp. alb both ovaries;"),
            [Ovary(both_sides="+corp. alb", start=19, end=42)],
        )

    def test_ovary_state_06(self):
        self.assertEqual(
            parse("ovaries: R 2 c. alb, L sev c. alb;"),
            [
                Ovary(left_side="sev c. alb", right_side="c. alb", start=0, end=33),
            ],
        )

    def test_ovary_state_07(self):
        self.assertEqual(
            parse("ovaries immature;"),
            [Ovary(description="immature", start=0, end=16)],
        )

    def test_ovary_state_08(self):
        self.assertEqual(
            parse("reproductive data=Ovary, fallopian tubes dark red."),
            [Ovary(description="fallopian tubes dark red", start=18, end=49)],
        )

    def test_ovary_state_09(self):
        self.assertEqual(
            parse(
                "reproductive data=Left ovary=3x1.5mm, "
                "pale pink in color; uterus thin"
            ),
            [Ovary(left_side="pale pink", length=3.0, width=1.5, start=18, end=47)],
        )

    def test_ovary_state_10(self):
        self.assertEqual(
            parse(", ovaries immature (no lg folls) ;"),
            [Ovary(description="immature", start=2, end=18)],
        )

    # def test_ovary_state_11(self):
    #     self.assertEqual(
    #         parse("reproductive data=Ovaries and uterus small, immature"),
    #         [Ovary(state="small, immature", start=18, end=52)],
    #     )
    #
    # def test_ovary_state_12(self):
    #     self.assertEqual(
    #         parse("ovaries mod size;"),
    #         [Ovary(state="mod size", start=0, end=16)],
    #     )
    #
    # def test_ovary_state_13(self):
    #     self.assertEqual(
    #         parse("reproductive data=Ovaries minute, not embryos."),
    #         [Ovary(state="minute", start=18, end=32)],
    #     )
    #
    # def test_ovary_state_14(self):
    #     self.assertEqual(
    #         parse("; both ovaries sev c.alb.;"),
    #         [Ovary(state="sev c.alb", side="both", start=2, end=24)],
    #     )
    #
    # def test_ovary_state_15(self):
    #     self.assertEqual(
    #         parse("reproductive data=pelvis fused, ovaries inactive;"),
    #         [Ovary(state="inactive", start=32, end=48)],
    #     )
    #
    # def test_ovary_state_16(self):
    #     self.assertEqual(
    #         parse("reproductive data=right ovary destroyed ;"),
    #         [Ovary(state="destroyed", side="right", start=18, end=39)],
    #     )
    #
    # def test_ovary_state_17(self):
    #     self.assertEqual(
    #         parse("reproductive data=large ovaries ;"),
    #         [Ovary(state="large", start=18, end=31)],
    #     )
    #
    # def test_ovary_state_18(self):
    #     self.assertEqual(
    #         parse("ovaries somewhat enlarged"),
    #         [Ovary(state="somewhat enlarged", start=0, end=25)],
    #     )
    #
    # def test_ovary_state_19(self):
    #     self.assertEqual(
    #         parse("ovaries imm."), [Ovary(state="imm", start=0, end=11)]
    #     )
    #
    # def test_ovary_state_20(self):
    #     self.assertEqual(
    #         parse("ovaries: both w/sev c. alb;"),
    #         [Ovary(state="sev c. alb", side="both", start=0, end=26)],
    #     )
    #
    # def test_ovary_state_21(self):
    #     self.assertEqual(
    #         parse("corpus luteum visible in both ovaries"),
    #         [Ovary(state="corpus luteum visible", side="both", start=0, end=37)],
    #     )
    #
    # def test_ovary_state_22(self):
    #     self.assertEqual(
    #         parse("reproductive data=only 1 fully developed ovary ;"),
    #         [Ovary(state="fully developed", start=25, end=46)],
    #     )
    #
    # def test_ovary_state_23(self):
    #     self.assertEqual(
    #         parse("ovaries shrunken"),
    #         [Ovary(state="shrunken", start=0, end=16)],
    #     )
    #
    # def test_ovary_state_24(self):
    #     self.assertEqual(
    #         parse("inactive ovary"),
    #         [Ovary(state="inactive", start=0, end=14)],
    #     )
    #
    # def test_ovary_state_25(self):
    #     self.assertEqual(
    #         parse("no embryos, nips small, ovary < 1 x 1 mm"), []
    #     )
    #
    # def test_ovary_state_26(self):
    #     self.assertEqual(
    #         parse("Cyst on ovary"),
    #         [Ovary(state="cyst on", start=0, end=13)],
    #     )
    #
    # def test_ovary_state_27(self):
    #     self.assertEqual(
    #         parse("; 4 bodies in L ovary;"),
    #         [Ovary(state="4 bodies in", side="l", start=2, end=21)],
    #     )
    #
    # def test_ovary_state_28(self):
    #     self.assertEqual(
    #         parse("Mod. fat, ovaries black"),
    #         [Ovary(state="black", start=10, end=23)],
    #     )
    #
    # def test_ovary_state_29(self):
    #     self.assertEqual(
    #         parse("ovary not seen"),
    #         [Ovary(state="not seen", start=0, end=14)],
    #     )
    #
    # def test_ovary_state_30(self):
    #     self.assertEqual(
    #         parse("ovaries pink, fat"),
    #         [Ovary(state="pink", start=0, end=12)],
    #     )
    #
    # def test_ovary_state_31(self):
    #     self.assertEqual(
    #         parse("Left side of ovaries large and cancerous"),
    #         [Ovary(state="large and cancerous", start=13, end=40)],
    #     )
    #
    # def test_ovary_state_32(self):
    #     self.assertEqual(
    #         parse("ovaries well developed, but not pregnant apparently;"),
    #         [Ovary(state="well developed", start=0, end=22)],
    #     )
    #
    # def test_ovary_state_33(self):
    #     self.assertEqual(
    #         parse(
    #             "ovaries pink and smooth, fat around base of " "tail and oviduct"
    #         ),
    #         [Ovary(state="pink and smooth", start=0, end=23)],
    #     )
    #
    # def test_ovary_state_34(self):
    #     self.assertEqual(
    #         parse("Yng. 7 blastocysts and 2 ovaries preserved (where?)"),
    #         [],
    #     )
    #
    # def test_ovary_state_35(self):
    #     self.assertEqual(
    #         parse(
    #             "reproductive data=imp, pelv fused, nipp tiny, nullip, "
    #             "both ov w/ few sm foll;"
    #         ),
    #         [Ovary(state="few sm foll", side="both", start=54, end=76)],
    #     )
    #
    # def test_ovary_state_36(self):
    #     self.assertEqual(
    #         parse(
    #             "stomach, jaw, claw, ovaries, womb too large to preserve"
    #         ),
    #         [],
    #     )
    #
    # def test_ovary_state_37(self):
    #     self.assertEqual(
    #         parse(
    #             "Rov 3 cl, Lov 4 cl, both ov sm-med foll; no molt no scars;"
    #         ),
    #         [Ovary(state="sm-med foll", side="both", start=20, end=39)],
    #     )
