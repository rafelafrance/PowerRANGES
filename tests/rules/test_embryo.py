import unittest

from ranges.rules.embryo import Embryo
from ranges.rules.lactation_state import LactationState
from ranges.rules.pregnancy_state import PregnancyState
from tests.setup import parse


class TestEmbryo(unittest.TestCase):
    def test_embryo_01(self) -> None:
        """It handles a count with a suffix label."""
        self.maxDiff = None
        self.assertEqual(
            parse("4 emb"),
            [Embryo(count=4, start=0, end=5)],
        )

    def test_embryo_02(self) -> None:
        """It parses an absence notation."""
        self.maxDiff = None
        self.assertEqual(
            parse("not pregnant; no embs"),
            [
                PregnancyState(pregnancy=False, start=0, end=12),
                Embryo(count=0, start=14, end=21),
            ],
        )

    def test_embryo_03(self) -> None:
        """It parses counts per side."""
        self.assertEqual(
            parse("4 emb 3L 1R"),
            [Embryo(left=3, right=1, start=0, end=11, count=4)],
        )

    def test_embryo_04(self) -> None:
        """It parses sides without a total."""
        self.assertEqual(
            parse("embryos 2R-1L"),
            [Embryo(right=2, left=1, start=0, end=13, count=3)],
        )

    def test_embryo_05(self) -> None:
        """It does not pick up other embryo notations."""
        self.assertEqual(parse("embryo of 34402"), [])

    def test_embryo_06(self) -> None:
        """It parses another side1/side2 separated by a comma."""
        self.assertEqual(
            parse("emb.1R,1L; "),
            [Embryo(right=1, left=1, start=0, end=9, count=2)],
        )

    def test_embryo_07(self) -> None:
        """It handles female/male counts."""
        self.maxDiff = None
        self.assertEqual(
            parse("7 embryos, 4 male, and 3 female"),
            [Embryo(start=0, end=31, count=7)],
        )

    def test_embryo_08(self) -> None:
        """It handles count surrounded by parentheses."""
        self.assertEqual(
            parse("reproductive data=5 embryos (3L, 2R);"),
            [Embryo(left=3, right=2, start=18, end=36, count=5)],
        )

    def test_embryo_09(self) -> None:
        """It handles an adjective between the count and label."""
        self.assertEqual(
            parse("reproductive data= 4 small embryos."),
            [Embryo(start=19, end=34, count=4)],
        )

    def test_embryo_10(self) -> None:
        """It handles a length before the side counts."""
        self.assertEqual(
            parse("; 4 emb. x 07 mm, 3L2R"),
            [Embryo(length=7, left=3, right=2, start=2, end=22, count=5)],
        )

    def test_embryo_11(self) -> None:
        """It handles a count length combo without sides."""
        self.assertEqual(
            parse('; 3 emb. x 06 mm.",'),
            [Embryo(length=6, start=2, end=17, count=3)],
        )

    def test_embryo_12(self) -> None:
        """It recognizes a slash as a separator."""
        self.assertEqual(
            parse("reproductive data: 3 embryos - 14 mm, 2R/1L;"),
            [
                Embryo(
                    length=14,
                    right=2,
                    left=1,
                    count=3,
                    start=19,
                    end=43,
                )
            ],
        )

    def test_embryo_14(self) -> None:
        """It should skip this pattern."""
        self.assertEqual(parse("Fetus of AF 25577 (SHEID-99)."), [])

    def test_embryo_15(self) -> None:
        """It parses longer side notations."""
        self.assertEqual(
            parse(", 4 fetuses on side1, 1 on side2"),
            [Embryo(count=5, start=2, end=32)],
        )

    def test_embryo_16(self) -> None:
        """It handles words between the count and label."""
        self.assertEqual(
            parse("ONLY. 3 VERY LARGE FOETI(50)."),
            [Embryo(start=6, end=24, count=3)],
        )

    def test_embryo_17(self) -> None:
        """It parses the total count at the end."""
        self.assertEqual(
            parse("Foeti: 2R4L=6;"),
            [Embryo(right=2, left=4, start=0, end=13, count=6)],
        )

    def test_embryo_18(self) -> None:
        """It should only parse_fields the first & second notations."""
        self.assertEqual(
            parse("pregnant; 1 emb; CR-74; emb W-25; emb WT-4.8"),
            [
                PregnancyState(pregnancy=True, start=0, end=8),
                Embryo(start=10, end=15, count=1),
                Embryo(
                    length=74,
                    start=17,
                    end=22,
                    measured_from="crown",
                    units_inferred=True,
                ),
            ],
        )

    def test_embryo_19(self) -> None:
        """It parses a mixed notation when sides lead the counts."""
        self.assertEqual(
            parse("horns R 2 emb x 11, L 4 emb x 11,"),
            [
                Embryo(
                    length=11,
                    right=2,
                    left=4,
                    count=6,
                    start=6,
                    end=23,
                ),
            ],
        )

    def test_embryo_20(self) -> None:
        """It parses a numeric word count."""
        self.assertEqual(
            parse("FOUR EMBS, 25MM"),
            [Embryo(count=4, length=25, start=0, end=15)],
        )

    def test_embryo_21(self) -> None:
        """It parses a crown-rump length."""
        self.assertEqual(
            parse("crown-rump length=13 mm"),
            [Embryo(length=13, start=0, end=23, measured_from="crown")],
        )

    def test_embryo_22(self) -> None:
        """It handles no units."""
        self.assertEqual(
            parse("Embryo crown-rump length 22"),
            [
                Embryo(
                    length=22,
                    units_inferred=True,
                    start=0,
                    end=27,
                    measured_from="crown",
                )
            ],
        )

    def test_embryo_23(self) -> None:
        """It handles odd interstitial characters."""
        self.assertEqual(
            parse("3 embs/2L+2R/cr=X34mm"),
            [
                Embryo(
                    start=0,
                    end=21,
                    left=2,
                    right=2,
                    count=4,
                    length=34,
                    measured_from="crown",
                ),
            ],
        )

    def test_embryo_24(self) -> None:
        """It parses a length with a width."""
        self.assertEqual(
            parse(", cr=5x5 ;"),
            [
                Embryo(
                    length=5,
                    width=5,
                    units_inferred=True,
                    measured_from="crown",
                    start=2,
                    end=8,
                )
            ],
        )

    def test_embryo_25(self) -> None:
        """It parses a length with a width and units."""
        self.assertEqual(
            parse("; reproductive data=cr=9x8mm"),
            [Embryo(length=9, width=8, start=20, end=28, measured_from="crown")],
        )

    def test_embryo_28(self) -> None:
        """It picks up the presence of an embryo."""
        self.assertEqual(
            parse("Near-term fetus"),
            [Embryo(start=0, end=15, count=1)],
        )

    def test_embryo_29(self) -> None:
        """It gets a count with a presence term."""
        self.assertEqual(
            parse("6 near-term embryos."),
            [Embryo(start=0, end=19, count=6)],
        )

    def test_embryo_30(self) -> None:
        """It parses a mixed count/length string with both a length and a width."""
        self.assertEqual(
            parse("2 embryos side2 horn, 3 side1, ~9x10mm"),
            [
                Embryo(
                    length=9,
                    width=10,
                    count=5,
                    start=0,
                    end=38,
                )
            ],
        )

    def test_embryo_32(self) -> None:
        """It handles this key format."""
        self.assertEqual(
            parse("3 embryos L side, 1 R. Mammaries developing."),
            [Embryo(left=3, right=1, start=0, end=22, count=4)],
        )

    def test_embryo_33(self) -> None:
        """It handles am x as a side separator."""
        self.assertEqual(
            parse("Embryos: 5R x 4L c.r. 3 mm."),
            [
                Embryo(start=0, end=16, right=5, left=4, count=9),
                Embryo(start=17, end=27, length=3.0, measured_from="crown"),
            ],
        )

    def test_embryo_34(self) -> None:
        """It handles a single side."""
        self.assertEqual(
            parse("embs.=1R,!L"),
            [Embryo(right=1, start=0, end=8, count=1)],
        )

    def test_embryo_35(self) -> None:
        """It parses a length/width in the middle of the counts."""
        self.assertEqual(
            parse("1 embryo side2 horn 4x8mm, 1 embryo side1 horn"),
            [
                Embryo(
                    start=0,
                    end=41,
                    length=4.0,
                    width=8.0,
                    count=2,
                )
            ],
        )

    def test_embryo_36(self) -> None:
        """It parses a mixed notation with a leading key."""
        self.assertEqual(
            parse("embs=1R (CR=32 mm), 1L (CR=32&28mm) ;"),
            [
                Embryo(
                    start=0,
                    end=22,
                    length=32.0,
                    measured_from="crown",
                    right=1,
                    left=1,
                    count=2,
                ),
                Embryo(
                    start=24,
                    end=29,
                    length=32.0,
                    units_inferred=True,
                    measured_from="crown",
                ),
            ],
        )

    def test_embryo_37(self) -> None:
        """It handles a key merged with a cross."""
        self.assertEqual(
            parse("R horn 5embsx18mm, L horn 1 resorb embx5mm, 1embx18mm; "),
            [
                Embryo(
                    start=0,
                    end=27,
                    length=18.0,
                    measured_from="crown",
                    left=1,
                    right=5,
                    count=6,
                ),
            ],
        )

    def test_embryo_38(self) -> None:
        """It handles the side inside of parentheses."""
        self.assertEqual(
            parse("emb 5x21 (R2 L3),"),
            [
                Embryo(start=0, end=16, length=21, right=2, left=3, count=5),
            ],
        )

    def test_embryo_39(self) -> None:
        """It handles a few words inbetween the sides."""
        self.assertEqual(
            parse("emb 1x13( R), 1+ pl sc (L),"),
            [
                Embryo(start=0, end=26, length=13, right=1, left=1, count=2),
            ],
        )

    def test_embryo_40(self) -> None:
        """It handles the key after the length."""
        self.assertEqual(
            parse("reproductive data=3 large, 20mm embryos: 2R, 1L."),
            [
                Embryo(start=27, end=48, length=20, right=2, left=1, count=3),
            ],
        )

    def test_embryo_41(self) -> None:
        """It correctly parses numbers being next to each other."""
        self.assertEqual(
            parse("reproductive data=5 3mm embryos: 1R, 4L"),
            [
                Embryo(start=18, end=39, length=3, right=1, left=4, count=5),
            ],
        )

    def test_embryo_42(self) -> None:
        """It handles a missing total count."""
        self.assertEqual(
            parse("""L 1 emb x 3 mm and 1 emb 2.5 mm;"""),
            [
                Embryo(start=0, end=14, length=3, left=1, count=1),
                Embryo(start=19, end=31, length=2.5, count=1),
            ],
        )

    def test_embryo_43(self) -> None:
        """It parses an 'each side' notation."""
        self.assertEqual(
            parse("2 embryos each side (4 total), 3x4mm"),
            [
                Embryo(start=0, end=36, length=3, width=4, left=2, right=2, count=4),
            ],
        )

    def test_embryo_44(self) -> None:
        """It handles a key at the end of the notation."""
        self.assertEqual(
            parse("reproductive data=2Rx1Lx23 mm fetuses"),
            [
                Embryo(start=18, end=37, length=23, right=2, left=1, count=3),
            ],
        )

    def test_embryo_45(self) -> None:
        """It handles the sides being inside of parentheses."""
        self.maxDiff = None
        self.assertEqual(
            parse("Pregnant with 4 embryos (rt = 1, lt = 3;"),
            [
                PregnancyState(pregnancy=True, start=0, end=8),
                Embryo(
                    start=14,
                    end=39,
                    count=4,
                    right=1,
                    left=3,
                ),
            ],
        )

    def test_embryo_46(self) -> None:
        """It handles the key in the middle of the notation."""
        self.assertEqual(
            parse("RBS 4029; EMB-R 2, EMB-L 3, CR 8 mm"),
            [
                Embryo(
                    start=10,
                    end=35,
                    length=8,
                    right=2,
                    left=3,
                    count=5,
                    measured_from="crown",
                ),
            ],
        )

    def test_embryo_47(self) -> None:
        """It handles a lot of colons between the fields."""
        self.maxDiff = None
        self.assertEqual(
            parse("reproductive data=Emb = 4 : CR = 17mm : 2R x 2L"),
            [
                Embryo(
                    end=47,
                    length=17,
                    right=2,
                    left=2,
                    count=4,
                    start=18,
                    measured_from="crown",
                )
            ],
        )

    def test_embryo_48(self) -> None:
        """It allows parentheses around all values."""
        self.assertEqual(
            parse("Embryos (R2, L4, 10mm)."),
            [Embryo(length=10, end=22, right=2, left=4, start=0, count=6)],
        )

    def test_embryo_49(self) -> None:
        """It handles the length at index 3."""
        self.assertEqual(
            parse("4 embs: 2(R)&2(L)=9mm"),
            [Embryo(length=9.0, start=0, end=21, right=2, left=2, count=4)],
        )

    def test_embryo_50(self) -> None:
        """It parses an equation format."""
        self.assertEqual(
            parse("embryos 1 + 2 = 3 (29763, 29764) CR = 30 mm."),
            [
                Embryo(count=3, start=0, end=17),
                Embryo(start=33, end=44, length=30.0, measured_from="crown"),
            ],
        )

    def test_embryo_51(self) -> None:
        self.assertEqual(
            parse("Note in catalog: Lactating - 3 embryos"),
            [
                LactationState(
                    lactation=True,
                    description="Lactating",
                    start=17,
                    end=26,
                ),
                Embryo(start=29, end=38, count=3),
            ],
        )

    def test_embryo_52(self) -> None:
        self.maxDiff = None
        self.assertEqual(
            parse("6 embryos: 2/3 term"),
            [Embryo(start=0, end=9, count=6)],
        )

    def test_embryo_53(self) -> None:
        self.assertEqual(
            parse("no embryos"),
            [Embryo(start=0, end=10, count=0)],
        )

    def test_embryo_54(self) -> None:
        self.assertEqual(
            parse("One embryo. C-R: 32 mm"),
            [Embryo(start=0, end=22, length=32, measured_from="crown", count=1)],
        )
