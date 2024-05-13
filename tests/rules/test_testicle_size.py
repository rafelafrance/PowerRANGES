import unittest

from ranges.pylib.rules.testicle import Testicle
from tests.setup import parse


class TestTesticleSize(unittest.TestCase):
    def test_testicle_length_01(self):
        self.assertEqual(
            parse("testes = 8x5 mm"),
            [Testicle(length=8, width=5, start=0, end=15)],
        )

    def test_testicle_length_02(self):
        self.assertEqual(
            parse("testes: 20mm. Sent to Berkeley 10/1/71"),
            [Testicle(length=20, start=0, end=13)],
        )

    def test_testicle_length_03(self):
        self.assertEqual(
            parse("reproductive data=testis 5mm ; "),
            [Testicle(length=5, start=18, end=28)],
        )

    def test_testicle_length_04(self):
        self.assertEqual(
            parse("reproductive data=NS; T=9x4 ; endoparasite "),
            [
                Testicle(
                    description="ns",
                    length=9,
                    width=4,
                    units_inferred=True,
                    start=18,
                    end=27,
                )
            ],
        )

    def test_testicle_length_05(self):
        self.assertEqual(
            parse("reproductive data=testes: 18x8 mm; scrotal ;"),
            [Testicle(length=18, width=8, description="scrotal", start=18, end=42)],
        )

    def test_testicle_length_06(self):
        self.assertEqual(
            parse("Plus Tissue; plus Baculum: Test 21x11"),
            [Testicle(length=21, width=11, units_inferred=True, start=27, end=37)],
        )

    def test_testicle_length_07(self):
        self.assertEqual(
            parse("; reproductive data=testes scrotal; T = 9mm in length"),
            [Testicle(length=9, description="scrotal", start=20, end=43)],
        )

    def test_testicle_length_08(self):
        self.assertEqual(
            parse("Scrotal 9 mm x 5 mm"),
            [
                Testicle(
                    length=9,
                    width=5,
                    description="scrotal",
                    start=0,
                    end=19,
                )
            ],
        )

    def test_testicle_length_09(self):
        self.assertEqual(
            parse("reproductive data=testes abdominal; T = 3 x 1.8 ;"),
            [
                Testicle(
                    length=3,
                    width=1.8,
                    description="abdominal",
                    units_inferred=True,
                    start=18,
                    end=47,
                )
            ],
        )

    def test_testicle_length_10(self):
        self.assertEqual(
            parse("testis-20mm ; reproductive data=testis-21mm ; "),
            [
                Testicle(length=20, start=0, end=11),
                Testicle(length=21, start=32, end=43),
            ],
        )

    def test_testicle_length_11(self):
        self.assertEqual(
            parse("Testes x6"),
            [Testicle(length=6, units_inferred=True, start=0, end=9)],
        )

    def test_testicle_length_12(self):
        self.assertEqual(
            parse("testes scrotal, L testis 13x5mm"),
            [
                Testicle(description="scrotal", start=0, end=14),
                Testicle(length=13, width=5, start=18, end=31),
            ],
        )

    def test_testicle_length_17(self):
        self.assertEqual(
            parse("testis-7mm"),
            [Testicle(length=7, start=0, end=10)],
        )

    def test_testicle_length_18(self):
        self.assertEqual(
            parse("reproductive data=T=10x4 ; "),
            [Testicle(length=10, width=4, units_inferred=True, start=18, end=24)],
        )

    # def test_testicle_length_20(self):
    #     self.assertEqual(
    #         parse("adult ; T=9x4 ; endoparasite "),
    #         [
    #             Testicle(
    #                 length=9.0,
    #                 width=4.0,
    #                 units_inferred=True,
    #                 start=8,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_21(self):
    #     self.assertEqual(
    #         parse("adult ; T=9 ; endoparasite "),
    #         [
    #             Testicle(
    #                 length=9,
    #                 units_inferred=True,
    #                 start=8,
    #                 end=11,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_22(self):
    #     self.assertEqual(
    #         parse("TESTES 5-3.5 MM,"),
    #         [Testicle(length=5, width=3.5, start=0, end=15)],
    #     )
    #
    # def test_testicle_length_23(self):
    #     self.assertEqual(
    #         parse("reproductive data=T: R-2x4mm ; "),
    #         [
    #             Testicle(
    #                 length=2,
    #                 width=4,
    #                 start=0,
    #                 end=28,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_24(self):
    #     self.assertEqual(
    #         parse("reproductive data=T: L-2x4mm ; "),
    #         [
    #             Testicle(
    #                 length=2,
    #                 width=4,
    #                 start=0,
    #                 end=28,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_25(self):
    #     self.assertEqual(
    #         parse("testes (R) 6 x 1.5 & 5 x 2 mm"),
    #         [
    #             Testicle(
    #                 length=6.0,
    #                 width=1.5,
    #                 start=0,
    #                 end=29,
    #             ),
    #             Testicle(
    #                 length=5.0,
    #                 width=2.0,
    #                 start=0,
    #                 end=29,
    #             ),
    #         ],
    #     )
    #
    # def test_testicle_length_26(self):
    #     self.assertEqual(parse("Cataloged by: R.L. Humphrey, 31 January 1995"), [])
    #
    # def test_testicle_length_27(self):
    #     self.assertEqual(
    #         parse("; reproductive data=5x3 inguinal ;"),
    #         [Testicle(length=5, width=3, units_inferred=True, start=2, end=23)],
    #     )
    #
    # def test_testicle_length_28(self):
    #     self.assertEqual(
    #         parse("sex=male ; reproductive data=Testes .5' , scrotal"),
    #         [Testicle(length=152.4, start=11, end=39)],
    #     )
    #
    # def test_testicle_length_29(self):
    #     self.assertEqual(
    #         parse("; reproductive data=TESTES NOT DESCENDED - 6 MM age"),
    #         [Testicle(length=6, start=2, end=47)],
    #     )
    #
    # def test_testicle_length_31(self):
    #     self.assertEqual(
    #         parse("reproductive data=Right testicle: 20x9 mm ;"),
    #         [
    #             Testicle(
    #                 length=20.0,
    #                 width=9.0,
    #                 start=0,
    #                 end=41,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_32(self):
    #     self.assertEqual(
    #         parse("; reproductive data=Testes scrotal, 32x11"),
    #         [Testicle(length=32, width=11, units_inferred=True, start=2, end=41)],
    #     )
    #
    # def test_testicle_length_33(self):
    #     self.assertEqual(
    #         parse("; reproductive data=R 20mm L x 6 mm Wne scars ;"),
    #         [
    #             Testicle(
    #                 length=20,
    #                 start=2,
    #                 end=26,
    #             )
    #         ],
    #     )
    #
    # def test_testicle_length_34(self):
    #     self.assertEqual(
    #         parse("; reproductive data=R 20mm L 6 mm ;"),
    #         [
    #             Testicle(
    #                 length=20,
    #                 start=2,
    #                 end=33,
    #             ),
    #             Testicle(length=6, start=2, end=33),
    #         ],
    #     )
    #
    # def test_testicle_length_37(self):
    #     self.assertEqual(parse("; reproductive data=t=233mg ;"), [])
