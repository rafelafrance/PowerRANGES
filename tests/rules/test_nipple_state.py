import unittest

from ranges.pylib.rules.lactation_state import LactationState
from ranges.pylib.rules.mammary import Mammary
from ranges.pylib.rules.nipple import Nipple
from tests.setup import parse


class TestNippleState(unittest.TestCase):
    def test_nipple_state_01(self):
        self.assertEqual(
            parse("nipples large"),
            [Nipple(state="large", start=0, end=13)],
        )

    def test_nipple_state_02(self):
        self.assertEqual(
            parse("protuberant nipples"),
            [Nipple(state="protuberant", start=0, end=19)],
        )

    def test_nipple_state_03(self):
        self.assertEqual(
            parse("NO nipple showing"),
            [Nipple(state="not showing", start=0, end=17)],
        )

    def test_nipple_state_04(self):
        self.assertEqual(
            parse("VERY SMALL FALSE NIPPLES"),
            [
                Nipple(
                    state="small",
                    start=5,
                    end=24,
                )
            ],
        )

    def test_nipple_state_05(self):
        self.assertEqual(
            parse("reproductive data=enlarged Nipples ;"),
            [Nipple(state="enlarged", start=18, end=34)],
        )

    def test_nipple_state_06(self):
        self.assertEqual(
            parse("Nipples slightly enlarged."),
            [
                Nipple(
                    state="enlarged",
                    start=0,
                    end=25,
                )
            ],
        )

    def test_nipple_state_07(self):
        self.assertEqual(
            parse("Nipples pigmented."),
            [Nipple(state="pigmented", start=0, end=17)],
        )

    def test_nipple_state_08(self):
        self.assertEqual(
            parse("nip. sm., low fat"),
            [Nipple(state="small", start=0, end=7)],
        )

    def test_nipple_state_09(self):
        self.assertEqual(
            parse("; teats visible,"),
            [Nipple(state="visible", start=2, end=15)],
        )

    def test_nipple_state_10(self):
        self.assertEqual(
            parse("10 post-lactating teats"),
            [Nipple(state="post-lactating", count=10, start=0, end=23)],
        )

    def test_nipple_state_11(self):
        self.assertEqual(
            parse(", LG UTERUS & TEATS,"),
            [Nipple(state="large", start=2, end=19)],
        )

    def test_nipple_state_12(self):
        self.assertEqual(
            parse("4 teats post lac."),
            [
                Nipple(count=4, start=0, end=7),
                LactationState(state="not lactating", start=8, end=16),
            ],
        )

    def test_nipple_state_13(self):
        self.assertEqual(
            parse("mammary glands much swollen"),
            [
                Mammary(
                    state="swollen",
                    start=0,
                    end=27,
                )
            ],
        )

    def test_nipple_state_14(self):
        self.assertEqual(
            parse("; mammary tissue present;"),
            [
                Mammary(
                    state="present",
                    start=2,
                    end=24,
                )
            ],
        )

    def test_nipple_state_15(self):
        self.assertEqual(
            parse("nipples small, moderate"),
            [Nipple(state="small medium", start=0, end=23)],
        )

    def test_nipple_state_16(self):
        self.assertEqual(
            parse("mammary glands active"),
            [Mammary(state="active", start=0, end=21)],
        )

    def test_nipple_state_17(self):
        self.assertEqual(
            parse("well developed mammary tissue"),
            [
                Mammary(
                    state="developed",
                    start=5,
                    end=29,
                )
            ],
        )

    def test_nipple_state_18(self):
        self.assertEqual(
            parse("mammae conspicuous;"),
            [Mammary(state="visible", start=0, end=18)],
        )

    def test_nipple_state_19(self):
        self.assertEqual(
            parse("; MAMMARY TISSSUE ABSENT;"),
            [
                Mammary(
                    state="absent",
                    start=2,
                    end=24,
                )
            ],
        )

    def test_nipple_state_20(self):
        self.assertEqual(
            parse("; reproductive data=no nipples showing;"),
            [Nipple(state="not showing", start=20, end=38)],
        )
