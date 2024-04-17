import unittest

from ranges.pylib.rules.pregnancy_state import PregnancyState
from ranges.pylib.rules.sex import Sex
from tests.setup import parse


class TestPregnancyState(unittest.TestCase):
    def test_pregnancy_state_01(self):
        self.assertEqual(
            parse("pregnant;"),
            [PregnancyState(state="pregnant", start=0, end=8)],
        )

    def test_pregnancy_state_02(self):
        self.assertEqual(
            parse("not pregnant;"),
            [PregnancyState(state="not pregnant", start=0, end=12)],
        )

    def test_pregnancy_state_03(self):
        self.assertEqual(
            parse("non-pregnant"),
            [PregnancyState(state="not pregnant", start=0, end=12)],
        )

    def test_pregnancy_state_04(self):
        self.assertEqual(
            parse("Box ID: UAFWALR34. Recent Pregnancy."),
            [PregnancyState(state="not pregnant", start=19, end=35)],
        )

    def test_pregnancy_state_05(self):
        self.assertEqual(
            parse("probably pregnant"),
            [PregnancyState(state="pregnant", start=9, end=17)],
        )

    def test_pregnancy_state_06(self):
        self.assertEqual(
            parse("Fox was pregnant, but"),
            [PregnancyState(state="not pregnant", start=4, end=16)],
        )

    def test_pregnancy_state_07(self):
        self.assertEqual(
            parse("GMU catalog.  Pregnant?"),
            [PregnancyState(state="pregnant", start=13, end=21)],
        )

    def test_pregnancy_state_08(self):
        self.assertEqual(parse("IMPREGNATED WITH POLYVINYL ACETATE"), [])

    def test_pregnancy_state_09(self):
        self.assertEqual(
            parse("probably early pregnancy"),
            [PregnancyState(state="pregnant", start=15, end=24)],
        )

    def test_pregnancy_state_10(self):
        self.assertEqual(
            parse("No NK# assigned previously, pregnant"),
            [PregnancyState(state="pregnant", start=28, end=36)],
        )

    def test_pregnancy_state_11(self):
        self.assertEqual(
            parse("possible early pregnancy"),
            [PregnancyState(state="pregnant", start=15, end=24)],
        )

    def test_pregnancy_state_12(self):
        self.assertEqual(
            parse(",prob. pregnant,"),
            [PregnancyState(state="pregnant", start=7, end=15)],
        )

    def test_pregnancy_state_13(self):
        self.assertEqual(
            parse("; not visibly pregnant,"),
            [PregnancyState(state="not pregnant", start=2, end=22)],
        )

    def test_pregnancy_state_14(self):
        self.assertEqual(
            parse("No evidence of pregnancy,"),
            [PregnancyState(state="not pregnant", start=0, end=24)],
        )

    def test_pregnancy_state_15(self):
        self.assertEqual(
            parse("males and a pregnant female,"),
            [
                Sex(start=0, end=5, _trait="sex", _text="males", sex="male"),
                PregnancyState(state="pregnant", start=12, end=20),
                Sex(start=21, end=27, _trait="sex", _text="female", sex="female"),
            ],
        )

    def test_pregnancy_state_16(self):
        self.assertEqual(
            parse("pregnancy not evident"),
            [PregnancyState(state="not pregnant", start=0, end=21)],
        )

    def test_pregnancy_state_17(self):
        self.assertEqual(
            parse("*Two pregnancies were visible on uterus."),
            [PregnancyState(state="pregnant", start=5, end=16)],
        )

    def test_pregnancy_state_18(self):
        self.assertEqual(
            parse("number 2859; no pregnancies"),
            [PregnancyState(state="not pregnant", start=13, end=27)],
        )

    def test_pregnancy_state_19(self):
        self.assertEqual(
            parse("reproductive data=Not gravid"),
            [PregnancyState(state="not pregnant", start=18, end=28)],
        )

    def test_pregnancy_state_20(self):
        self.assertEqual(
            parse("reproductive data=At least primiparous"),
            [PregnancyState(state="pregnant", start=27, end=38)],
        )

    def test_pregnancy_state_21(self):
        self.assertEqual(
            parse("post-parous"),
            [PregnancyState(state="not pregnant", start=0, end=11)],
        )

    def test_pregnancy_state_22(self):
        self.assertEqual(
            parse("non parous"),
            [PregnancyState(state="not pregnant", start=0, end=10)],
        )
