import unittest

from ranges.pylib.rules.life_stage import LifeStage
from tests.setup import parse


class TestLifeStage(unittest.TestCase):
    def test_life_stage_01(self):
        self.assertEqual(
            parse("age class=adult/juvenile after"),
            [
                LifeStage(
                    trait="life_stage", life_stage="adult/juvenile", start=0, end=24
                ),
            ],
        )

    def test_life_stage_02(self):
        self.assertEqual(
            parse("age=u ad."),
            [LifeStage(trait="life_stage", life_stage="u ad.", start=0, end=9)],
        )

    def test_life_stage_03(self):
        self.assertEqual(
            parse("age class=over-winter ;"),
            [LifeStage(trait="life_stage", life_stage="over-winter", start=0, end=21)],
        )

    def test_life_stage_04(self):
        self.assertEqual(
            parse("; age=1st year more than four words here"),
            [LifeStage(trait="life_stage", life_stage="1st year", start=2, end=14)],
        )

    def test_life_stage_05(self):
        self.assertEqual(
            parse("words after hatching year more words"),
            [
                LifeStage(
                    trait="life_stage",
                    life_stage="after hatching year",
                    start=6,
                    end=25,
                )
            ],
        )

    def test_life_stage_06(self):
        self.assertEqual(parse("age determined by 20-sided die"), [])

    def test_life_stage_07(self):
        self.assertEqual(
            parse("LifeStage Remarks: 5-6 wks;"),
            [LifeStage(trait="life_stage", life_stage="5-6 wks", start=0, end=26)],
        )

    def test_life_stage_08(self):
        self.assertEqual(
            parse("mentions juvenile"),
            [LifeStage(trait="life_stage", life_stage="juvenile", start=9, end=17)],
        )

    def test_life_stage_09(self):
        self.assertEqual(
            parse("mentions juveniles in the field"),
            [LifeStage(trait="life_stage", life_stage="juveniles", start=9, end=18)],
        )

    def test_life_stage_10(self):
        self.assertEqual(
            parse("one or more adults"),
            [LifeStage(trait="life_stage", life_stage="adults", start=12, end=18)],
        )

    def test_life_stage_11(self):
        self.assertEqual(
            parse("adults"),
            [LifeStage(trait="life_stage", life_stage="adults", start=0, end=6)],
        )

    def test_life_stage_12(self):
        self.assertEqual(
            parse("Adulte"),
            [LifeStage(trait="life_stage", life_stage="adulte", start=0, end=6)],
        )

    def test_life_stage_13(self):
        self.assertEqual(
            parse("AGE IMM"),
            [LifeStage(trait="life_stage", life_stage="imm", start=0, end=7)],
        )

    def test_life_stage_14(self):
        self.assertEqual(
            parse("subadult"),
            [LifeStage(trait="life_stage", life_stage="subadult", start=0, end=8)],
        )

    def test_life_stage_15(self):
        self.assertEqual(parse("subadultery"), [])

    def test_life_stage_16(self):
        self.assertEqual(
            parse("in which larvae are found"),
            [LifeStage(trait="life_stage", life_stage="larvae", start=9, end=15)],
        )

    def test_life_stage_17(self):
        self.assertEqual(
            parse("one tadpole"),
            [LifeStage(trait="life_stage", life_stage="tadpole", start=4, end=11)],
        )

    def test_life_stage_18(self):
        """Life stage removed."""
        self.assertEqual(parse("some embryos"), [])

    def test_life_stage_19(self):
        self.assertEqual(
            parse("young adult"),
            [LifeStage(trait="life_stage", life_stage="young adult", start=0, end=11)],
        )

    def test_life_stage_20(self):
        self.assertEqual(
            parse("adult young"),
            [LifeStage(trait="life_stage", life_stage="adult young", start=0, end=11)],
        )

    def test_life_stage_21(self):
        self.assertEqual(
            parse("sub-adult"),
            [LifeStage(trait="life_stage", life_stage="sub-adult", start=0, end=9)],
        )

    def test_life_stage_22(self):
        self.assertEqual(
            parse("adult(s) and juvenile(s)"),
            [
                LifeStage(trait="life_stage", life_stage="adult", start=0, end=5),
                LifeStage(trait="life_stage", life_stage="juvenile", start=13, end=21),
            ],
        )

    def test_life_stage_23(self):
        self.assertEqual(
            parse("young-of-the-year"),
            [
                LifeStage(
                    trait="life_stage", life_stage="young-of-the-year", start=0, end=17
                )
            ],
        )

    def test_life_stage_24(self):
        self.assertEqual(
            parse("YOLK SAC"),
            [LifeStage(trait="life_stage", life_stage="yolk sac", start=0, end=8)],
        )

    def test_life_stage_25(self):
        self.assertEqual(parse("Specimen Age Estimate - minimum date: 15030"), [])

    def test_life_stage_26(self):
        """It handles 'seconds' as a time unit and an ordinal."""
        self.assertEqual(
            parse("; age=second year more than four words here"),
            [LifeStage(trait="life_stage", life_stage="second year", start=2, end=17)],
        )

    def test_life_stage_27(self):
        """It handles regular ordinal terms."""
        self.assertEqual(
            parse("; age=third year more than four words here"),
            [LifeStage(trait="life_stage", life_stage="third year", start=2, end=16)],
        )
