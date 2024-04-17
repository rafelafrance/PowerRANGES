# import unittest
#
# from ranges.pylib.rules.mammary import Mammary
# from ranges.pylib.rules.nipple import Nipple
# from tests.setup import parse
#
#
# class TestNippleState(unittest.TestCase):
#     def test_nipple_state_01(self):
#         self.assertEqual(
#             parse("nipples large"),
#             [Nipple(state="enlarged", start=0, end=13)],
#         )
#
#     def test_nipple_state_02(self):
#         self.assertEqual(
#             parse("protuberant nipples"),
#             [Nipple(state="enlarged", start=0, end=19)],
#         )
#
#     def test_nipple_state_03(self):
#         self.assertEqual(
#             parse("NO nipple showing"),
#             [Nipple(state="not enlarged", start=0, end=9)],
#         )
#
#     def test_nipple_state_04(self):
#         self.assertEqual(
#             parse("VERY SMALL FALSE NIPPLES"),
#             [
#                 Nipple(
#                     state="not enlarged",
#                     start=5,
#                     end=24,
#                 )
#             ],
#         )
#
#     def test_nipple_state_06(self):
#         self.assertEqual(
#             parse("Nipples slightly enlarged."),
#             [
#                 Nipple(
#                     state="enlarged",
#                     start=0,
#                     end=25,
#                 )
#             ],
#         )
#
#     def test_nipple_state_07(self):
#         self.assertEqual(
#             parse("Nipples pigmented."),
#             [Nipple(state="nipples pigmented", start=0, end=17)],
#         )
#
#     def test_nipple_state_08(self):
#         self.assertEqual(
#             parse("no scars or emb., nip. sm., low fat"),
#             [Nipple(state="nip. sm", start=18, end=25)],
#         )
#
#     def test_nipple_state_09(self):
#         self.assertEqual(
#             parse("; teats visible,"),
#             [Nipple(state="teats visible", start=2, end=15)],
#         )
#
#     def test_nipple_state_10(self):
#         self.assertEqual(
#             parse("10 post-lactating teats"),
#             [Nipple(state="post-lactating teats", start=3, end=23)],
#         )
#
#     def test_nipple_state_11(self):
#         self.assertEqual(
#             parse(", LG UTERUS & TEATS,"),
#             [Nipple(state="lg uterus & teats", start=2, end=19)],
#         )
#
#     def test_nipple_state_12(self):
#         self.assertEqual(
#             parse("4 teats post lac."),
#             [Nipple(state="teats post lac", start=2, end=16)],
#         )
#
#     def test_nipple_state_13(self):
#         self.assertEqual(
#             parse("lactating, mammary glands much swollen"),
#             [
#                 Nipple(
#                     state="mammary glands much swollen",
#                     start=11,
#                     end=38,
#                 )
#             ],
#         )
#
#     def test_nipple_state_14(self):
#         self.assertEqual(
#             parse("; mammary tissue present;"),
#             [
#                 Nipple(
#                     state="mammary tissue present",
#                     start=2,
#                     end=24,
#                 )
#             ],
#         )
#
#     def test_nipple_state_15(self):
#         self.assertEqual(
#             parse("VO, NE, mamm. lg."),
#             [Nipple(state="mamm. lg", start=8, end=16)],
#         )
#
#     def test_nipple_state_16(self):
#         self.assertEqual(
#             parse("mammary glands active"),
#             [Nipple(state="mammary glands active", start=0, end=21)],
#         )
#
#     def test_nipple_state_17(self):
#         self.assertEqual(
#             parse("vagina opened, well developed mammary tissue"),
#             [
#                 Nipple(
#                     state="well developed mammary tissue",
#                     start=15,
#                     end=44,
#                 )
#             ],
#         )
#
#     def test_nipple_state_18(self):
#         self.assertEqual(
#             parse("mammae conspicuous; lactating;"),
#             [Nipple(state="mammae conspicuous", start=0, end=18)],
#         )
#
#     def test_nipple_state_19(self):
#         self.assertEqual(
#             parse("; MAMMARY TISSSUE ABSENT;"),
#             [
#                 Nipple(
#                     state="mammary tisssue absent",
#                     start=2,
#                     end=24,
#                 )
#             ],
#         )
#
#     def test_nipple_state_20(self):
#         self.assertEqual(
#             parse("; reproductive data=no nipples showing, uterus found;"),
#             [Nipple(state="no nipples showing", start=20, end=38)],
#         )
#
#     def test_nipple_state_21(self):
#         self.assertEqual(
#             parse("nipples small, moderate fat"),
#             [Nipple(state="nipples small", start=0, end=13)],
#         )
#
#     def test_nipple_state_22(self):
#         self.assertEqual(
#             parse("uterus enlarged, large nipples"),
#             [Nipple(state="large nipples", start=17, end=30)],
#         )
#
#     def test_nipple_state_23(self):
#         self.assertEqual(
#             parse("nipples medium"),
#             [Nipple(state="nipples medium", start=0, end=14)],
#         )
#
#     def test_nipple_state_24(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data=No placental scars or embryos.  "
#                 "3 nipples prominen"
#             ),
#             [Nipple(state="nipples prominen", start=52, end=68)],
#         )
#
#     def test_nipple_state_25(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev: none, no plsc,"),
#             [Nipple(state="nipple dev: none", start=18, end=34)],
#         )
#
#     def test_nipple_state_26(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev, 3R+0L=3 plsc ;"),
#             [Nipple(state="nipple dev", start=18, end=28)],
#         )
#
#     def test_nipple_state_27(self):
#         self.assertEqual(
#             parse(", pelvis slgt sep, nipp med+, no scars,"),
#             [Nipple(state="nipp med+", start=19, end=28)],
#         )
#
#     def test_nipple_state_28(self):
#         self.assertEqual(
#             parse("sep, nipp med, sm reddsih scar"),
#             [Nipple(state="nipp med", start=5, end=13)],
#         )
#
#     def test_nipple_state_29(self):
#         self.assertEqual(
#             parse("reproductive data=Ad. mammery glands developed "
#             "but no nipples"),
#             [
#                 Nipple(
#                     state="mammery glands developed",
#                     start=22,
#                     end=46,
#                 )
#             ],
#         )
#
#     def test_nipple_state_30(self):
#         self.assertEqual(
#             parse("reproductive data=vulva open; no nipples apparent ;"),
#             [],
#         )
#
#     def test_nipple_state_31(self):
#         self.assertEqual(
#             parse("reproductive data=nipples bare ;"),
#             [Nipple(state="nipples bare", start=18, end=30)],
#         )
#
#     def test_nipple_state_32(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev:large, 1R+2L=3embryo,"),
#             [Nipple(state="nipple dev:large", start=18, end=34)],
#         )
#
#     def test_nipple_state_33(self):
#         self.assertEqual(
#             parse("reproductive data=nipples very bare ;"),
#             [Nipple(state="nipples very bare", start=18, end=35)],
#         )
#
#     def test_nipple_state_34(self):
#         self.assertEqual(
#             parse("reproductive data=2R+4L=6plsc developed mamm tissue;"),
#             [
#                 Nipple(
#                     state="developed mamm tissue",
#                     start=30,
#                     end=51,
#                 )
#             ],
#         )
#
#     def test_nipple_state_35(self):
#         self.assertEqual(
#             parse("reproductive data=Lactating; clear & enlarged teats ;"),
#             [Nipple(state="enlarged teats", start=37, end=51)],
#         )
#
#     def test_nipple_state_36(self):
#         self.assertEqual(
#             parse("reproductive data=enlargedNipples ;"),
#             [Nipple(state="enlargednipples", start=18, end=33)],
#         )
