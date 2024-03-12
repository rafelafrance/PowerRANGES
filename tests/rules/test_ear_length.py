import unittest

from ranges.pylib.rules.ear_length import EarLength
from tests.setup import parse


class TestEarLength(unittest.TestCase):
    def test_total_length_01(self):
        self.assertEqual(
            parse('{"earLengthInMM":"9" };'),
            [EarLength(trait="ear_length", length=9, start=2, end=19)],
        )

    # def test_ear_length_02(self):
    #     """It parses an ear length given as a fraction."""
    #     self.assertEqual(
    #         parse('ear 9/16"'),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=14.29,
    #                 units_inferred=False,
    #                 start=0,
    #                 end=23,
    #             )
    #         ],
    #     )

    # def test_ear_length_03(self):
    #     self.assertEqual(
    #         parse('L. 9", T. 4", HF. 2", E 1",'),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=25.4,
    #                 units_inferred=False,
    #                 ambiguous=True,
    #                 start=22,
    #                 end=26,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_04(self):
    #     self.assertEqual(
    #        parse('{"measurements":"TotalLength=180 Tail=82 ' 'HindFoot=28 Ear=18" }'),
    #         [
    #             EarLength(
    #              trait="ear_length", length=18, units_inferred=True, start=53, end=59
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_05(self):
    #     self.assertEqual(
    #         parse('{"earLength":"13", "gonadLength":"3"}'),
    #         [
    #             EarLength(
    #                trait="ear_length", length=13, units_inferred=True, start=2, end=16
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_06(self):
    #     self.assertEqual(parse("ear tag 570"), [])
    #
    # def test_ear_length_07(self):
    #   self.assertEqual(parse("verbatim collector=E. E. Makela 2432 ; sex=female"), [])
    #
    # def test_ear_length_08(self):
    #     self.assertEqual(parse("grid 9, station E1."), [])
    #
    # def test_ear_length_09(self):
    #     self.assertEqual(
    #         parse("ear from notch=17 mm;"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=17,
    #                 units_inferred=False,
    #                 measured_from="notch",
    #                 start=0,
    #                 end=20,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_10(self):
    #     self.assertEqual(
    #         parse("earfromcrown=17mm;"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=17,
    #                 units_inferred=False,
    #                 measured_from="crown",
    #                 start=0,
    #                 end=17,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_11(self):
    #     self.assertEqual(
    #         parse('{"measurements":"242-109-37-34=N/D" }'),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=34,
    #                 units_inferred=False,
    #                 start=17,
    #                 end=34,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_12(self):
    #     self.assertEqual(
    #         parse("E/n-21mm"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=21,
    #                 units_inferred=False,
    #                 ambiguous=True,
    #                 measured_from="n",
    #                 start=0,
    #                 end=8,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_13(self):
    #     self.assertEqual(
    #         parse("E/c-21mm"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=21,
    #                 units_inferred=False,
    #                 ambiguous=True,
    #                 measured_from="c",
    #                 start=0,
    #                 end=8,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_14(self):
    #     self.assertEqual(
    #         parse("; ear from notch=.25 in"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=6.35,
    #                 units_inferred=False,
    #                 measured_from="notch",
    #                 start=2,
    #                 end=23,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_15(self):
    #     self.assertEqual(
    #         parse('"relatedresourceid": "99846657-2832-4987-94cd-451b9679725c"'),
    #         [],
    #     )
    #
    # def test_ear_length_16(self):
    #     self.assertEqual(parse('"356142E 4805438N. Very small"'), [])
    #
    # def test_ear_length_17(self):
    #     self.assertEqual(
    #         parse("Hind Foot: 19 EFN: 13 Weight: 16.3"),
    #         [
    #             EarLength(
    #                 trait="ear_length",
    #                 length=13,
    #                 measured_from="n",
    #                 units_inferred=True,
    #                 start=14,
    #                 end=21,
    #             )
    #         ],
    #     )
    #
    # def test_ear_length_22(self):
    #     self.assertEqual(parse("E.T., E3781185 / N3701740, LLTA 89-116, T=10x7"), [])
    #
    # def test_ear_length_23(self):
    #     self.assertEqual(parse("Cert #E0554185; Skull Seal #0406307"), [])
    #
    # def test_ear_length_24(self):
    #     self.assertEqual(parse("T=12x8, E379700/N3740240"), [])
    #
    # def test_ear_length_25(self):
    #     self.assertEqual(parse("Hawaiian chain.  Magnemite 610-E 7050."), [])
    #
    # def test_ear_length_26(self):
    #     self.assertEqual(parse("Gray, J. E. (1866)."), [])
