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
            [Testicle(description="undesc", start=0, end=13)],
        )

    # def test_testicle_description_06(self):
    #     self.assertEqual(
    #         parse("testes not fully descended"),
    #         [Testicle(description="testes not fully descended", start=0, end=26)],
    #     )
    #
    # def test_testicle_description_07(self):
    #     self.assertEqual(
    #         parse("tes undescend."),
    #         [Testicle(description="tes undescend", start=0, end=13)],
    #     )
    #
    # def test_testicle_description_08(self):
    #     self.assertEqual(
    #         parse("t abdominal"),
    #         [Testicle(description="t abdominal", start=0, end=11)],
    #     )
    #
    # def test_testicle_description_09(self):
    #     self.assertEqual(
    #         parse(
    #             "hind foot with claw=35 mm; "
    #             "reproductive data=Testicle partially descended. "
    #             "Sperm present."
    #         ),
    #         [Testicle(description="testes partially descended", start=45, end=71)],
    #     )
    #
    # def test_testicle_description_10(self):
    #     self.assertEqual(
    #         parse(
    #             "sex=male ; reproductive data=testis 5mm, abdominal "
    #             "; ear from notch=20 mm; "
    #         ),
    #         [Testicle(description="testis 5mm, abdominal", start=29, end=50)],
    #     )
    #
    # def test_testicle_description_12(self):
    #     self.assertEqual(
    #         parse(
    #             "verbatim preservation date=8 October 1986 ; "
    #             "reproductive data=No testicles"
    #         ),
    #         [Testicle(description="no testicles", start=62, end=74)],
    #     )
    #
    # def test_testicle_description_13(self):
    #     self.assertEqual(
    #         parse(
    #             "weight=53 g; reproductive data=testes decended, T=8x3 ;"
    #         ),
    #         [Testicle(description="testes decended", start=31, end=46)],
    #     )
    #
    # def test_testicle_description_14(self):
    #     self.assertEqual(
    #         parse("weight=75.6 g; reproductive data=Testicle small"),
    #         [Testicle(description="testes small", start=15, end=45)],
    #     )
    #
    # def test_testicle_description_15(self):
    #     self.assertEqual(
    #         parse("weight=75.6 g; reproductive data=small"),
    #         [Testicle(description="small", start=15, end=38)],
    #     )
    #
    # def test_testicle_description_16(self):
    #     self.assertEqual(
    #         parse("puncture wound in left abdominal region."), []
    #     )
    #
    # def test_testicle_description_17(self):
    #     self.assertEqual(parse(" reproductive data=plsc"), [])
    #
    # def test_testicle_description_18(self):
    #     self.assertEqual(
    #         parse(
    #             "junk before reproductive data=Testicle small, not descended"
    #         ),
    #         [Testicle(description="testes small, not descended", start=12, end=57)],
    #     )
    #
    # def test_testicle_description_19(self):
    #     self.assertEqual(
    #         parse("Mixed woods // TESTES NOT DESCENDED"),
    #         [Testicle(description="testes not descended", start=15, end=35)],
    #     )
    #
    # def test_testicle_description_20(self):
    #     self.assertEqual(parse("reproductive data=Uteri small, clear"), [])
    #
    # def test_testicle_description_21(self):
    #     self.assertEqual(
    #         parse("; reproductive data=testes = 4x3 mm; "), []
    #     )
    #
    # def test_testicle_description_22(self):
    #     self.assertEqual(
    #         parse("Deciduous woods // TESTES DESCENDED, AND ENLARGED"),
    #        [Testicle(description="testes descended, and enlarged", start=19, end=49)],
    #     )
    #
    # def test_testicle_description_23(self):
    #     self.assertEqual(
    #         parse("Testis abd. Collected with 22 cal. pellet rifle."),
    #         [Testicle(description="testis abd", start=0, end=10)],
    #     )
    #
    # def test_testicle_description_24(self):
    #     self.assertEqual(
    #         parse("reproductive data=test 3.5x2, pt desc, Et not visib,"),
    #         [Testicle(description="test 3.5x2, pt desc", start=18, end=37)],
    #     )
    #
    # def test_scrotal_state_01(self):
    #     self.assertEqual(
    #         parse("testes not-scrotal"),
    #         [Testicle(description="testes not-scrotal", start=0, end=18)],
    #     )
    #
    # def test_scrotal_state_02(self):
    #     self.assertEqual(
    #         parse("testes no scrotum"),
    #         [Testicle(description="testes no scrotum", start=0, end=17)],
    #     )
    #
    # def test_scrotal_state_03(self):
    #     self.assertEqual(
    #         parse("testis nscr"),
    #         [Testicle(description="testis nscr", start=0, end=11)],
    #     )
    #
    # def test_scrotal_state_04(self):
    #     self.assertEqual(
    #         parse("testes ns"), [Testicle(description="testes ns", start=0, end=9)]
    #     )
    #
    # def test_scrotal_state_05(self):
    #     self.assertEqual(parse("t nscr"),
    #     [Testicle(description="t nscr", start=0, end=6)])
    #
    # def test_scrotal_state_06(self):
    #     self.assertEqual(parse("t ns"),
    #     [{"end": 4, "start": 0, "description": "t ns"}])
    #
    # def test_scrotal_state_07(self):
    #     self.assertEqual(
    #         parse("reproductive data=testes: 11x7 mm (scrotal)"),
    #         [Testicle(description="scrotal", start=48, end=55)],
    #     )
    #
    # def test_scrotal_state_08(self):
    #     self.assertEqual(
    #         parse("non-scrotal, sem. ves. 14 mm "),
    #         [Testicle(description="non-scrotal", start=0, end=11)],
    #     )
    #
    # def test_scrotal_state_09(self):
    #     self.assertEqual(
    #         parse("reproductive data=NS ;"),
    #         [Testicle(description="ns", start=0, end=20)],
    #     )
    #
    # def test_scrotal_state_10(self):
    #     self.assertEqual(
    #         parse("reproductive data=SCR ;"),
    #         [Testicle(description="scr", start=18, end=21)],
    #     )
