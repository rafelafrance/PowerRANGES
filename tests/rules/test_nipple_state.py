import unittest

from ranges.rules.lactation_state import LactationState
from ranges.rules.nipple import Nipple
from tests.setup import parse


class TestNippleState(unittest.TestCase):
    def test_nipple_state_01(self) -> None:
        self.assertEqual(
            parse("nipples large"),
            [Nipple(size="large", start=0, end=13)],
        )

    def test_nipple_state_02(self) -> None:
        self.assertEqual(
            parse("protuberant nipples"),
            [Nipple(description="protuberant", start=0, end=19)],
        )

    def test_nipple_state_03(self) -> None:
        self.assertEqual(
            parse("NO nipple showing"),
            [Nipple(description="not showing", start=0, end=17)],
        )

    def test_nipple_state_04(self) -> None:
        self.assertEqual(
            parse("VERY SMALL FALSE NIPPLES"),
            [
                Nipple(
                    size="small",
                    start=5,
                    end=24,
                )
            ],
        )

    def test_nipple_state_05(self) -> None:
        self.assertEqual(
            parse("reproductive data=enlarged Nipples ;"),
            [Nipple(size="enlarged", start=18, end=34)],
        )

    def test_nipple_state_06(self) -> None:
        self.assertEqual(
            parse("Nipples slightly enlarged."),
            [
                Nipple(
                    size="enlarged",
                    start=0,
                    end=25,
                )
            ],
        )

    def test_nipple_state_07(self) -> None:
        self.assertEqual(
            parse("Nipples pigmented."),
            [Nipple(description="pigmented", start=0, end=17)],
        )

    def test_nipple_state_08(self) -> None:
        self.assertEqual(
            parse("nip. sm., low fat"),
            [Nipple(size="small", start=0, end=7)],
        )

    def test_nipple_state_09(self) -> None:
        self.assertEqual(
            parse("; teats visible,"),
            [Nipple(description="visible", start=2, end=15)],
        )

    def test_nipple_state_10(self) -> None:
        self.assertEqual(
            parse("10 post-lactating teats"),
            [Nipple(description="post-lactating", count=10, start=0, end=23)],
        )

    def test_nipple_state_11(self) -> None:
        self.assertEqual(
            parse(", LG UTERUS & TEATS,"),
            [Nipple(size="large", start=2, end=19)],
        )

    def test_nipple_state_12(self) -> None:
        self.assertEqual(
            parse("4 teats post lac."),
            [
                Nipple(count=4, start=0, end=7),
                LactationState(
                    lactation=False, description="post lac", start=8, end=16
                ),
            ],
        )

    def test_nipple_state_13(self) -> None:
        self.assertEqual(
            parse("mammary glands much swollen"),
            [
                Nipple(
                    description="swollen",
                    start=0,
                    end=27,
                )
            ],
        )

    def test_nipple_state_14(self) -> None:
        self.assertEqual(
            parse("; mammary tissue present;"),
            [
                Nipple(
                    description="present",
                    start=2,
                    end=24,
                )
            ],
        )

    def test_nipple_state_15(self) -> None:
        self.assertEqual(
            parse("nipples small, moderate"),
            [Nipple(size="small medium", start=0, end=23)],
        )

    def test_nipple_state_16(self) -> None:
        self.assertEqual(
            parse("mammary glands active"),
            [Nipple(description="active", start=0, end=21)],
        )

    def test_nipple_state_17(self) -> None:
        self.assertEqual(
            parse("well developed mammary tissue"),
            [
                Nipple(
                    description="developed",
                    start=5,
                    end=29,
                )
            ],
        )

    def test_nipple_state_18(self) -> None:
        self.assertEqual(
            parse("mammae conspicuous;"),
            [Nipple(description="visible", start=0, end=18)],
        )

    def test_nipple_state_19(self) -> None:
        self.assertEqual(
            parse("; MAMMARY TISSSUE ABSENT;"),
            [
                Nipple(
                    description="absent",
                    start=2,
                    end=24,
                )
            ],
        )

    def test_nipple_state_20(self) -> None:
        self.assertEqual(
            parse("; reproductive data=no nipples showing;"),
            [Nipple(description="not showing", start=20, end=38)],
        )
