import unittest

from ranges.pylib.rules.hind_foot_length import HindFootLength
from tests.setup import parse


class TestHindFootLength(unittest.TestCase):
    def test_hind_foot_length_01(self):
        """It parses a notation with a claw."""
        self.assertEqual(
            parse("hind foot with claw=30 mm;"),
            [
                HindFootLength(
                    length=30,
                    includes="claw",
                    start=0,
                    end=25,
                )
            ],
        )

    def test_hind_foot_length_02(self):
        """It handles missing units."""
        self.assertEqual(
            parse("; HindFoot: 30.0; "),
            [
                HindFootLength(
                    length=30,
                    units_inferred=True,
                    start=2,
                    end=16,
                )
            ],
        )

    def test_hind_foot_length_03(self):
        """It parses a notation with a dash between the key and value."""
        self.maxDiff = None
        self.assertEqual(
            parse("HF-30mm,"),
            [HindFootLength(length=30, start=0, end=7)],
        )

    def test_hind_foot_length_04(self):
        """It parses a key with units."""
        self.assertEqual(
            parse('"footLengthInMillimeters"="31",'),
            [HindFootLength(length=31, start=1, end=29)],
        )

    def test_hind_foot_length_05(self):
        """It parses inch units."""
        self.maxDiff = None
        self.assertEqual(
            parse("; hind foot with claw=2 in;"),
            [
                HindFootLength(
                    length=50.8,
                    includes="claw",
                    start=2,
                    end=26,
                )
            ],
        )
