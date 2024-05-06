import unittest

from ranges.pylib.rules.placenta_scar_count import PlacentalScarCount
from tests.setup import parse


class TestPlacentalScarCount(unittest.TestCase):
    def test_placental_scar_count_01(self):
        self.assertEqual(
            parse("7 plac scar"),
            [PlacentalScarCount(count=7, present=True, start=0, end=11)],
        )

    def test_placental_scar_count_02(self):
        self.assertEqual(
            parse("5 plac scar 3L 2R"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=3, right=2, start=20, end=37
                )
            ],
        )

    def test_placental_scar_count_03(self):
        self.assertEqual(
            parse("3 placental scars, 1L, 2R"),
            [
                PlacentalScarCount(
                    present=True, count=3, left=1, right=2, start=0, end=25
                )
            ],
        )

    def test_placental_scar_count_04(self):
        self.assertEqual(
            parse("4 plac scar"),
            [PlacentalScarCount(present=True, count=4, start=0, end=11)],
        )

    def test_placental_scar_count_05(self):
        self.assertEqual(
            parse("no placental scars"),
            [PlacentalScarCount(present=False, count=0, start=0, end=18)],
        )

    def test_placental_scar_count_06(self):
        self.assertEqual(
            parse("2+1=3 placental scars"),
            [
                PlacentalScarCount(
                    present=True, count=3, side1=2, side2=1, start=0, end=21
                )
            ],
        )

    def test_placental_scar_count_07(self):
        self.assertEqual(
            parse("placental scar 1 + 2"),
            [
                PlacentalScarCount(
                    present=True, count=3, side1=1, side2=2, start=9, end=29
                )
            ],
        )

    def test_placental_scar_count_08(self):
        self.assertEqual(
            parse("uterus enlarged, scarring"),
            [PlacentalScarCount(present=True, start=17, end=25)],
        )

    def test_placental_scar_count_09(self):
        self.assertEqual(
            parse("uterine scars"),
            [PlacentalScarCount(present=True, start=4, end=26)],
        )

    def test_placental_scar_count_10(self):
        self.assertEqual(
            parse("plac scar 1L"),
            [PlacentalScarCount(present=True, count=1, left=1, start=0, end=12)],
        )

    def test_placental_scar_count_11(self):
        self.assertEqual(
            parse("; 4 faint placental scars"),
            [PlacentalScarCount(count=4, start=2, end=25)],
        )

    def test_placental_scar_count_12(self):
        self.assertEqual(
            parse("5 plac scars: 3(R)&2(L)"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=2, right=3, start=0, end=22
                )
            ],
        )

    def test_placental_scar_count_13(self):
        self.assertEqual(
            parse("2 placental scars, 0L, 2R"),
            [
                PlacentalScarCount(
                    present=True, count=2, left=0, right=2, start=0, end=25
                )
            ],
        )

    def test_placental_scar_count_14(self):
        self.assertEqual(
            parse("2+1=3 placental scars"),
            [
                PlacentalScarCount(
                    present=True, count=3, side1=2, side2=1, start=0, end=21
                )
            ],
        )

    def test_placental_scar_count_15(self):
        self.assertEqual(
            parse("not breeding, two scars, 1 left, 1 right"),
            [
                PlacentalScarCount(
                    present=True, count=2, left=1, right=1, start=18, end=40
                )
            ],
        )

    def test_placental_scar_count_16(self):
        self.assertEqual(
            parse("placental scars 1 + 1, mam tissue"),
            [
                PlacentalScarCount(
                    present=True, count=2, side1=1, side2=1, start=0, end=21
                )
            ],
        )

    def test_placental_scar_count_17(self):
        self.assertEqual(
            parse("2 P-SCAR R, 1 P-SCAR L"),
            [
                PlacentalScarCount(
                    present=True, count=3, left=1, right=2, start=0, end=22
                )
            ],
        )

    def test_placental_scar_count_18(self):
        self.assertEqual(
            parse("5 scars: 2lf,3rt"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=2, right=3, start=0, end=16
                )
            ],
        )

    def test_placental_scar_count_19(self):
        self.assertEqual(
            parse("P-SCAR-R 3, P-SCAR-L 2"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=2, right=3, start=11, end=33
                )
            ],
        )

    def test_placental_scar_count_20(self):
        self.assertEqual(
            parse("1R,0L plac scar"),
            [
                PlacentalScarCount(
                    present=True, count=1, left=0, right=1, start=0, end=15
                )
            ],
        )

    def test_placental_scar_count_21(self):
        self.assertEqual(
            parse("3 pac. scars:1(R)&2(L)"),
            [
                PlacentalScarCount(
                    present=True, count=3, left=2, right=1, start=0, end=21
                )
            ],
        )

    def test_placental_scar_count_22(self):
        self.assertEqual(
            parse("plac scar-9; lactating)"),
            [PlacentalScarCount(present=True, count=9, start=0, end=11)],
        )

    def test_placental_scar_count_23(self):
        self.assertEqual(
            parse("1 lt. plac. scar, 2 rt emb: CR: 16 mm"),
            [
                PlacentalScarCount(
                    present=True, count=3, left=1, right=2, start=0, end=22
                )
            ],
        )

    def test_placental_scar_count_24(self):
        self.assertEqual(
            parse("3+4= 7 placental scars"),
            [
                PlacentalScarCount(
                    present=True, count=7, side1=3, side2=4, start=0, end=22
                )
            ],
        )

    def test_placental_scar_count_25(self):
        self.assertEqual(
            parse("; no embroys or scar"),
            [PlacentalScarCount(present=False, count=0, start=2, end=20)],
        )

    def test_placental_scar_count_26(self):
        self.assertEqual(
            parse("; 3 prominent placental scars"),
            [PlacentalScarCount(present=True, count=3, start=2, end=29)],
        )

    def test_placental_scar_count_27(self):
        self.assertEqual(
            parse("reproductive data=no plsc ; "),
            [PlacentalScarCount(present=False, start=29, end=36)],
        )

    def test_placental_scar_count_28(self):
        self.assertEqual(
            parse("L 3 plac scars, R 2 pl. scars;"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=3, right=2, start=0, end=29
                )
            ],
        )

    def test_placental_scar_count_29(self):
        self.assertEqual(
            parse("reproductive data=3R, 2L, placental scars;"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=2, right=3, start=18, end=41
                )
            ],
        )

    def test_placental_scar_count_30(self):
        self.assertEqual(
            parse("reproductive data=Scars - 5 on left, 5 of right"),
            [
                PlacentalScarCount(
                    present=True, count=10, left=5, right=5, start=18, end=47
                )
            ],
        )

    def test_placental_scar_count_31(self):
        self.assertEqual(
            parse(";reproductive data=Placental scars-2R; Embryos-1L,"),
            [PlacentalScarCount(present=True, count=2, right=2, start=19, end=37)],
        )

    def test_placental_scar_count_32(self):
        self.assertEqual(
            parse("no visible placental scarring"),
            [PlacentalScarCount(present=False, count=0, start=0, end=29)],
        )

    def test_placental_scar_count_33(self):
        self.assertEqual(parse("; 1 scar on tail ;"), [])

    def test_placental_scar_count_34(self):
        self.assertEqual(
            parse(", no scars horns R 2 plac scars, L 3 plac scars,"),
            [
                PlacentalScarCount(
                    present=True, start=17, end=47, count=5, right=2, left=3
                ),
            ],
        )

    def test_placental_scar_count_35(self):
        self.assertEqual(
            parse("reproductive data=horns R+L1.5wide 2+plac. scars,"),
            [PlacentalScarCount(present=True, start=74, end=85)],
        )

    def test_placental_scar_count_36(self):
        self.assertEqual(
            parse("; reproductive data=scars  0R-4L ;"),
            [
                PlacentalScarCount(
                    present=True, count=4, left=4, right=0, start=33, end=45
                )
            ],
        )

    def test_placental_scar_count_37(self):
        self.assertEqual(
            parse(
                "SKULL CLEANED AT ILLINOIS STATE MUSEUM OCT 95; "
                "SCAR ABOVE TAIL, EVIDENCE OF PAST INSECT DAMAGE;"
            ),
            [],
        )

    def test_placental_scar_count_38(self):
        self.assertEqual(
            parse("ut horns: R 1 definite scar, L 2+ scars;"),
            [
                PlacentalScarCount(
                    present=True, count=3, left=2, right=1, start=10, end=39
                )
            ],
        )

    def test_placental_scar_count_39(self):
        self.assertEqual(
            parse("DINO 14431; placental scars"),
            [PlacentalScarCount(present=True, start=12, end=27)],
        )

    def test_placental_scar_count_40(self):
        self.assertEqual(
            parse('"Note in catalog: same as 135478";Scarritt ' 'Venezuelan Exped."'),
            [],
        )

    def test_placental_scar_count_41(self):
        self.assertEqual(
            parse("5 ut scars, 132-62-20-15=19"),
            [PlacentalScarCount(present=True, count=5, start=0, end=10)],
        )

    def test_placental_scar_count_42(self):
        self.assertEqual(
            parse("specimen number AJU 372; P-SCAR-R 5, P-SCAR-L 5"),
            [
                PlacentalScarCount(
                    present=True, count=10, left=5, right=5, start=25, end=47
                )
            ],
        )

    def test_placental_scar_count_43(self):
        self.assertEqual(
            parse("Zion 11396; NK 36683; scars"),
            [PlacentalScarCount(present=True, start=22, end=27)],
        )

    def test_placental_scar_count_44(self):
        self.assertEqual(
            parse(
                "negative for nematodes; skull labeled 14 Nov 57. PSM: "
                "Mamm Puget Sound Museum ID 27461"
            ),
            [],
        )

    def test_placental_scar_count_45(self):
        self.assertEqual(
            parse(
                "born in lab on Sept 3 to 7 '56; placed in sep. cage 28 "
                "Sept 56; skull labeled 23 Jan 57"
            ),
            [],
        )

    def test_placental_scar_count_46(self):
        self.assertEqual(
            parse("H,K,L,L,S; UTERINE SCARS=2R"),
            [PlacentalScarCount(present=True, count=2, right=2, start=11, end=27)],
        )

    def test_placental_scar_count_47(self):
        self.assertEqual(
            parse("no embryonic scars 360-40-125-68 1800g"),
            [PlacentalScarCount(present=False, count=0, start=0, end=18)],
        )

    def test_placental_scar_count_48(self):
        self.assertEqual(
            parse("scars"),
            [PlacentalScarCount(present=True, start=0, end=5)],
        )

    def test_placental_scar_count_49(self):
        self.assertEqual(
            parse("fat=2; lactating; 14 embryo scars"),
            [PlacentalScarCount(present=True, count=14, start=18, end=33)],
        )

    def test_placental_scar_count_50(self):
        self.assertEqual(
            parse("3 scars left, 3 right; lactating."),
            [
                PlacentalScarCount(
                    present=True, count=6, left=3, right=3, start=0, end=21
                )
            ],
        )

    def test_placental_scar_count_51(self):
        self.assertEqual(
            parse("Uterine scars: 1 L, 3 R."),
            [
                PlacentalScarCount(
                    present=True, count=4, left=1, right=3, start=0, end=23
                )
            ],
        )

    def test_placental_scar_count_52(self):
        self.assertEqual(
            parse("scars: 2R, 2L"),
            [
                PlacentalScarCount(
                    present=True, count=4, left=2, right=2, start=0, end=13
                )
            ],
        )

    def test_placental_scar_count_53(self):
        self.assertEqual(
            parse("scars 3L, 3R"),
            [
                PlacentalScarCount(
                    present=True, count=6, left=3, right=3, start=15, end=27
                )
            ],
        )

    def test_placental_scar_count_55(self):
        self.assertEqual(
            parse("scars 2R, 3L,"),
            [
                PlacentalScarCount(
                    present=True, count=5, left=3, right=2, start=12, end=24
                )
            ],
        )
