import unittest

from ranges.pylib.rules.testicle import Testicle
from tests.setup import parse


class TestTesticleState(unittest.TestCase):
    def test_testicle_description_01(self):
        self.assertEqual(
            parse("some words reproductive data=No testicles; more words"),
            [Testicle(description="no testicles", start=29, end=41)],
        )

    def test_testicle_description_02(self):
        self.assertEqual(
            parse("testes descended"),
            [Testicle(description="descended", start=0, end=16)],
        )

    def test_testicle_description_03(self):
        self.assertEqual(
            parse("testes undescended"),
            [Testicle(description="undescended", start=0, end=18)],
        )

    def test_testicle_description_04(self):
        self.assertEqual(
            parse("testes undesc."),
            [Testicle(description="undescended", start=0, end=13)],
        )

    def test_testicle_description_06(self):
        self.assertEqual(
            parse("testes not fully descended"),
            [Testicle(description="not fully descended", start=0, end=26)],
        )

    def test_testicle_description_07(self):
        self.assertEqual(
            parse("tes undescend."),
            [Testicle(description="undescended", start=0, end=13)],
        )

    def test_testicle_description_08(self):
        self.assertEqual(
            parse("t abdominal"),
            [Testicle(description="abdominal", start=0, end=11)],
        )

    def test_testicle_description_09(self):
        self.assertEqual(
            parse("reproductive data=Testicle partially descended. "),
            [Testicle(description="partially descended", start=18, end=46)],
        )

    def test_testicle_description_10(self):
        self.assertEqual(
            parse("reproductive data=testis 5mm, abdominal "),
            [Testicle(description="abdominal", length=5, start=18, end=39)],
        )

    def test_testicle_description_12(self):
        self.assertEqual(
            parse("reproductive data=No testicles"),
            [Testicle(description="no testicles", start=18, end=30)],
        )

    def test_testicle_description_13(self):
        self.assertEqual(
            parse("reproductive data=testes decended, T=8x3 ;"),
            [
                Testicle(
                    description="descended",
                    length=8,
                    width=3,
                    units_inferred=True,
                    start=18,
                    end=40,
                )
            ],
        )

    def test_testicle_description_14(self):
        self.assertEqual(
            parse("reproductive data=Testicle small"),
            [Testicle(description="small", start=18, end=32)],
        )

    def test_testicle_description_16(self):
        self.assertEqual(parse("puncture wound in left abdominal region."), [])

    def test_testicle_description_18(self):
        self.assertEqual(
            parse("junk before reproductive data=Testicle small, not descended"),
            [Testicle(description="small, not descended", start=30, end=59)],
        )

    def test_testicle_description_19(self):
        self.assertEqual(
            parse("Mixed woods // TESTES NOT DESCENDED"),
            [Testicle(description="not descended", start=15, end=35)],
        )

    def test_testicle_description_20(self):
        self.assertEqual(parse("reproductive data=Uteri small, clear"), [])

    def test_testicle_description_21(self):
        self.assertEqual(
            parse("; reproductive data=testes = 4x3 mm; "),
            [Testicle(length=4, width=3, start=20, end=35)],
        )

    def test_testicle_description_22(self):
        self.assertEqual(
            parse("Deciduous woods // TESTES DESCENDED, AND ENLARGED"),
            [Testicle(description="descended enlarged", start=19, end=49)],
        )

    def test_testicle_description_23(self):
        self.assertEqual(
            parse("Testis abd. Collected with 22 cal. pellet rifle."),
            [Testicle(description="abdominal", start=0, end=10)],
        )

    def test_testicle_description_24(self):
        self.assertEqual(
            parse("reproductive data=test 3.5x2, pt desc, Et not visib,"),
            [
                Testicle(
                    description="pt desc",
                    length=3.5,
                    width=2,
                    units_inferred=True,
                    start=18,
                    end=37,
                )
            ],
        )

    def test_scrotal_state_25(self):
        self.assertEqual(
            parse("testes not-scrotal"),
            [Testicle(description="not-scrotal", start=0, end=18)],
        )

    def test_scrotal_state_26(self):
        self.assertEqual(
            parse("testes no scrotum"),
            [Testicle(description="no scrotum", start=0, end=17)],
        )

    def test_scrotal_state_27(self):
        self.assertEqual(
            parse("testis nscr"),
            [Testicle(description="non-scrotal", start=0, end=11)],
        )

    def test_scrotal_state_29(self):
        self.assertEqual(
            parse("testes ns"), [Testicle(description="non-scrotal", start=0, end=9)]
        )

    def test_scrotal_state_30(self):
        self.assertEqual(
            parse("t nscr"), [Testicle(description="non-scrotal", start=0, end=6)]
        )

    def test_scrotal_state_31(self):
        self.assertEqual(
            parse("reproductive data=testes: 11x7 mm (scrotal)"),
            [Testicle(description="scrotal", length=11, width=7, start=18, end=42)],
        )

    def test_scrotal_state_32(self):
        self.assertEqual(
            parse("non-scrotal, "),
            [Testicle(description="non-scrotal", start=0, end=11)],
        )

    def test_scrotal_state_33(self):
        self.assertEqual(
            parse("reproductive data=NS ;"),
            [Testicle(description="non-scrotal", start=18, end=20)],
        )

    def test_scrotal_state_34(self):
        self.assertEqual(
            parse("reproductive data=SCR ;"),
            [Testicle(description="scrotal", start=18, end=21)],
        )

    def test_scrotal_state_35(self):
        self.assertEqual(
            parse("t ns"), [Testicle(description="non-scrotal", start=0, end=4)]
        )
