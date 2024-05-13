import unittest

# from ranges.pylib.rules.gonad import Gonad
# from tests.setup import parse


class TestGonadSize(unittest.TestCase):
    pass
    # def test_ovary_size_01(self):
    #     self.assertEqual(
    #         parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
    #         [
    #             Ovary(
    #                 length=3,
    #                 units_inferred=True,
    #                 start=1,
    #                 end=21,
    #             ),
    #             Ovary(
    #                 length=2,
    #                 units_inferred=True,
    #                 start=25,
    #                 end=45,
    #             ),
    #         ],
    #     )

    # def test_ovary_size_02(self):
    #     self.assertEqual(
    #         parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
    #         [
    #             Ovary(
    #                 value=12,
    #                 ambiguous_key=True,
    #                 start=1,
    #                 end=21,
    #             ),
    #             Ovary(
    #                 value=5,
    #                 ambiguous_key=True,
    #                 start=25,
    #                 end=43,
    #             ),
    #         ],
    #     )

    # def test_parse_11(self):
    #     self.assertEqual(
    #         parse("tag# 1089; bag# 156; no gonads"),
    #         [Testicle(description="no gonads", ambiguous_key=True, start=21, end=30)],
    #     )

    # def test_parse_13(self):
    #     self.assertEqual(
    #         parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
    #         [
    #             Testicle(
    #                 length=3,
    #                 units_inferred=True,
    #                 start=1,
    #                 end=21,
    #             ),
    #             Testicle(
    #                 length=2,
    #                 units_inferred=True,
    #                 start=25,
    #                 end=45,
    #             ),
    #         ],
    #     )
    #
    # def test_parse_14(self):
    #     self.assertEqual(
    #         parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
    #         [
    #             Testicle(
    #                 length=12,
    #                 ambiguous_key=True,
    #                 dimension="length",
    #                 start=1,
    #                 end=21,
    #             ),
    #             Testicle(
    #                 length=5,
    #                 units="MM",
    #
    #                 ambiguous_key=True,
    #                 dimension="width",
    #                 start=25,
    #                 end=43,
    #             ),
    #         ],
    #     )
    #
    # def test_parse_15(self):
    #     self.assertEqual(
    #         parse(
    #             "left gonad width=9.1 mm; right gonad width=9.2 mm; "
    #             "right gonad length=16.1 mm; left gonad length=16.2 mm"
    #         ),
    #         [
    #             Testicle(
    #                 length=9.1,
    #
    #
    #                 ambiguous_key=True,
    #                 side="left",
    #                 dimension="width",
    #                 start=0,
    #                 end=23,
    #             ),
    #             Testicle(
    #                 length=9.2,
    #
    #
    #                 ambiguous_key=True,
    #                 side="right",
    #                 dimension="width",
    #                 start=25,
    #                 end=49,
    #             ),
    #             Testicle(
    #                 length=16.1,
    #
    #
    #                 ambiguous_key=True,
    #                 side="right",
    #                 dimension="length",
    #                 start=51,
    #                 end=77,
    #             ),
    #             Testicle(
    #                 length=16.2,
    #
    #
    #                 ambiguous_key=True,
    #                 side="left",
    #                 dimension="length",
    #                 start=79,
    #                 end=104,
    #             ),
    #         ],
    #     )
    #
    # def test_parse_16(self):
    #     self.assertEqual(
    #         parse('"gonadLengthInMM":"9mm w.o./epid", '),
    #         [
    #             Testicle(
    #                 length=9,
    #                 units=["MM", "mm"],
    #
    #                 ambiguous_key=True,
    #                 dimension="length",
    #                 start=1,
    #                 end=22,
    #             )
    #         ],
    #     )

    # def test_parse_35(self):
    #     self.assertEqual(
    #         parse("; reproductive data=(R) 20x10mm L 6x4 mm ;"),
    #         [
    #             Testicle(
    #                 length=20,
    #                 width=10,
    #                 start=2,
    #                 end=40,
    #             ),
    #             Testicle(
    #                 length=6,
    #                 width=4,
    #                 start=2,
    #                 end=40,
    #             ),
    #         ],
    #     )
    #
    # def test_parse_36(self):
    #     self.assertEqual(
    #         parse("; reproductive data=R 20x10mm ;"),
    #         [
    #             Testicle(
    #                 length=20,
    #                 width=10,
    #                 start=2,
    #                 end=29,
    #             )
    #         ],
    #     )
