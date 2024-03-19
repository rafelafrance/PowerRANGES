import unittest

from ranges.pylib.rules.tragus_length import TragusLength
from tests.setup import parse


class TestTragusLength(unittest.TestCase):
    def test_tragus_length_01(self):
        """It parses a length without units."""
        self.assertEqual(
            parse("Tragus 7;"),
            [
                TragusLength(
                    trait="tragus_length", length=7, units_inferred=True, start=0, end=8
                )
            ],
        )
