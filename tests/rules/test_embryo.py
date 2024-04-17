import unittest

from ranges.pylib.rules.embryo import Embryo
from ranges.pylib.rules.nipple import Nipple
from ranges.pylib.rules.pregnancy_state import PregnancyState
from tests.setup import parse


class TestEmbryo(unittest.TestCase):
    def test_embryo_01(self):
        """It handles a count with a suffix label."""
        self.maxDiff = None
        self.assertEqual(
            parse("4 emb"),
            [Embryo(count=4, start=0, end=5)],
        )

    def test_embryo_02(self):
        """It parses an absence notation."""
        self.maxDiff = None
        self.assertEqual(
            parse("not pregnant; no embs"),
            [
                PregnancyState(state="not pregnant", start=0, end=12),
                Embryo(count=0, start=14, end=21),
            ],
        )

    def test_embryo_03(self):
        """It parses counts per side."""
        self.assertEqual(
            parse("4 emb 3L 1R"),
            [Embryo(count=4, left=3, right=1, start=0, end=11)],
        )

    def test_embryo_04(self):
        """It parses sides without a total."""
        self.assertEqual(
            parse("embryos 2R-1L"),
            [Embryo(count=3, left=1, right=2, start=0, end=13)],
        )

    def test_embryo_05(self):
        """It does not pick up other embryo notations."""
        self.assertEqual(parse("embryo of 34402"), [])

    def test_embryo_06(self):
        """It parses another left/right separated by a comma."""
        self.assertEqual(
            parse("emb.1R,1L; "),
            [Embryo(count=2, left=1, right=1, start=0, end=9)],
        )

    def test_embryo_07(self):
        """It handles female/male counts."""
        self.assertEqual(
            parse("7 embryos, 4 male, and 3 female"),
            [Embryo(count=7, male=4, female=3, start=0, end=31)],
        )

    def test_embryo_08(self):
        """It handles count surrounded by parentheses."""
        self.assertEqual(
            parse("reproductive data=5 embryos (3L, 2R);"),
            [Embryo(count=5, left=3, right=2, start=18, end=36)],
        )

    def test_embryo_09(self):
        """It handles an adjective between the count and label."""
        self.assertEqual(
            parse("reproductive data= 4 small embryos."),
            [Embryo(count=4, start=19, end=34)],
        )

    def test_embryo_10(self):
        """It handles a length before the side counts."""
        self.assertEqual(
            parse("; 4 emb. x 07 mm, 3L2R"),
            [Embryo(length=7, count=4, left=3, right=2, start=2, end=22)],
        )

    def test_embryo_11(self):
        """It handles a count length combo without sides."""
        self.assertEqual(
            parse('; 3 emb. x 06 mm.",'),
            [Embryo(length=6, count=3, start=2, end=17)],
        )

    def test_embryo_12(self):
        """It recognizes a slash as a separator."""
        self.assertEqual(
            parse("reproductive data: 3 embryos - 14 mm, 2R/1L;"),
            [
                Embryo(
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
            [
                Nipple(state="medium", start=0, end=12),
                Embryo(count=0, start=14, end=33),
            ],
        )

    def test_embryo_14(self):
        """It should skip this pattern."""
        self.assertEqual(parse("Fetus of AF 25577 (SHEID-99)."), [])

    def test_embryo_15(self):
        """It parses longer side notations."""
        self.assertEqual(
            parse(", 4 fetuses on left, 1 on right"),
            [Embryo(count=5, left=4, right=1, start=2, end=31)],
        )

    def test_embryo_16(self):
        """It handles words between the count and label."""
        self.assertEqual(
            parse("ONLY. 3 VERY LARGE FOETI(50)."),
            [Embryo(count=3, start=6, end=24)],
        )

    def test_embryo_17(self):
        """It parses the total count at the end."""
        self.assertEqual(
            parse("Foeti: 2R4L=6;"),
            [Embryo(count=6, left=4, right=2, start=0, end=13)],
        )

    def test_embryo_18(self):
        """It should only parse the first & second notations."""
        self.assertEqual(
            parse("pregnant; 1 emb; CR-74; emb W-25; emb WT-4.8"),
            [
                PregnancyState(state="pregnant", start=0, end=8),
                Embryo(count=1, start=10, end=15),
                Embryo(length=74, units_inferred=True, start=17, end=22),
            ],
        )

    def test_embryo_19(self):
        """It parses a mixed notation when sides lead the counts."""
        self.assertEqual(
            parse("no scars, horns R 2 emb x 11, L 4 emb x 11,"),
            [
                Embryo(
                    length=11,
                    count=6,
                    left=4,
                    right=2,
                    start=16,
                    end=33,
                ),
            ],
        )

    def test_embryo_20(self):
        """It parses a numeric word count."""
        self.assertEqual(
            parse("FOUR EMBS, 25MM"),
            [Embryo(length=25, count=4, start=0, end=15)],
        )

    def test_embryo_21(self):
        """It parses a crown-rump length."""
        self.assertEqual(
            parse("crown-rump length=13 mm"),
            [Embryo(length=13, start=0, end=23)],
        )

    def test_embryo_22(self):
        """It handles no units."""
        self.assertEqual(
            parse("Embryo crown-rump length 22"),
            [
                Embryo(
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
                Embryo(start=0, end=12, count=3, left=2, right=2),
                Embryo(start=13, end=21, length=34.0),
            ],
        )

    def test_embryo_24(self):
        """It parses a length with a width."""
        self.assertEqual(
            parse(", cr=5x5 ;"),
            [
                Embryo(
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
            [Embryo(length=9, width=8, start=20, end=28)],
        )

    def test_embryo_26(self):
        """It parses scars."""
        self.assertEqual(
            parse("2 embryo scars left horn, 1 right"),
            [
                Embryo(
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
            parse("2 embryo scars, 1 in each horn,"),
            [
                Embryo(
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
            [Embryo(count=1, start=0, end=15)],
        )

    def test_embryo_29(self):
        """It gets a count with a presence term."""
        self.assertEqual(
            parse("6 near-term embryos."),
            [Embryo(count=6, start=0, end=19)],
        )

    def test_embryo_30(self):
        """It parses a mixed count/length string with both a length and a width."""
        self.assertEqual(
            parse("2 embryos right horn, 3 left, ~9x10mm"),
            [
                Embryo(
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
        """It handles a side for presence/absence."""
        self.assertEqual(
            parse("Fetus on left, 18mm crown to rump."),
            [
                Embryo(count=1, left=1, start=0, end=13),
                Embryo(length=18, start=15, end=33),
            ],
        )

    def test_embryo_32(self):
        """It handles this key format."""
        self.assertEqual(
            parse("3 embryos L side, 1 R. Mammaries developing."),
            [Embryo(count=4, left=3, right=1, start=0, end=22)],
        )

    def test_embryo_33(self):
        """It handles a x as a side separator."""
        self.assertEqual(
            parse("Embryos: 5R x 4L c.r. 3 mm."),
            [
                Embryo(count=9, left=4, right=5, start=0, end=16),
                Embryo(length=3, start=17, end=27),
            ],
        )

    def test_embryo_34(self):
        """It handles a single side."""
        self.assertEqual(
            parse("embs.=1R,!L"),
            [Embryo(count=1, right=1, start=0, end=8)],
        )

    def test_embryo_35(self):
        """It parses a length/width in the middle of the counts."""
        self.assertEqual(
            parse("1 embryo right horn 4x8mm, 1 embryo left horn"),
            [
                Embryo(
                    start=0,
                    end=40,
                    length=4.0,
                    width=8.0,
                    count=2,
                    left=1,
                    right=1,
                )
            ],
        )

    def test_embryo_36(self):
        """It parses a mixed notation with a leading key."""
        self.assertEqual(
            parse("embs=1R (CR=32 mm), 1L (CR=32&28mm) ;"),
            [
                Embryo(
                    start=0,
                    end=22,
                    length=32,
                    count=2,
                    left=1,
                    right=1,
                ),
                Embryo(start=24, end=29, length=32, units_inferred=True),
            ],
        )

    def test_embryo_37(self):
        """It handles a key merged with a cross."""
        self.assertEqual(
            parse("R horn 5embsx18mm, L horn 1 resorb embx5mm, 1embx18mm; "),
            [
                Embryo(
                    start=0,
                    end=27,
                    length=18,
                    count=6,
                    left=1,
                    right=5,
                ),
                Embryo(start=35, end=42, length=5),
                Embryo(start=44, end=53, length=18, count=1),
            ],
        )

    def test_embryo_38(self):
        """It handles the side inside of parentheses."""
        self.assertEqual(
            parse("emb 5x21 (R2 L3),"),
            [
                Embryo(
                    start=0,
                    end=16,
                    length=21,
                    count=5,
                    left=3,
                    right=2,
                ),
            ],
        )

    def test_embryo_39(self):
        """It handles a few words inbetween the sides."""
        self.assertEqual(
            parse("emb 1x13( R), 1+ pl sc (L),"),
            [
                Embryo(
                    start=0,
                    end=26,
                    length=13,
                    count=2,
                    left=1,
                    right=1,
                ),
            ],
        )

    def test_embryo_40(self):
        """It handles the key after the length."""
        self.assertEqual(
            parse("reproductive data=3 large, 20mm embryos: 2R, 1L."),
            [
                Embryo(
                    start=27,
                    end=48,
                    length=20,
                    count=3,
                    left=1,
                    right=2,
                ),
            ],
        )

    def test_embryo_41(self):
        """It correctly parses numbers being next to each other."""
        self.assertEqual(
            parse("reproductive data=5 3mm embryos: 1R, 4L"),
            [
                Embryo(
                    start=18,
                    end=39,
                    length=3,
                    count=5,
                    left=4,
                    right=1,
                ),
            ],
        )

    def test_embryo_42(self):
        """It handles a missing total count."""
        self.assertEqual(
            parse("""L 1 emb x 3 mm and 1 emb 2.5 mm;"""),
            [
                Embryo(
                    start=0,
                    end=14,
                    length=3,
                    count=1,
                    left=1,
                ),
                Embryo(
                    start=19,
                    end=31,
                    length=2.5,
                    count=1,
                ),
            ],
        )

    def test_embryo_43(self):
        """It parses an 'each side' notation."""
        self.assertEqual(
            parse("2 embryos each side (4 total), 3x4mm"),
            [
                Embryo(
                    start=0,
                    end=36,
                    length=3,
                    width=4,
                    count=4,
                    left=2,
                    right=2,
                ),
            ],
        )

    def test_embryo_44(self):
        """It handles a key at the end of the notation."""
        self.assertEqual(
            parse("reproductive data=2Rx1Lx23 mm fetuses"),
            [
                Embryo(
                    start=18,
                    end=37,
                    length=23,
                    count=3,
                    left=1,
                    right=2,
                ),
            ],
        )

    def test_embryo_45(self):
        """It handles the sides being inside of parentheses."""
        self.maxDiff = None
        self.assertEqual(
            parse("Pregnant with 4 embryos (rt = 1, lt = 3;"),
            [
                PregnancyState(state="pregnant", start=0, end=8),
                Embryo(
                    start=14,
                    end=39,
                    count=4,
                    left=3,
                    right=1,
                ),
            ],
        )

    def test_embryo_46(self):
        """It handles the key in the middle of the notation."""
        self.assertEqual(
            parse("RBS 4029; EMB-R 2, EMB-L 3, CR 8 mm"),
            [
                Embryo(
                    start=10,
                    end=35,
                    length=8,
                    count=5,
                    left=3,
                    right=2,
                ),
            ],
        )

    def test_embryo_47(self):
        """It handles a lot of colons between the fields."""
        self.assertEqual(
            parse("reproductive data=Emb = 4 : CR = 17mm : 2R x 2L"),
            [
                Embryo(
                    end=47,
                    length=17,
                    left=2,
                    right=2,
                    start=18,
                    count=4,
                )
            ],
        )

    def test_embryo_48(self):
        """It allows parentheses around all values."""
        self.assertEqual(
            parse("Embryos (R2, L4, 10mm)."),
            [Embryo(length=10, end=22, left=4, right=2, start=0, count=6)],
        )

    def test_embryo_49(self):
        """It handles the length at index 3."""
        self.assertEqual(
            parse("4 embs: 2(R)&2(L)=9mm"),
            [Embryo(length=9, start=0, end=21, left=2, right=2, count=4)],
        )

    def test_embryo_50(self):
        """It parses an equation format."""
        self.assertEqual(
            parse("embryos 1 + 2 = 3 (29763, 29764) CR = 30 mm."),
            [
                Embryo(count=3, side1=1, side2=2, start=0, end=17),
                Embryo(length=30.0, start=33, end=44),
            ],
        )
