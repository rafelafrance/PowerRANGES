import unittest

from ranges.pylib.rules.tail_length import TailLength
from tests.setup import parse


class TestTailLength(unittest.TestCase):
    def test_tail_length_01(self):
        """It parses a tail length with a label with keys."""
        self.assertEqual(
            parse("tailLengthInmm: 102"),
            [TailLength(trait="tail_length", length=102, start=0, end=19)],
        )

    def test_tail_length_02(self):
        """It parses a tail length."""
        self.assertEqual(
            parse("tail length=95 mm;"),
            [TailLength(trait="tail_length", length=95, start=0, end=17)],
        )

    def test_tail_length_03(self):
        """It does not pick up a testes notation."""
        self.assertEqual(parse("reproductive data=testes abdominal; T = 3 x 1.8 ;"), [])

    def test_tail_length_04(self):
        """It does not parse an elevation."""
        self.assertEqual(parse("ELEV G.T. 3900 FT"), [])
