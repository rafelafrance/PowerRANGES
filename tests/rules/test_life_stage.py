import unittest

from ranges.pylib.rules.life_stage import LifeStage
from tests.setup import parse


class TestLifeStage(unittest.TestCase):
    def test_life_stage_01(self):
        self.assertEqual(
            parse("age class=adult/juvenile after"),
            [
                LifeStage(life_stage="adult/juvenile", start=0, end=24),
            ],
        )

    def test_life_stage_02(self):
        self.assertEqual(
            parse("age=u ad."),
            [LifeStage(life_stage="u ad.", start=0, end=9)],
        )

    def test_life_stage_03(self):
        self.assertEqual(
            parse("age class=over-winter ;"),
            [LifeStage(life_stage="over-winter", start=0, end=21)],
        )

    def test_life_stage_04(self):
        self.assertEqual(
            parse("; age=1st year"),
            [LifeStage(life_stage="1st year", start=2, end=14)],
        )

    def test_life_stage_05(self):
        self.assertEqual(
            parse("words after hatching year more words"),
            [
                LifeStage(
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
            [LifeStage(life_stage="5-6 wks", start=0, end=26)],
        )

    def test_life_stage_08(self):
        self.assertEqual(
            parse("mentions juvenile"),
            [LifeStage(life_stage="juvenile", start=9, end=17)],
        )

    def test_life_stage_09(self):
        self.assertEqual(
            parse("mentions juveniles in the field"),
            [LifeStage(life_stage="juvenile", start=9, end=18)],
        )

    def test_life_stage_10(self):
        self.assertEqual(
            parse("one or more adults"),
            [LifeStage(life_stage="adult", start=12, end=18)],
        )

    def test_life_stage_11(self):
        self.assertEqual(
            parse("adults"),
            [LifeStage(life_stage="adult", start=0, end=6)],
        )

    def test_life_stage_12(self):
        self.assertEqual(
            parse("Adulte"),
            [LifeStage(life_stage="adult", start=0, end=6)],
        )

    def test_life_stage_13(self):
        self.assertEqual(
            parse("AGE IMM"),
            [LifeStage(life_stage="immature", start=0, end=7)],
        )

    def test_life_stage_14(self):
        self.assertEqual(
            parse("subadult"),
            [LifeStage(life_stage="subadult", start=0, end=8)],
        )

    def test_life_stage_15(self):
        self.assertEqual(parse("subadultery"), [])

    def test_life_stage_16(self):
        self.assertEqual(
            parse("in which larvae are found"),
            [LifeStage(life_stage="larval", start=9, end=15)],
        )

    def test_life_stage_17(self):
        self.assertEqual(
            parse("one tadpole"),
            [LifeStage(life_stage="tadpole", start=4, end=11)],
        )

    def test_life_stage_18(self):
        """Life stage removed."""
        self.assertEqual(parse("some embryos"), [])

    def test_life_stage_19(self):
        self.assertEqual(
            parse("young adult"),
            [LifeStage(life_stage="young adult", start=0, end=11)],
        )

    def test_life_stage_20(self):
        self.assertEqual(
            parse("adult young"),
            [LifeStage(life_stage="young adult", start=0, end=11)],
        )

    def test_life_stage_21(self):
        self.assertEqual(
            parse("sub-adult"),
            [LifeStage(life_stage="subadult", start=0, end=9)],
        )

    def test_life_stage_22(self):
        self.assertEqual(
            parse("adult(s) and juvenile(s)"),
            [
                LifeStage(life_stage="adult", start=0, end=5),
                LifeStage(life_stage="juvenile", start=13, end=21),
            ],
        )

    def test_life_stage_23(self):
        self.assertEqual(
            parse("young-of-the-year"),
            [LifeStage(life_stage="young of the year", start=0, end=17)],
        )

    def test_life_stage_24(self):
        self.assertEqual(
            parse("YOLK SAC"),
            [LifeStage(life_stage="yolk sac", start=0, end=8)],
        )

    def test_life_stage_25(self):
        self.assertEqual(parse("Specimen Age Estimate - minimum date: 15030"), [])

    def test_life_stage_26(self):
        """It handles 'seconds' as a time unit and an ordinal."""
        self.assertEqual(
            parse("; age=second year"),
            [LifeStage(life_stage="second year", start=2, end=17)],
        )

    def test_life_stage_27(self):
        """It handles regular ordinal terms."""
        self.assertEqual(
            parse("; age=third year"),
            [LifeStage(life_stage="third year", start=2, end=16)],
        )

    def test_life_stage_28(self):
        """It handles an ordinal alone."""
        self.assertEqual(
            parse("Note in catalog: and a second skull"),
            [],
        )

    def test_life_stage_29(self):
        self.assertEqual(
            parse("; 2nd Asiatnc Eped./"),
            [],
        )

    def test_life_stage_30(self):
        self.assertEqual(
            parse("age class=young of year;"),
            [LifeStage(life_stage="young of the year", start=0, end=23)],
        )
