# import unittest
#
# from ranges.pylib.rules.nipple_state import NippleState
# from tests.setup import parse
#
#
# class TestNippleState(unittest.TestCase):
#     def test_nipple_state_01(self):
#         self.assertEqual(
#             parse("vagina closed, nipples large"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipples large", start=15, end=28
#                 )
#             ],
#         )
#
#     def test_nipple_state_02(self):
#         self.assertEqual(
#             parse("pregnant; 5 emb; protuberant nipples"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="protuberant nipples",
#                     start=17, end=36
#                 )
#             ],
#         )
#
#     def test_nipple_state_03(self):
#         self.assertEqual(
#             parse("NO nipple showing"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="no nipple showing", start=0, end=17
#                 )
#             ],
#         )
#
#     def test_nipple_state_04(self):
#         self.assertEqual(
#             parse("no emb; VERY SMALL FALSE NIPPLES"),
#             [
#                 NippleState(
#                     trait="nipple_state",
#                     state="very small false nipples",
#                     start=8,
#                     end=32,
#                 )
#             ],
#         )
#
#     def test_nipple_state_05(self):
#         self.assertEqual(
#             parse("; NIPPLES INDICATE PREVIOUS LACTATION"),
#             [
#                 NippleState(
#                     trait="nipple_state",
#                     state="nipples indicate previous lactation",
#                     start=2,
#                     end=37,
#                 )
#             ],
#         )
#
#     def test_nipple_state_06(self):
#         self.assertEqual(
#             parse("Nipples slightly enlarged."),
#             [
#                 NippleState(
#                     trait="nipple_state",
#                     state="nipples slightly enlarged",
#                     start=0,
#                     end=25,
#                 )
#             ],
#         )
#
#     def test_nipple_state_07(self):
#         self.assertEqual(
#             parse("Nipples pigmented."),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipples pigmented", start=0, end=17
#                 )
#             ],
#         )
#
#     def test_nipple_state_08(self):
#         self.assertEqual(
#             parse("no scars or emb., nip. sm., low fat"),
#             [NippleState(trait="nipple_state", state="nip. sm", start=18, end=25)],
#         )
#
#     def test_nipple_state_09(self):
#         self.assertEqual(
#             parse("; teats visible,"),
#             [NippleState(trait="nipple_state", state="teats visible",
#             start=2, end=15)],
#         )
#
#     def test_nipple_state_10(self):
#         self.assertEqual(
#             parse("10 post-lactating teats"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="post-lactating teats",
#                     start=3, end=23
#                 )
#             ],
#         )
#
#     def test_nipple_state_11(self):
#         self.assertEqual(
#             parse(", LG UTERUS & TEATS,"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="lg uterus & teats", start=2, end=19
#                 )
#             ],
#         )
#
#     def test_nipple_state_12(self):
#         self.assertEqual(
#             parse("4 teats post lac."),
#             [
#                 NippleState(
#                     trait="nipple_state", state="teats post lac", start=2, end=16
#                 )
#             ],
#         )
#
#     def test_nipple_state_13(self):
#         self.assertEqual(
#             parse("lactating, mammary glands much swollen"),
#             [
#                 NippleState(
#                     trait="nipple_state",
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
#                 NippleState(
#                     trait="nipple_state",
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
#             [NippleState(trait="nipple_state", state="mamm. lg", start=8, end=16)],
#         )
#
#     def test_nipple_state_16(self):
#         self.assertEqual(
#             parse("mammary glands active"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="mammary glands active",
#                     start=0, end=21
#                 )
#             ],
#         )
#
#     def test_nipple_state_17(self):
#         self.assertEqual(
#             parse("vagina opened, well developed mammary tissue"),
#             [
#                 NippleState(
#                     trait="nipple_state",
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
#             [
#                 NippleState(
#                     trait="nipple_state", state="mammae conspicuous", start=0, end=18
#                 )
#             ],
#         )
#
#     def test_nipple_state_19(self):
#         self.assertEqual(
#             parse("; MAMMARY TISSSUE ABSENT;"),
#             [
#                 NippleState(
#                     trait="nipple_state",
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
#             [
#                 NippleState(
#                     trait="nipple_state", state="no nipples showing", start=20, end=38
#                 )
#             ],
#         )
#
#     def test_nipple_state_21(self):
#         self.assertEqual(
#             parse("nipples small, moderate fat"),
#             [NippleState(trait="nipple_state", state="nipples small",
#             start=0, end=13)],
#         )
#
#     def test_nipple_state_22(self):
#         self.assertEqual(
#             parse("uterus enlarged, large nipples"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="large nipples", start=17, end=30
#                 )
#             ],
#         )
#
#     def test_nipple_state_23(self):
#         self.assertEqual(
#             parse("nipples medium"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipples medium", start=0, end=14
#                 )
#             ],
#         )
#
#     def test_nipple_state_24(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data=No placental scars or embryos.  "
#                 "3 nipples prominen"
#             ),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipples prominen", start=52, end=68
#                 )
#             ],
#         )
#
#     def test_nipple_state_25(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev: none, no plsc,"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipple dev: none", start=18, end=34
#                 )
#             ],
#         )
#
#     def test_nipple_state_26(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev, 3R+0L=3 plsc ;"),
#             [NippleState(trait="nipple_state", state="nipple dev", start=18, end=28)],
#         )
#
#     def test_nipple_state_27(self):
#         self.assertEqual(
#             parse(", pelvis slgt sep, nipp med+, no scars,"),
#             [NippleState(trait="nipple_state", state="nipp med+", start=19, end=28)],
#         )
#
#     def test_nipple_state_28(self):
#         self.assertEqual(
#             parse("sep, nipp med, sm reddsih scar"),
#             [NippleState(trait="nipple_state", state="nipp med", start=5, end=13)],
#         )
#
#     def test_nipple_state_29(self):
#         self.assertEqual(
#             parse("reproductive data=Ad. mammery glands developed " "but no nipples"),
#             [
#                 NippleState(
#                     trait="nipple_state",
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
#             [NippleState(trait="nipple_state", state="nipples bare",
#             start=18, end=30)],
#         )
#
#     def test_nipple_state_32(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev:large, 1R+2L=3embryo,"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipple dev:large", start=18, end=34
#                 )
#             ],
#         )
#
#     def test_nipple_state_33(self):
#         self.assertEqual(
#             parse("reproductive data=nipples very bare ;"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="nipples very bare", start=18, end=35
#                 )
#             ],
#         )
#
#     def test_nipple_state_34(self):
#         self.assertEqual(
#             parse("reproductive data=2R+4L=6plsc developed mamm tissue;"),
#             [
#                 NippleState(
#                     trait="nipple_state",
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
#             [
#                 NippleState(
#                     trait="nipple_state", state="enlarged teats", start=37, end=51
#                 )
#             ],
#         )
#
#     def test_nipple_state_36(self):
#         self.assertEqual(
#             parse("reproductive data=enlargedNipples ;"),
#             [
#                 NippleState(
#                     trait="nipple_state", state="enlargednipples", start=18, end=33
#                 )
#             ],
#         )
