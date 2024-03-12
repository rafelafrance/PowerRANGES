import unittest

from ranges.pylib.rules.forearm_length import ForearmLength
from tests.setup import parse


class TestForearmLength(unittest.TestCase):
    def test_forearm_length_01(self):
        """It parses a forearm notation."""
        self.assertEqual(
            parse("Forearm 33 mm;"),
            [ForearmLength(trait="forearm_length", length=33, start=0, end=13)],
        )

    def test_forearm_length_02(self):
        """It handles missing units."""
        self.assertEqual(
            parse("For.A. 33;"),
            [
                ForearmLength(
                    trait="forearm_length",
                    length=33,
                    units_inferred=True,
                    start=0,
                    end=9,
                )
            ],
        )

    def test_forearm_length_03(self):
        """It parses a key with units."""
        self.assertEqual(
            parse("forearmleninmm 90"),
            [ForearmLength(trait="forearm_length", length=90, start=0, end=17)],
        )

    def test_forearm_length_04(self):
        """It handles a suffix key."""
        self.assertEqual(
            parse('{"measurements":"44.0 (FA)" }'),
            [
                ForearmLength(
                    trait="forearm_length",
                    length=44,
                    units_inferred=True,
                    start=17,
                    end=26,
                )
            ],
        )
