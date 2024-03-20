import unittest

from ranges.pylib.rules.embryo import Embryo
from tests.setup import parse


class TestEmbryoCount(unittest.TestCase):
    def test_embryo_01(self):
        """It handles a count with a suffix label."""
        self.maxDiff = None
        self.assertEqual(
            parse("pregnant; 4 emb"),
            [Embryo(trait="embryo", count=4, start=10, end=15)],
        )

    def test_embryo_02(self):
        """It parses an absence notation."""
        self.assertEqual(
            parse("not pregnant; no embs"),
            [
                Embryo(trait="embryo", count=0, start=0, end=12),
                Embryo(trait="embryo", count=0, start=14, end=21),
            ],
        )

    def test_embryo_03(self):
        """It parses counts per side."""
        self.assertEqual(
            parse("pregnant; 4 emb 3L 1R"),
            [Embryo(trait="embryo", count=4, left=3, right=1, start=10, end=21)],
        )

    def test_embryo_04(self):
        """It parses sides without a total."""
        self.assertEqual(
            parse("embryos 2R-1L"),
            [Embryo(trait="embryo", count=3, left=1, right=2, start=0, end=13)],
        )

    def test_embryo_05(self):
        """It does not pick up other embryo notations."""
        self.assertEqual(parse("embryo of 34402"), [])

    def test_embryo_06(self):
        """It parses another left/right separated by a comma."""
        self.assertEqual(
            parse("emb.1R,1L; "),
            [Embryo(trait="embryo", count=2, left=1, right=1, start=0, end=9)],
        )

    def test_embryo_07(self):
        """It handles female/male counts."""
        self.assertEqual(
            parse("7 embryos, 4 male, and 3 female"),
            [Embryo(trait="embryo", count=7, male=4, female=3, start=0, end=31)],
        )

    def test_embryo_08(self):
        """It handles count surrounded by parentheses."""
        self.assertEqual(
            parse("reproductive data=5 embryos (3L, 2R);"),
            [Embryo(trait="embryo", count=5, left=3, right=2, start=18, end=36)],
        )

    def test_embryo_09(self):
        """It handles an adjective between the count and label."""
        self.assertEqual(
            parse("reproductive data= 4 small embryos."),
            [Embryo(trait="embryo", count=4, start=19, end=34)],
        )

    def test_embryo_10(self):
        """It handles a length before the side counts."""
        self.assertEqual(
            parse("; 4 emb. x 07 mm, 3L2R"),
            [
                Embryo(
                    trait="embryo", length=7, count=4, left=3, right=2, start=2, end=22
                )
            ],
        )

    def test_embryo_11(self):
        """It handles a count length combo without sides."""
        self.assertEqual(
            parse('; 3 emb. x 06 mm.",'),
            [Embryo(trait="embryo", length=6, count=3, start=2, end=17)],
        )

    def test_embryo_12(self):
        """It recognizes a slash as a separator."""
        self.assertEqual(
            parse("reproductive data: 3 embryos - 14 mm, 2R/1L;"),
            [
                Embryo(
                    trait="embryo",
                    length=14,
                    count=3,
                    left=1,
                    right=2,
                    start=19,
                    end=43,
                )
            ],
        )

    def test_embryo_13(self):
        """It gets a zero count with separating words."""
        self.assertEqual(
            parse("Med. nipples, no scars or embryos, mod. fat"),
            [Embryo(trait="embryo", count=0, start=14, end=33)],
        )

    def test_embryo_14(self):
        """It should skip this pattern."""
        self.assertEqual(parse("Fetus of AF 25577 (SHEID-99)."), [])

    def test_embryo_15(self):
        """It parses longer side notations."""
        self.assertEqual(
            parse(", 4 fetuses on left, 1 on right"),
            [Embryo(trait="embryo", count=5, left=4, right=1, start=2, end=31)],
        )

    def test_embryo_16(self):
        """It handles words between the count and label."""
        self.assertEqual(
            parse("ONLY. 3 VERY LARGE FOETI(50)."),
            [Embryo(trait="embryo", count=3, start=6, end=24)],
        )

    def test_embryo_17(self):
        """It parses the total count at the end."""
        self.assertEqual(
            parse("Foeti: 2R4L=6;"),
            [Embryo(trait="embryo", count=6, left=4, right=2, start=0, end=13)],
        )

    def test_embryo_18(self):
        """It should only parse the first & second notations."""
        self.assertEqual(
            parse("pregnant; 1 emb; CR-74; emb W-25; emb WT-4.8"),
            [
                Embryo(trait="embryo", count=1, start=10, end=15),
                Embryo(
                    trait="embryo", length=74, units_inferred=True, start=17, end=22
                ),
            ],
        )

    def test_embryo_19(self):
        """It parses a mixed notation when sides lead the counts."""
        self.assertEqual(
            parse("no scars, horns R 2 emb x 11, L 4 emb x 11,"),
            [
                Embryo(
                    trait="embryo",
                    length=11,
                    count=6,
                    left=4,
                    right=2,
                    start=16,
                    end=37,
                ),
            ],
        )

    def test_embryo_20(self):
        """It parses a numeric word count."""
        self.assertEqual(
            parse("FOUR EMBS, 25MM"),
            [Embryo(trait="embryo", length=25, count=4, start=0, end=15)],
        )

    def test_embryo_21(self):
        """It parses a crown-rump length."""
        self.assertEqual(
            parse("crown-rump length=13 mm"),
            [Embryo(trait="embryo", length=13, start=0, end=23)],
        )

    def test_embryo_22(self):
        """It handles no units."""
        self.assertEqual(
            parse("Embryo crown-rump length 22"),
            [
                Embryo(
                    trait="embryo",
                    length=22,
                    units_inferred=True,
                    start=0,
                    end=27,
                )
            ],
        )

    def test_embryo_23(self):
        """It handles odd interstitial characters."""
        self.assertEqual(
            parse("3 embs/2L+2R/cr=X34mm"),
            [
                Embryo(trait="embryo", start=0, end=12, count=3, left=2, right=2),
                Embryo(trait="embryo", start=13, end=21, length=34.0),
            ],
        )

    def test_embryo_24(self):
        """It parses a length with a width."""
        self.assertEqual(
            parse(", cr=5x5 ;"),
            [
                Embryo(
                    trait="embryo",
                    length=5,
                    width=5,
                    units_inferred=True,
                    start=2,
                    end=8,
                )
            ],
        )

    def test_embryo_25(self):
        """It parses a length with a width and units."""
        self.assertEqual(
            parse("; reproductive data=cr=9x8mm"),
            [Embryo(trait="embryo", length=9, width=8, start=20, end=28)],
        )

    def test_embryo_26(self):
        """It parses scars."""
        self.assertEqual(
            parse("2 embryo scars left horn, 1 right"),
            [
                Embryo(
                    trait="embryo",
                    count=3,
                    left=2,
                    right=1,
                    start=0,
                    end=33,
                )
            ],
        )

    def test_embryo_27(self):
        """It does not pick up the '1 in'."""
        self.assertEqual(
            parse("2 embryo scars, 1 in each horn, lactating"),
            [
                Embryo(
                    trait="embryo",
                    count=2,
                    start=0,
                    end=8,
                )
            ],
        )

    def test_embryo_28(self):
        """It picks up the presence of an embryo."""
        self.assertEqual(
            parse("Near-term fetus"),
            [Embryo(trait="embryo", count=1, start=0, end=15)],
        )

    def test_embryo_29(self):
        self.assertEqual(
            parse("6 near-term embryos."),
            [Embryo(trait="embryo", count=6, start=0, end=19)],
        )

    def test_embryo_30(self):
        self.maxDiff = None
        self.assertEqual(
            parse("2 embryos right horn, 3 left, ~9x10mm"),
            [
                Embryo(
                    trait="embryo",
                    count=5,
                    length=9,
                    width=10,
                    left=3,
                    right=2,
                    start=0,
                    end=37,
                )
            ],
        )

    def test_embryo_31(self):
        self.assertEqual(
            parse("Fetus on left, 18mm crown to rump."),
            [
                Embryo(trait="embryo", count=1, left=1, start=0, end=13),
                Embryo(trait="embryo", length=18, start=15, end=33),
            ],
        )

    # def test_embryo_40(self):
    #     self.assertEqual(
    #         parse("3 embryos L side, 1 R. Mammaries developing."),
    #         [Embryo(trait="embryo", count=4, left=3, right=1, start=0, end=21)],
    #     )
    #
    # def test_embryo_41(self):
    #     self.assertEqual(
    #         parse(
    #             "corp. lut. 2L, 4R, no scars, embryos 2L, 4R, "
    #             "nipples small, moderate fat"
    #         ),
    #         [Embryo(trait="embryo", count=6, left=2, right=4, start=29, end=43)],
    #     )
    #
    # def test_embryo_42(self):
    #     self.assertEqual(
    #         parse("perforate; 2L 2R emb; CR-9; 1L R emb; mammary"),
    #         [Embryo(trait="embryo", count=4, left=2, right=2, start=11, end=20)],
    #     )
    #
    # def test_embryo_43(self):
    #     self.assertEqual(
    #         parse("Embryos: 5R x 4L c.r. 3 mm."),
    #         [Embryo(trait="embryo", count=9, left=4, right=5, start=0, end=16)],
    #     )
    #
    # def test_embryo_44(self):
    #     self.assertEqual(
    #         parse("reproductive data=8 3mm. embryos."),
    #         [Embryo(trait="embryo", count=8, start=18, end=32)],
    #     )
    #
    # def test_embryo_45(self):
    #     self.assertEqual(
    #         parse("reproductive data=mammae (4L, 5R)"),
    #         [Embryo(trait="embryo", count=9, left=4, right=5, start=0, end=32)],
    #     )
    #
    # def test_embryo_46(self):
    #     self.assertEqual(
    #         parse("embs.=1R,!L"),
    #         [Embryo(trait="embryo", count=1, left=1, right=1, start=0, end=11)],
    #     )
    #
    # def test_embryo_47(self):
    #     self.assertEqual(
    #         parse("(260)-(150)-37-14  47.6g  embs 1R,1L"),
    #         [Embryo(trait="embryo", count=2, left=1, right=1, start=26, end=36)],
    #     )
    #
    # def test_embryo_48(self):
    #     self.assertEqual(
    #         parse("1 embryo right horn 4x8mm, 1 embryo left horn"),
    #         [
    #             {"end": 14, "right": 1, "start": 0, "count": 1},
    #             {"end": 40, "left": 1, "start": 27, "count": 1},
    #         ],
    #     )
    #
    # def test_embryo_49(self):
    #     self.assertEqual(
    #         parse("embs=1R (CR=32 mm), 1L (CR=32&28mm) ;"),
    #         [{"end": 22, "left": 1, "right": 1, "start": 0, "count": 2}],
    #     )
    #
    # def test_embryo_50(self):
    #     self.assertEqual(
    #         parse("reproductive data=embryos left:3 right:3 ;"),
    #         [{"end": 40, "left": 3, "right": 3, "start": 18, "count": 6}],
    #     )
    #
    # def test_embryo_51(self):
    #     self.assertEqual(
    #         parse("R horn 5embsx18mm, L horn 1 resorb embx5mm, 1embx18mm; "),
    #         [
    #             {"end": 27, "left": 1, "right": 5, "start": 0, "count": 6},
    #             {"end": 48, "start": 44, "count": 1},
    #         ],
    #     )
    #
    # def test_embryo_52(self):
    #     self.assertEqual(
    #         parse("emb 5x21 (R2 L3),"),
    #         [{"end": 15, "left": 3, "right": 2, "start": 0, "count": 5}],
    #     )
    #
    # def test_embryo_53(self):
    #     self.assertEqual(
    #         parse("emb 1x13( R), 1+ pl sc (L),"),
    #         [{"end": 11, "right": 1, "start": 0, "count": 1}],
    #     )
    #
    # def test_embryo_54(self):
    #     self.assertEqual(
    #         parse("reproductive data=3 large, 20mm embryos: 2R, 1L."),
    #         [{"end": 47, "left": 1, "right": 2, "start": 32, "count": 3}],
    #     )
    #
    # def test_embryo_55(self):
    #     self.assertEqual(
    #         parse("reproductive data=5 3mm embryos: 1R, 4L"),
    #         [{"end": 39, "left": 4, "right": 1, "start": 18, "count": 5}],
    #     )
    #
    # def test_embryo_56(self):
    #     self.assertEqual(
    #         parse("5 3mm embyros: 1R, 4L"),
    #         [{"end": 21, "left": 4, "right": 1, "start": 0, "count": 5}],
    #     )
    #
    # def test_embryo_57(self):
    #     self.assertEqual(
    #         parse(
    #             """vulva w/sm blood clot; R horn 2 mmx2.5 mm,
    #             L 1 emb x 3 mm and 1 emb 2.5 mm;"""
    #         ),
    #         [
    #             {"end": 66, "start": 61, "count": 1},
    #             {"end": 83, "start": 78, "count": 1},
    #         ],
    #     )
    #
    # def test_embryo_58(self):
    #     self.assertEqual(
    #         parse("2 embryos each side (4 total), 3x4mm"),
    #         [{"end": 19, "left": 2, "right": 2, "start": 0, "count": 4}],
    #     )
    #
    # def test_embryo_59(self):
    #     self.assertEqual(
    #         parse("reproductive data=2Rx1Lx23 mm fetuses"),
    #         [{"end": 24, "left": 1, "right": 2, "start": 0, "count": 3}],
    #     )
    #
    # def test_embryo_60(self):
    #     self.assertEqual(
    #         parse("VC, R2, L3=19, embryos saved"),
    #         [{"end": 22, "left": 3, "right": 2, "start": 4, "count": 5}],
    #     )
    #
    # def test_embryo_61(self):
    #     self.assertEqual(
    #         parse("VO, mamm. lg., 4L, CRL=26, embryos saved"),
    #         [{"end": 34, "left": 4, "start": 15, "count": 4}],
    #     )
    #
    # def test_embryo_62(self):
    #     self.assertEqual(
    #         parse("corpora lutea: L-4, R-5; embryos: L-2, R-3 (5x3mm)"),
    #         [{"end": 42, "left": 2, "right": 3, "start": 25, "count": 5}],
    #     )
    #
    # def test_embryo_63(self):
    #     self.assertEqual(
    #         parse("Pregnant with 4 embryos (rt = 1, lt = 3;"),
    #         [{"end": 39, "left": 3, "right": 1, "start": 14, "count": 4}],
    #     )
    #
    # def test_embryo_64(self):
    #     self.assertEqual(
    #         parse("RBS 4029; EMB-R 2, EMB-L 3, CR 8 mm"),
    #         [{"end": 26, "left": 3, "right": 2, "start": 10, "count": 5}],
    #     )
    #
    # def test_embryo_65(self):
    #     self.assertEqual(
    #         parse("reproductive data=4 2.5mm embryos"),
    #         [{"end": 33, "start": 18, "count": 4}],
    #     )
    #
    # def test_embryo_66(self):
    #     self.assertEqual(
    #         parse("reproductive data=Emb = 4 : CR = 17mm : 2R x 2L"),
    #         [{"end": 47, "left": 2, "right": 2, "start": 18, "count": 4}],
    #     )
    #
    # def test_embryo_67(self):
    #     self.assertEqual(
    #         parse("reproductive data=3 embryos (3R, 1L)"),
    #         [{"end": 35, "left": 1, "right": 3, "start": 18, "count": 4}],
    #     )
    #
    # def test_embryo_68(self):
    #     self.assertEqual(
    #         parse("Embryos (R2, L4, 10mm)."),
    #         [{"end": 35, "left": 1, "right": 3, "start": 18, "count": 4}],
    #     )


