import unittest

from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.life_stage import LifeStage
from ranges.pylib.rules.total_length import TotalLength
from tests.setup import parse


class TestTotalLength(unittest.TestCase):
    def test_total_length_01(self):
        self.assertEqual(
            parse('{"totalLengthInMM":"123" };'),
            [TotalLength(length=123, start=2, end=23)],
        )

    def test_total_length_02(self):
        """It handles a total length without units."""
        self.assertEqual(
            parse("measurements: ToL=230;"),
            [
                TotalLength(
                    length=230,
                    units_inferred=True,
                    start=14,
                    end=21,
                ),
            ],
        )

    def test_total_length_03(self):
        """It handles a total length with units."""
        self.assertEqual(
            parse(" total length=231 mm;"),
            [
                TotalLength(length=231, start=0, end=19),
            ],
        )

    def test_total_length_04(self):
        """It parses a snout-vent length."""
        self.assertEqual(
            parse("snout-vent length=54 mm;"),
            [
                TotalLength(length=54, start=0, end=23),
            ],
        )

    def test_total_length_05(self):
        """It parses a compound total length."""
        self.assertEqual(
            parse("t.l.= 2 feet 3.1 - 4.5 inches "),
            [
                TotalLength(
                    length=[688.34, 723.9],
                    start=0,
                    end=29,
                )
            ],
        )

    def test_total_length_06(self):
        """It parses a compound total length without a key."""
        self.assertEqual(
            parse("2 ft. 3.1 - 4.5 in. "),
            [
                TotalLength(
                    length=[688.34, 723.9],
                    ambiguous=True,
                    start=0,
                    end=19,
                )
            ],
        )

    def test_total_length_07(self):
        """It handles different units."""
        self.assertEqual(
            parse("total length= 2 ft."),
            [TotalLength(length=609.6, start=0, end=19)],
        )

    def test_total_length_08(self):
        """It handles an ambiguous key."""
        self.assertEqual(
            parse("length=8 mm"),
            [
                TotalLength(
                    length=8,
                    ambiguous=True,
                    start=0,
                    end=11,
                )
            ],
        )

    def test_total_length_09(self):
        """It handles wrong units."""
        self.assertEqual(
            parse("SVL=0 g"),
            [
                BodyMass(
                    start=3,
                    end=7,
                    mass=0.0,
                    ambiguous=True,
                )
            ],
        )

    def test_total_length_10(self):
        """It handles a suffix key."""
        self.assertEqual(
            parse("Size=13 cm TL"),
            [TotalLength(length=130, start=5, end=13)],
        )

    def test_total_length_11(self):
        """It parses a total length range with a suffix key."""
        self.assertEqual(
            parse("det_comments:31.5-58.3inTL"),
            [
                TotalLength(
                    length=[31.5, 58.3],
                    units_inferred=True,
                    start=13,
                    end=26,
                )
            ],
        )

    def test_total_length_12(self):
        """It handles key, length, and units all in a single word."""
        self.assertEqual(
            parse("SVL52mm"),
            [TotalLength(length=52, start=0, end=7)],
        )

    def test_total_length_13(self):
        """It handles units between the key and value."""
        self.assertEqual(
            parse("TL (mm) 44, xx"),
            [
                TotalLength(length=44, start=0, end=10),
            ],
        )

    def test_total_length_14(self):
        """It handles an ambiguous range without units."""
        self.assertEqual(
            parse('{"length":"20-29" }'),
            [
                TotalLength(
                    length=[20, 29],
                    ambiguous=True,
                    units_inferred=True,
                    start=2,
                    end=16,
                )
            ],
        )

    def test_total_length_15(self):
        """It parses a merged units and key."""
        self.assertEqual(
            parse("Length: 12-34 mmSL"),
            [TotalLength(length=[12, 34], start=0, end=18)],
        )

    def test_total_length_16(self):
        """Parse lengths given in fractional inches."""
        self.assertEqual(
            parse("LENGTH 3/8 IN."),
            [
                TotalLength(
                    length=9.52,
                    ambiguous=True,
                    start=0,
                    end=14,
                )
            ],
        )

    def test_total_length_17(self):
        """Parse a length with fraction and a whole number."""
        self.assertEqual(
            parse("LENGTH 1 1/2 IN."),
            [
                TotalLength(
                    length=38.1,
                    ambiguous=True,
                    start=0,
                    end=16,
                )
            ],
        )

    def test_total_length_18(self):
        """It handles the parentheses enclosing the measurement."""
        self.assertEqual(
            parse("measurement on tag for T. L. (141 mm) cannot be correct"),
            [TotalLength(length=141, start=23, end=37)],
        )

    def test_total_length_19(self):
        """It handles this really short key abbreviation."""
        self.assertEqual(
            parse("L: 275."),
            [
                TotalLength(
                    length=275,
                    units_inferred=True,
                    ambiguous=True,
                    start=0,
                    end=6,
                )
            ],
        )

    def test_total_length_20(self):
        self.assertEqual(
            parse("Body and tail: 1690 mm;"),
            [
                TotalLength(
                    length=1690,
                    start=0,
                    end=22,
                )
            ],
        )

    def test_total_length_21(self):
        """It parses a new 'nose-tail' key."""
        self.assertEqual(
            parse("Other Measurements: nose-tail=60in., girth=39in."),
            [
                TotalLength(
                    length=1524,
                    start=20,
                    end=35,
                )
            ],
        )

    def test_total_length_22(self):
        """It handles a long key."""
        self.maxDiff = None
        self.assertEqual(
            parse("Imm., L. snout to tip of tail 1510,"),
            [
                LifeStage(start=0, end=4, _text="Imm.", life_stage="imm."),
                TotalLength(
                    length=1510,
                    units_inferred=True,
                    start=9,
                    end=34,
                ),
            ],
        )
