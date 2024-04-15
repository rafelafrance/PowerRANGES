import unittest

from ranges.pylib.rules.nipple_count import NippleCount
from tests.setup import parse


class TestNipple(unittest.TestCase):
    def test_nipple_count_01(self):
        self.assertEqual(
            parse("6 mammae"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=8)],
        )

    def test_nipple_count_02(self):
        self.assertEqual(
            parse("1:2 = 6 mammae"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=14)],
        )

    def test_nipple_count_03(self):
        self.assertEqual(
            parse("6 inguinal mammae visible but small;"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=17)],
        )

    def test_nipple_count_04(self):
        self.assertEqual(
            parse("mammae 2+2"),
            [NippleCount(trait="nipple_count", count=4, start=0, end=10)],
        )

    def test_nipple_count_05(self):
        self.assertEqual(
            parse("0 : 2 = 4 mammae"),
            [NippleCount(trait="nipple_count", count=4, start=0, end=16)],
        )

    def test_nipple_count_06(self):
        self.assertEqual(
            parse("mammae: 1 + 2 = 6"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=17)],
        )

    def test_nipple_count_07(self):
        self.assertEqual(
            parse("3 pec, 3 ing mammae"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=19)],
        )

    def test_nipple_count_08(self):
        self.assertEqual(
            parse("(mammae: 1 pr + 2 pr = 6)"),
            [NippleCount(trait="nipple_count", count=6, start=1, end=24)],
        )

    def test_nipple_count_09(self):
        self.assertEqual(
            parse("4 teats exposed, mammary glands developed,"),
            [NippleCount(trait="nipple_count", count=4, start=0, end=7)],
        )

    def test_nipple_count_10(self):
        self.assertEqual(
            parse("6 conspicuous mammae;"),
            [NippleCount(trait="nipple_count", count=6, start=0, end=20)],
        )

    def test_nipple_count_11(self):
        self.assertEqual(parse("a fauna of about 800 mammal teeth"), [])

    def test_nipple_count_12(self):
        self.assertEqual(parse("Source: MRS. ID# 42-1111.  Mammary development,"), [])

    def test_nipple_count_13(self):
        self.assertEqual(parse("TEATS 98% LEAF,2%"), [])

    def test_nipple_count_14(self):
        self.assertEqual(parse("reproductive data=mammae (4L, 5R)"), [])
