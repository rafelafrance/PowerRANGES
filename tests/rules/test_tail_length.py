import unittest

from ranges.pylib.rules.tail_length import TailLength
from tests.setup import parse


class TestTailLength(unittest.TestCase):
    def test_tail_length_01(self):
        """It parses a tail length with a label with keys."""
        self.assertEqual(
            parse("tailLengthInmm: 102"),
            [TailLength(length=102, start=0, end=19)],
        )

    def test_tail_length_02(self):
        """It parses a tail length."""
        self.assertEqual(
            parse("tail length=95 mm;"),
            [TailLength(length=95, start=0, end=17)],
        )

    def test_tail_length_03(self):
        """It does not parse_fields an elevation."""
        self.assertEqual(parse("ELEV G.T. 3900 FT"), [])
