import unittest

from ranges.pylib.rules.embryo_length import EmbryoLength
from tests.setup import parse


class TestEmbryoLength(unittest.TestCase):
    def test_embryo_length_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse("crown-rump length=13 mm"),
            [EmbryoLength(trait="embryo_length", length=13, start=0, end=23)],
        )

    def test_embryo_length_02(self):
        self.assertEqual(
            parse("Embryo crown-rump length 22"),
            [
                EmbryoLength(
                    trait="embryo_length",
                    length=22,
                    units_inferred=True,
                    start=0,
                    end=27,
                )
            ],
        )


#     def test_embryo_length_03(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data: 4 embryos - 15 mm, crown-rump length"
#             ),
#             [EmbryoLength(trait="embryo_length", length=15, start=21, end=55)],
#         )
#
#     def test_embryo_length_04(self):
#         self.assertEqual(
#             parse(", CR (crown-rump length) =7 ;"),
#             [EmbryoLength(trait="embryo_length", length=7, start=6, end=27)],
#         )
#
#     def test_embryo_length_05(self):
#         self.assertEqual(
#             parse(", CRL=59 mm; "),
#             [EmbryoLength(trait="embryo_length", length=59, start=2, end=11)],
#         )
#
#     def test_embryo_length_06(self):
#         self.assertEqual(
#             parse("pregnant; 1 emb; cr-28"),
#             [EmbryoLength(trait="embryo_length", length=28,
#             inferred=True, start=17, end=22)],
#         )
#
#     def test_embryo_length_07(self):
#         self.assertEqual(
#             parse("embryos left horn, cr-rump: 23mm."),
#             [EmbryoLength(trait="embryo_length", length=23, start=19, end=32)],
#         )
#
#     def test_embryo_length_08(self):
#         self.assertEqual(
#             parse("4 embs/1R/3L/cr=2mm"),
#             [EmbryoLength(trait="embryo_length", length=2, start=13, end=19)],
#         )
#
#     def test_embryo_length_09(self):
#         self.assertEqual(
#             parse("3 embs/2L+2R/cr=X34mm"),
#             [EmbryoLength(trait="embryo_length", length=34,  start=13, end=21)],
#         )
#
#     def test_embryo_length_10(self):
#         self.assertEqual(
#             parse(", cr=5x5 ;"),
#             [EmbryoLength(trait="embryo_length", length=[5, 5], units_inferred=True,
#             start=2, end=8)],
#         )
#
#     def test_embryo_length_11(self):
#         self.assertEqual(
#             parse("sex=recorded as unknown ; reproductive data=cr=9x8mm"),
#             [EmbryoLength(trait="embryo_length", length=[9, 8], start=44, end=52)],
#         )
#
#     def test_embryo_length_12(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data=Embryos: 2 (1 resorbing) R, 3 Left, "
#                 "crown-rump length, 36 mm."
#             ),
#             [EmbryoLength(trait="embryo_length", length=36, start=54, end=78)],
#         )
#
#     def test_embryo_length_13(self):
#         self.assertEqual(parse("collector=CR 910025, E. E. Makela ;"), [])
#
#     def test_embryo_length_14(self):
#         self.assertEqual(
#             parse(
#                 "Embryos of AF 48621. Eight embryos of AF 48621.  CR=6"
#             ),
#             [EmbryoLength(trait="embryo_length", length=6, units=None,
#             units_inferred=True, start=49, end=53)],
#         )
#
#     def test_embryo_length_15(self):
#         self.assertEqual(parse("snap 47: middle Cow Cr."), [])
#
#     def test_embryo_length_16(self):
#         self.assertEqual(parse("headwaters Kaluich Cr, ca 1500 ft"), [])
#
#     def test_embryo_length_17(self):
#         self.assertEqual(
#             parse("CR=15mm left intact"),
#             [EmbryoLength(trait="embryo_length", length=15, start=147, end=154)],
#         )
#
#     def test_embryo_length_18(self):
#         self.assertEqual(
#             parse("OCGR pg, 4 embs, 2R, 2L, 12 mm 4 2 2"),
#             [
#                 EmbryoLength(trait="embryo_length", length=12, start=11, end=36),
#                 EmbryoLength(trait="embryo_length", length=4, start=11, end=36),
#                 EmbryoLength(trait="embryo_length", length=2, start=11, end=36),
#                 EmbryoLength(trait="embryo_length", length=2, start=11, end=36),
#             ],
#         )
#
#     def test_embryo_length_19(self):
#         self.assertEqual(
#             parse("Mammals 7 embs, 3 mm"),
#             [EmbryoLength(trait="embryo_length", length=3, start=10, end=20)],
#         )
#
#     def test_embryo_length_20(self):
#         self.assertEqual(
#             parse("Mammals 3 embs, 24mm"),
#             [EmbryoLength(trait="embryo_length", length=24, start=10, end=20)],
#         )
#
#     def test_embryo_length_21(self):
#         self.assertEqual(
#             parse("3 embs, 2L, 1R, 19 mm, 17 mm, 17 mm"),
#             [
#                 EmbryoLength(trait="embryo_length", length=19, start=2, end=35),
#                 EmbryoLength(trait="embryo_length", length=17, start=2, end=35),
#                 EmbryoLength(trait="embryo_length", length=17, start=2, end=35),
#             ],
#         )
#
#     def test_embryo_length_22(self):
#         self.assertEqual(
#             parse(
#                 "Mammals vagina open; mammae tiny; not lactating9 embryos; " "cr-10 ?"
#             ),
#             [
#                 EmbryoLength(trait="embryo_length",
#                     length=10,
#                     units_inferred=True,
#                     start=58,
#                     end=65,
#                     uncertain=True,
#                 )
#             ],
#         )
#
#     def test_embryo_length_23(self):
#         self.assertEqual(
#             parse("4 embs: 2(R)&2(L)=9mm "),
#             [EmbryoLength(trait="embryo_length", length=9, start=2, end=21)],
#         )
#
#     def test_embryo_length_24(self):
#         self.assertEqual(
#             parse("reproductive data=embryos: 2L, 1R-0.5x0.5 mm ;"),
#             [
#                 EmbryoLength(trait="embryo_length",
#                     length=[0.5, 0.5], start=18, end=44
#                 )
#             ],
#         )
# 1
#     def test_embryo_length_25(self):
#         self.assertEqual(
#             parse("7 embryos, 4 male, and 3 female, CRL=59 mm;"),
#             [EmbryoLength(trait="embryo_length", length=59.0, start=33, end=42)],
#         )
#
#     def test_embryo_length_27(self):
#         self.assertEqual(
#             parse(
#                 "uterus large, embryos 1 + 1 = 2 (29763, 29764) CR = 30 mm."
#             ),
#             [EmbryoLength(trait="embryo_length", length=30.0, start=47, end=57)],
#         )
#
#     def test_embryo_length_28(self):
#         self.assertEqual(
#             parse(
#                 "uterus large, CR = 30 mm."
#             ),
#             [EmbryoLength(trait="embryo_length", length=30.0, start=47, end=57)],
#         )
