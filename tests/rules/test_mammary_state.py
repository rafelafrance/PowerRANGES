import unittest

from ranges.rules.mammary import Mammary
from ranges.rules.nipple import Nipple
from tests.setup import parse


class TestNippleState(unittest.TestCase):
    def test_nipple_state_01(self) -> None:
        self.assertEqual(
            parse("nipples large"),
            [Nipple(state="large", start=0, end=13)],
        )

    def test_nipple_state_02(self) -> None:
        self.assertEqual(
            parse("protuberant nipples"),
            [Nipple(state="protuberant", start=0, end=19)],
        )

    def test_nipple_state_03(self) -> None:
        self.assertEqual(
            parse("NO nipple showing"),
            [Nipple(state="not showing", start=0, end=17)],
        )

    def test_nipple_state_04(self) -> None:
        self.assertEqual(
            parse("VERY SMALL FALSE NIPPLES"),
            [Nipple(state="small", start=5, end=24)],
        )

    def test_nipple_state_05(self) -> None:
        self.assertEqual(
            parse("Nipples slightly enlarged."),
            [Nipple(state="enlarged", start=0, end=25)],
        )

    def test_nipple_state_06(self) -> None:
        self.assertEqual(
            parse("Nipples pigmented."), [Nipple(state="pigmented", start=0, end=17)]
        )

    def test_nipple_state_07(self) -> None:
        self.assertEqual(
            parse(", nip. sm., low fat"),
            [Nipple(state="small", start=2, end=9)],
        )

    def test_nipple_state_08(self) -> None:
        self.assertEqual(
            parse("; teats visible,"),
            [Nipple(start=2, end=15, state="visible")],
        )

    def test_nipple_state_09(self) -> None:
        self.assertEqual(
            parse(", LG UTERUS & TEATS,"),
            [Nipple(state="large", start=2, end=19)],
        )

    def test_nipple_state_10(self) -> None:
        self.assertEqual(
            parse("mammary glands much swollen"),
            [Mammary(state="swollen", start=0, end=27)],
        )

    def test_nipple_state_11(self) -> None:
        self.assertEqual(
            parse("NE, mamm. lg."),
            [Mammary(state="large", start=4, end=12)],
        )

    def test_nipple_state_12(self) -> None:
        self.assertEqual(
            parse("mammary glands active"), [Mammary(state="active", start=0, end=21)]
        )

    def test_nipple_state_13(self) -> None:
        self.assertEqual(
            parse("mammae conspicuous;"),
            [Mammary(state="visible", start=0, end=18)],
        )

    def test_nipple_state_14(self) -> None:
        self.assertEqual(
            parse("reproductive data=enlarged Nipples ;"),
            [Nipple(state="enlarged", start=18, end=34)],
        )

    def test_nipple_state_15(self) -> None:
        self.assertEqual(
            parse("; MAMMARY TISSSUE ABSENT;"),
            [Mammary(state="absent", start=2, end=24)],
        )

    def test_nipple_state_16(self) -> None:
        self.assertEqual(
            parse("; reproductive data=no nipples showing, uterus found;"),
            [Nipple(state="not showing", start=20, end=38)],
        )

    def test_nipple_state_17(self) -> None:
        self.assertEqual(
            parse("nipples medium"), [Nipple(state="medium", start=0, end=14)]
        )

    def test_nipple_state_18(self) -> None:
        self.assertEqual(
            parse("3 nipples prominent"),
            [Nipple(state="prominent", count=3, start=0, end=19)],
        )

    def test_nipple_state_19(self) -> None:
        self.assertEqual(
            parse("reproductive data=nipple dev: none"),
            [Nipple(state="not developed", start=18, end=34)],
        )

    def test_nipple_state_20(self) -> None:
        self.assertEqual(
            parse("reproductive data=nipple dev,;"),
            [Nipple(state="developed", start=18, end=28)],
        )

    def test_nipple_state_21(self) -> None:
        self.assertEqual(
            parse(", pelvis slgt sep, nipp med+,"),
            [Nipple(state="medium", start=19, end=27)],
        )

    def test_nipple_state_22(self) -> None:
        self.assertEqual(
            parse("reproductive data=mammery glands developed but no nipples"),
            [
                Mammary(state="developed", start=18, end=42),
                Nipple(state="none", start=47, end=57),
            ],
        )

    def test_nipple_state_23(self) -> None:
        self.assertEqual(
            parse("no nipples apparent ;"),
            [Nipple(state="none", start=0, end=10)],
        )

    def test_nipple_state_24(self) -> None:
        self.assertEqual(
            parse("clear & enlarged teats ;"),
            [Nipple(state="enlarged", start=8, end=22)],
        )
