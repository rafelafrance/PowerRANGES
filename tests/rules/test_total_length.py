import unittest

from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.total_length import TotalLength
from tests.setup import parse


class TestTotalLength(unittest.TestCase):
    def test_total_length_01(self):
        self.assertEqual(
            parse('{"totalLengthInMM":"123" };'),
            [TotalLength(trait="total_length", length=123, start=2, end=23)],
        )

    def test_total_length_02(self):
        """It handles a total length without units."""
        self.assertEqual(
            parse("measurements: ToL=230;"),
            [
                TotalLength(
                    trait="total_length",
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
                TotalLength(trait="total_length", length=231, start=0, end=19),
            ],
        )

    def test_total_length_04(self):
        """It parses a snout-vent length."""
        self.assertEqual(
            parse("snout-vent length=54 mm;"),
            [
                TotalLength(trait="total_length", length=54, start=0, end=23),
            ],
        )

    def test_total_length_05(self):
        """It parses a compound total length."""
        self.assertEqual(
            parse("t.l.= 2 feet 3.1 - 4.5 inches "),
            [
                TotalLength(
                    trait="total_length",
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
                    trait="total_length",
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
            [TotalLength(trait="total_length", length=609.6, start=0, end=19)],
        )

    def test_total_length_08(self):
        """It handles an ambiguous key."""
        self.assertEqual(
            parse("length=8 mm"),
            [
                TotalLength(
                    trait="total_length",
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
                    trait="body_mass",
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
            [TotalLength(trait="total_length", length=130, start=5, end=13)],
        )

    def test_total_length_11(self):
        """It parses a total length range with a suffix key."""
        self.assertEqual(
            parse("det_comments:31.5-58.3inTL"),
            [
                TotalLength(
                    trait="total_length",
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
            [TotalLength(trait="total_length", length=52, start=0, end=7)],
        )

    def test_total_length_13(self):
        """It handles units between the key and value."""
        self.assertEqual(
            parse("TL (mm) 44, xx"),
            [
                TotalLength(trait="total_length", length=44, start=0, end=10),
            ],
        )

    def test_total_length_14(self):
        """It handles an ambiguous range without units."""
        self.assertEqual(
            parse('{"length":"20-29" }'),
            [
                TotalLength(
                    trait="total_length",
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
            [TotalLength(trait="total_length", length=[12, 34], start=0, end=18)],
        )

    # def test_total_length_081(self):
    #     self.assertEqual(
    #         parse("LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=9.52,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_082(self):
    #     self.assertEqual(
    #         parse("LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=9.52,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=15,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_086(self):
    #     self.assertEqual(
    #         parse("measurement on tag for T. L. (141 mm) cannot be correct"),
    #         [TotalLength(trait="total_length", length=141, start=23, end=36)],
    #     )
    #
    # def test_total_length_087(self):
    #     self.assertEqual(
    #         parse("L: 275. T: 65.; "),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=275,
    #                 units_inferred=True,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=6,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_094(self):
    #     self.assertEqual(
    #         parse("t.l.= 2 feet, 4.5 inches "),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=723.9,
    #                 start=0,
    #                 end=24,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_095(self):
    #     target = (
    #         "The length reported (2560 cm = 85 feet) is a bit "
    #         "large for B. physalus and is more in keeping with B. "
    #         "musculus. Redman, N. (2014). Whales' Bones of France, "
    #         "Southern Europe, Middle East and North Africa. "
    #         "Teddington, England, Redman Publishing. "
    #         "p. 24-25, 41-42"
    #     )
    #     self.assertEqual(parse(target), [])

    # def test_total_length_108(self):
    #     self.assertEqual(
    #         parse(
    #             """Body and tail: 109 mm"""
    #         ),
    #         [TotalLength(trait="total_length", length=109, start=0, end=34)],
    #     )
