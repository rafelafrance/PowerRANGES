import unittest

from ranges.rules.mammary import Mammary
from ranges.rules.nipple import Nipple
from tests.setup import parse


class TestNipple(unittest.TestCase):
    def test_nipple_count_01(self) -> None:
        self.assertEqual(
            parse("6 mammae"),
            [Mammary(count=6, start=0, end=8)],
        )

    def test_nipple_count_02(self) -> None:
        self.assertEqual(
            parse("1:2 = 6 mammae"),
            [Mammary(count=6, start=0, end=14)],
        )

    def test_nipple_count_03(self) -> None:
        self.assertEqual(
            parse("6 inguinal mammae visible but small;"),
            [Mammary(state="visible", count=6, start=0, end=25)],
        )

    def test_nipple_count_04(self) -> None:
        self.assertEqual(
            parse("mammae 2+2"),
            [Mammary(count=4, start=0, end=10)],
        )

    def test_nipple_count_05(self) -> None:
        self.assertEqual(
            parse("0 : 2 = 4 mammae"),
            [Mammary(count=4, start=0, end=16)],
        )

    def test_nipple_count_06(self) -> None:
        self.assertEqual(
            parse("mammae: 1 + 2 = 6"),
            [Mammary(count=6, start=0, end=17)],
        )

    def test_nipple_count_07(self) -> None:
        self.assertEqual(
            parse("3 pec, 3 ing mammae"),
            [Mammary(count=6, start=0, end=19)],
        )

    def test_nipple_count_08(self) -> None:
        self.assertEqual(
            parse("(mammae: 1 pr + 2 pr = 6)"),
            [Mammary(count=6, start=1, end=24)],
        )

    def test_nipple_count_09(self) -> None:
        self.assertEqual(
            parse("4 teats exposed, mammary glands developed,"),
            [
                Nipple(count=4, start=0, end=7),
                Mammary(state="developed", start=17, end=41),
            ],
        )

    def test_nipple_count_10(self) -> None:
        self.assertEqual(
            parse("6 conspicuous mammae;"),
            [Mammary(state="visible", count=6, start=0, end=20)],
        )

    def test_nipple_count_11(self) -> None:
        self.assertEqual(parse("a fauna of about 800 mammal teeth"), [])

    def test_nipple_count_12(self) -> None:
        self.assertEqual(parse("Source: MRS. ID# 42-1111.  Mammary development,"), [])

    def test_nipple_count_13(self) -> None:
        self.assertEqual(parse("TEATS 98% LEAF,2%"), [])

    def test_nipple_count_14(self) -> None:
        self.assertEqual(parse("reproductive data=mammae (4L, 5R)"), [])
