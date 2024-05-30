import unittest

from ranges.pylib.rules.ovary import Ovary
from tests.setup import parse


class TestOvarySize(unittest.TestCase):
    def test_ovary_size_01(self):
        self.assertEqual(
            parse("ovaries = 8x5 mm"),
            [Ovary(length=8.0, width=5.0, start=0, end=16)],
        )

    def test_ovary_size_02(self):
        self.assertEqual(
            parse("ovary < 1 x 1 mm"),
            [Ovary(length=1.0, width=1.0, start=0, end=16)],
        )

    def test_ovary_size_03(self):
        self.assertEqual(
            parse("[right ovary listed, left ovary: 4 x 2 mm]"),
            [
                Ovary(start=1, end=19, right_side="listed"),
                Ovary(length=4, width=2, start=21, end=41),
            ],
        )

    def test_ovary_size_04(self):
        self.assertEqual(
            parse("Rt Ovary 2.0x3.5mm, Lft Ovary 2.1x4.0mm."),
            [
                Ovary(
                    length=2,
                    width=3.5,
                    start=0,
                    end=18,
                ),
                Ovary(
                    length=2.1,
                    width=4,
                    start=20,
                    end=40,
                ),
            ],
        )

    def test_ovary_size_05(self):
        self.assertEqual(
            parse("ovaries: 20mm X 12mm, 18mm X 9mm."),
            [
                Ovary(
                    length=20,
                    width=12,
                    length2=18,
                    width2=9,
                    start=0,
                    end=33,
                ),
            ],
        )

    def test_ovary_size_06(self):
        self.assertEqual(
            parse("ovaries = 8 mm"),
            [Ovary(length=8, start=0, end=14)],
        )

    def test_ovary_size_07(self):
        self.assertEqual(
            parse('"ovaryLengthInMM":"12", "ovaryWidthInMM":"5",'),
            [
                Ovary(
                    length=12,
                    start=1,
                    end=21,
                ),
                Ovary(
                    width=5,
                    start=25,
                    end=43,
                ),
            ],
        )

    def test_ovary_size_08(self):
        self.assertEqual(
            parse('"ovaryLength":"12", "ovaryWidth":"5",'),
            [
                Ovary(
                    length=12,
                    units_inferred=True,
                    start=1,
                    end=17,
                ),
                Ovary(
                    width=5,
                    units_inferred=True,
                    start=21,
                    end=35,
                ),
            ],
        )

    def test_ovary_size_09(self):
        self.assertEqual(
            parse('"ovaryLength":"12mm", "ovaryWidth":"5 mm",'),
            [
                Ovary(
                    length=12,
                    start=1,
                    end=19,
                ),
                Ovary(
                    width=5,
                    start=23,
                    end=40,
                ),
            ],
        )

    def test_ovary_size_10(self):
        self.assertEqual(
            parse("reproductive data=ovary 2 x 1 1/4 mm"),
            [Ovary(length=2, width=1.25, start=18, end=36)],
        )
