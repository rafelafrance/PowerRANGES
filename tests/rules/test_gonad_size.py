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
