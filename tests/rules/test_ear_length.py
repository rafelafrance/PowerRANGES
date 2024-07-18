import unittest

from ranges.pylib.rules.ear_length import EarLength
from tests.setup import parse


class TestEarLength(unittest.TestCase):
    def test_total_length_01(self):
        self.assertEqual(
            parse('{"earLengthInMM":"9" };'),
            [EarLength(length=9, start=2, end=19)],
        )

    def test_ear_length_02(self):
        """It parses an ear length given as a fraction."""
        self.assertEqual(
            parse('ear 9/16"'),
            [
                EarLength(
                    length=14.29,
                    start=0,
                    end=9,
                )
            ],
        )

    def test_ear_length_03(self):
        """It handles a really short ear key."""
        self.assertEqual(
            parse('E 1",'),
            [
                EarLength(
                    length=25.4,
                    ambiguous=True,
                    start=0,
                    end=4,
                )
            ],
        )

    def test_ear_length_04(self):
        """It skips an ear tag."""
        self.assertEqual(parse("ear tag 570"), [])

    def test_ear_length_05(self):
        """It skips a name."""
        self.assertEqual(parse("verbatim collector=E. E. Makela 2432 "), [])

    def test_ear_length_06(self):
        """It gets a measured from notch notation."""
        self.assertEqual(
            parse("ear from notch=17 mm;"),
            [
                EarLength(
                    length=17,
                    measured_from="notch",
                    start=0,
                    end=20,
                )
            ],
        )

    def test_ear_length_07(self):
        """It gets a measured from crown notation."""
        self.assertEqual(
            parse("earfromcrown=17mm;"),
            [
                EarLength(
                    length=17,
                    measured_from="crown",
                    start=0,
                    end=17,
                )
            ],
        )

    def test_ear_length_08(self):
        """It does not parse_fields this."""
        self.assertEqual(parse("Hawaiian chain. Magnemite 610-E 7050."), [])

    def test_ear_length_09(self):
        """It does not pick up a name."""
        self.assertEqual(parse("Gray, J. E. (1866)."), [])

    def test_ear_length_10(self):
        """It gets an abbreviation."""
        self.assertEqual(
            parse(";E=6;"),
            [EarLength(length=6, start=1, end=4, ambiguous=True, units_inferred=True)],
        )