#     def test_embryo_12(self):
#         self.assertEqual(
#             parse(
#                 "reproductive data=Embryos: 2 (1 resorbing) R, 3 Left, "
#                 "crown-rump length, 36 mm."
#             ),
#             [Embryo(trait="embryo", length=36, start=54, end=78)],
#         )
#
#     def test_embryo_13(self):
#         self.assertEqual(parse("collector=CR 910025, E. E. Makela ;"), [])
#
#     def test_embryo_14(self):
#         self.assertEqual(
#             parse(
#                 "Embryos of AF 48621. Eight embryos of AF 48621."
#             ),
#             [Embryo(trait="embryo", length=6, units=None,
#             units_inferred=True, start=49, end=53)],
#         )
#
#     def test_embryo_15(self):
#         self.assertEqual(parse("snap 47: middle Cow Cr."), [])
#
#     def test_embryo_16(self):
#         self.assertEqual(parse("headwaters Kaluich Cr, ca 1500 ft"), [])
#
#     def test_embryo_17(self):
#         self.assertEqual(
#             parse("CR=15mm left intact"),
#             [Embryo(trait="embryo", length=15, start=147, end=154)],
#         )
#
#     def test_embryo_18(self):
#         self.assertEqual(
#             parse("OCGR pg, 4 embs, 2R, 2L, 12 mm 4 2 2"),
#             [
#                 Embryo(trait="embryo", length=12, start=11, end=36),
#                 Embryo(trait="embryo", length=4, start=11, end=36),
#                 Embryo(trait="embryo", length=2, start=11, end=36),
#                 Embryo(trait="embryo", length=2, start=11, end=36),
#             ],
#         )
#
#     def test_embryo_19(self):
#         self.assertEqual(
#             parse("Mammals 7 embs, 3 mm"),
#             [Embryo(trait="embryo", length=3, start=10, end=20)],
#         )
#
#     def test_embryo_20(self):
#         self.assertEqual(
#             parse("Mammals 3 embs, 24mm"),
#             [Embryo(trait="embryo", length=24, start=10, end=20)],
#         )
#
#     def test_embryo_21(self):
#         self.assertEqual(
#             parse("3 embs, 2L, 1R, 19 mm, 17 mm, 17 mm"),
#             [
#                 Embryo(trait="embryo", length=19, start=2, end=35),
#                 Embryo(trait="embryo", length=17, start=2, end=35),
#                 Embryo(trait="embryo", length=17, start=2, end=35),
#             ],
#         )
#
#     def test_embryo_22(self):
#         self.assertEqual(
#             parse(
#                 "Mammals vagina open; mammae tiny; not lactating9 embryos; " "cr-10 ?"
#             ),
#             [
#                 Embryo(trait="embryo",
#                     length=10,
#                     units_inferred=True,
#                     start=58,
#                     end=65,
#                     uncertain=True,
#                 )
#             ],
#         )
#
#     def test_embryo_23(self):
#         self.assertEqual(
#             parse("4 embs: 2(R)&2(L)=9mm "),
#             [Embryo(trait="embryo", length=9, start=2, end=21)],
#         )
#
#     def test_embryo_24(self):
#         self.assertEqual(
#             parse("reproductive data=embryos: 2L, 1R-0.5x0.5 mm ;"),
#             [
#                 Embryo(trait="embryo",
#                     length=[0.5, 0.5], start=18, end=44
#                 )
#             ],
#         )
# 1
#     def test_embryo_25(self):
#         self.assertEqual(
#             parse("7 embryos, 4 male, and 3 female, CRL=59 mm;"),
#             [Embryo(trait="embryo", length=59.0, start=33, end=42)],
#         )
#
#     def test_embryo_27(self):
#         self.assertEqual(
#             parse(
#                 "uterus large, embryos 1 + 1 = 2 (29763, 29764) CR = 30 mm."
#             ),
#             [Embryo(trait="embryo", length=30.0, start=47, end=57)],
#         )
#
#     def test_embryo_28(self):
#         self.assertEqual(
#             parse(
#                 "uterus large, CR = 30 mm."
#             ),
#             [Embryo(trait="embryo", length=30.0, start=47, end=57)],
#         )
