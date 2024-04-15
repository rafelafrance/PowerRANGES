# import unittest
#
# from ranges.pylib.rules.nipple_enlarged import NippleEnlarged
# from tests.setup import parse
#
#
# class TestNippleEnlarged(unittest.TestCase):
#     def test_nipple_enlarged__01(self):
#         self.assertEqual(
#             parse("vagina closed, nipples large"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=15, end=28
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__02(self):
#         self.assertEqual(
#             parse("pregnant; 5 emb; protuberant nipples"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=17, end=36
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__03(self):
#         self.assertEqual(
#             parse("NO nipple showing"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=0, end=9
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__04(self):
#         self.assertEqual(
#             parse("no emb; VERY SMALL FALSE NIPPLES"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=13, end=32
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__05(self):
#         self.assertEqual(parse("; NIPPLES INDICATE PREVIOUS LACTATION"), [])
#
#     def test_nipple_enlarged__06(self):
#         self.assertEqual(
#             parse("Nipples slightly enlarged."),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=0, end=25
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__07(self):
#         self.assertEqual(parse("Nipples pigmented."), [])
#
#     def test_nipple_enlarged__08(self):
#         self.assertEqual(
#             parse("no scars or emb., nip. sm., low fat"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=18, end=25
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__09(self):
#         self.assertEqual(parse("; teats visible,"), [])
#
#     def test_nipple_enlarged__10(self):
#         self.assertEqual(
#             parse(", LG UTERUS & TEATS,"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=2, end=19
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__11(self):
#         self.assertEqual(parse("4 teats post lac."), [])
#
#     def test_nipple_enlarged__12(self):
#         self.assertEqual(parse("lactating, mammary glands much swollen"), [])
#
#     def test_nipple_enlarged__13(self):
#         self.assertEqual(
#             parse("VO, NE, mamm. lg."),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=8, end=16
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__14(self):
#         self.assertEqual(parse("mammary glands active"), [])
#
#     def test_nipple_enlarged__15(self):
#         self.assertEqual(
#             parse("mammae conspicuous; lactating;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=0, end=18
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__16(self):
#         self.assertEqual(parse("; MAMMARY TISSSUE ABSENT;"), [])
#
#     def test_nipple_enlarged__17(self):
#         self.assertEqual(
#             parse("; reproductive data=no nipples showing, uterus found;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=20, end=30
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__18(self):
#         self.assertEqual(
#             parse("nipples small, moderate fat"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=0, end=13
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__19(self):
#         self.assertEqual(
#             parse("uterus enlarged, large nipples"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=17, end=30
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__20(self):
#         self.assertEqual(parse("nipples medium"), [])
#
#     def test_nipple_enlarged__21(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data=No placental scars or embryos. "
#                 "3 nipples prominent"
#             ),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=51, end=68
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__22(self):
#         self.assertEqual(
#             parse("reproductive data=nipple dev: none, no plsc,"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=18, end=34
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__23(self):
#         self.assertEqual(parse("reproductive data=nipple dev, 3R+0L=3 plsc ;"), [])
#
#     def test_nipple_enlarged__24(self):
#         self.assertEqual(parse(", pelvis slgt sep, nipp med+, no scars,"), [])
#
#     def test_nipple_enlarged__25(self):
#         self.assertEqual(
#             parse("reproductive data=Ad. mammery glands developed " "but no nipples"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=51, end=61
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__26(self):
#         self.assertEqual(
#             parse("reproductive data=vulva open; no nipples apparent ;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=30, end=40
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__27(self):
#         self.assertEqual(
#             parse("reproductive data=Lactating; clear & enlarged teats ;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=37, end=51
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__28(self):
#         self.assertEqual(
#             parse("reproductive data=enlargedNipples ;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=18, end=33
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__29(self):
#         self.assertEqual(
#             parse("reproductive data=OEN;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="enlarged", start=18, end=21
#                 )
#             ],
#         )
#
#     def test_nipple_enlarged__30(self):
#         self.assertEqual(
#             parse("reproductive data=OSN;"),
#             [
#                 NippleEnlarged(
#                     trait="nipple_enlarged", enlarged="not enlarged", start=18, end=21
#                 )
#             ],
#         )
