import unittest

from ranges.pylib.rules.nipple import Nipple
from tests.setup import parse


class TestNippleEnlarged(unittest.TestCase):
    def test_nipple_enlarged_01(self):
        self.assertEqual(
            parse("nipples large"),
            [Nipple(trait="nipple", state="enlarged", start=0, end=13)],
        )

    def test_nipple_enlarged_02(self):
        self.assertEqual(
            parse("protuberant nipples"),
            [Nipple(trait="nipple", state="enlarged", start=0, end=19)],
        )

    def test_nipple_enlarged_03(self):
        self.assertEqual(
            parse("NO nipple showing"),
            [Nipple(trait="nipple", state="not enlarged", start=0, end=9)],
        )

    def test_nipple_enlarged_04(self):
        self.assertEqual(
            parse("VERY SMALL FALSE NIPPLES"),
            [Nipple(trait="nipple", state="not enlarged", start=5, end=24)],
        )

    def test_nipple_enlarged_05(self):
        self.assertEqual(
            parse("Nipples slightly enlarged."),
            [Nipple(trait="nipple", state="enlarged", start=0, end=25)],
        )

    def test_nipple_enlarged_06(self):
        self.assertEqual(parse("Nipples pigmented."), [])

    def test_nipple_enlarged_07(self):
        self.assertEqual(
            parse(", nip. sm., low fat"),
            [Nipple(trait="nipple", state="not enlarged", start=2, end=9)],
        )

    def test_nipple_enlarged_08(self):
        self.assertEqual(
            parse("; teats visible,"),
            [Nipple(trait="nipple", start=2, end=15, state="enlarged")],
        )

    def test_nipple_enlarged_09(self):
        self.assertEqual(
            parse(", LG UTERUS & TEATS,"),
            [Nipple(trait="nipple", state="enlarged", start=2, end=19)],
        )

    def test_nipple_enlarged_11(self):
        self.assertEqual(parse("mammary glands much swollen"), [])

    def test_nipple_enlarged_12(self):
        self.assertEqual(
            parse("VO, NE, mamm. lg."),
            [Nipple(trait="nipple", state="enlarged", start=8, end=16)],
        )

    def test_nipple_enlarged_13(self):
        self.assertEqual(parse("mammary glands active"), [])

    def test_nipple_enlarged_14(self):
        self.assertEqual(
            parse("mammae conspicuous;"),
            [Nipple(trait="nipple", state="enlarged", start=0, end=18)],
        )

    def test_nipple_enlarged_15(self):
        self.assertEqual(parse("; MAMMARY TISSSUE ABSENT;"), [])

    def test_nipple_enlarged_16(self):
        self.assertEqual(
            parse("; reproductive data=no nipples showing, uterus found;"),
            [Nipple(trait="nipple", state="not enlarged", start=20, end=30)],
        )

    def test_nipple_enlarged_17(self):
        self.assertEqual(parse("nipples medium"), [])

    def test_nipple_enlarged_18(self):
        self.assertEqual(
            parse("3 nipples prominent"),
            [Nipple(trait="nipple", state="enlarged", count=3, start=0, end=19)],
        )

    def test_nipple_enlarged_19(self):
        self.assertEqual(
            parse("reproductive data=nipple dev: none"),
            [Nipple(trait="nipple", state="not enlarged", start=18, end=34)],
        )

    def test_nipple_enlarged_20(self):
        self.assertEqual(parse("reproductive data=nipple dev,;"), [])

    def test_nipple_enlarged_21(self):
        self.assertEqual(parse(", pelvis slgt sep, nipp med+, no scars,"), [])

    def test_nipple_enlarged_22(self):
        self.assertEqual(
            parse("reproductive data=mammery glands developed " "but no nipples"),
            [Nipple(trait="nipple", state="not enlarged", start=47, end=57)],
        )

    def test_nipple_enlarged_23(self):
        self.assertEqual(
            parse("no nipples apparent ;"),
            [Nipple(trait="nipple", state="not enlarged", start=0, end=10)],
        )

    def test_nipple_enlarged_24(self):
        self.assertEqual(
            parse("clear & enlarged teats ;"),
            [Nipple(trait="nipple", state="enlarged", start=8, end=22)],
        )

    def test_nipple_enlarged_25(self):
        self.assertEqual(
            parse("reproductive data=enlarged Nipples ;"),
            [Nipple(trait="nipple", state="enlarged", start=18, end=34)],
        )
