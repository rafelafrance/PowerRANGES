import unittest

from ranges.pylib.rules.tragus_length import TragusLength
from tests.setup import parse


class TestTragusLength(unittest.TestCase):
    def test_tragus_length_01(self):
        self.assertEqual(
            parse("Tragus 7;"),
            [
                TragusLength(
                    trait="tragus_length", length=7, units_inferred=True, start=0, end=8
                )
            ],
        )

    def test_tragus_length_02(self):
        self.assertEqual(
            parse("tragus-5 "),
            [
                TragusLength(
                    trait="tragus_length", length=5, units_inferred=True, start=0, end=8
                )
            ],
        )

    def test_tragus_length_03(self):
        self.assertEqual(
            parse("; tragus length=9 mm;"),
            [TragusLength(trait="tragus_length", length=9, start=2, end=20)],
        )

    def test_tragus_length_04(self):
        self.assertEqual(
            parse(""" "tragusLengthInMM":"6" }"""),
            [TragusLength(trait="tragus_length", length=6, start=1, end=21)],
        )

    def test_tragus_length_05(self):
        self.assertEqual(
            parse("""TR 7-xx;"""),
            [
                TragusLength(
                    trait="tragus_length",
                    length=7,
                    units_inferred=True,
                    start=0,
                    end=4,
                )
            ],
        )
