import unittest

from ranges.rules.testicle import Testicle
from tests.setup import parse


class TestTesticleSize(unittest.TestCase):
    def test_testicle_length_01(self) -> None:
        self.assertEqual(
            parse("testes = 8x5 mm"),
            [Testicle(length1=8, width1=5, start=0, end=15)],
        )

    def test_testicle_length_02(self) -> None:
        self.assertEqual(
            parse("testes: 20mm. Sent to Berkeley 10/1/71"),
            [Testicle(length1=20, start=0, end=13)],
        )

    def test_testicle_length_03(self) -> None:
        self.assertEqual(
            parse("reproductive data=testis 5mm ; "),
            [Testicle(length1=5, start=18, end=28)],
        )

    def test_testicle_length_04(self) -> None:
        self.assertEqual(
            parse("reproductive data=NS; T=9x4 ; endoparasite "),
            [
                Testicle(
                    position="non-scrotal",
                    length1=9,
                    width1=4,
                    units_inferred=True,
                    start=18,
                    end=27,
                )
            ],
        )

    def test_testicle_length_05(self) -> None:
        self.assertEqual(
            parse("reproductive data=testes: 18x8 mm; scrotal ;"),
            [Testicle(length1=18, width1=8, position="scrotal", start=18, end=42)],
        )

    def test_testicle_length_06(self) -> None:
        self.assertEqual(
            parse("Plus Tissue; plus Baculum: Test 21x11"),
            [Testicle(length1=21, width1=11, units_inferred=True, start=27, end=37)],
        )

    def test_testicle_length_07(self) -> None:
        self.assertEqual(
            parse("; reproductive data=testes scrotal; T = 9mm in length"),
            [Testicle(length1=9, position="scrotal", start=20, end=43)],
        )

    def test_testicle_length_08(self) -> None:
        self.assertEqual(
            parse("Scrotal 9 mm x 5 mm"),
            [
                Testicle(
                    length1=9,
                    width1=5,
                    position="scrotal",
                    start=0,
                    end=19,
                )
            ],
        )

    def test_testicle_length_09(self) -> None:
        self.assertEqual(
            parse("reproductive data=testes abdominal; T = 3 x 1.8 ;"),
            [
                Testicle(
                    length1=3,
                    width1=1.8,
                    position="abdominal",
                    units_inferred=True,
                    start=18,
                    end=47,
                )
            ],
        )

    def test_testicle_length_10(self) -> None:
        self.assertEqual(
            parse("testis-20mm ; reproductive data=testis-21mm ; "),
            [
                Testicle(length1=20, start=0, end=11),
                Testicle(length1=21, start=32, end=43),
            ],
        )

    def test_testicle_length_11(self) -> None:
        self.assertEqual(
            parse("Testes x6"),
            [Testicle(length1=6, units_inferred=True, start=0, end=9)],
        )

    def test_testicle_length_12(self) -> None:
        self.assertEqual(
            parse("testes scrotal, L testis 13x5mm"),
            [
                Testicle(position="scrotal", start=0, end=14),
                Testicle(length1=13, width1=5, start=18, end=31),
            ],
        )

    def test_testicle_length_17(self) -> None:
        self.assertEqual(
            parse("testis-7mm"),
            [Testicle(length1=7, start=0, end=10)],
        )

    def test_testicle_length_18(self) -> None:
        self.assertEqual(
            parse("reproductive data=T=10x4 ; "),
            [Testicle(length1=10, width1=4, units_inferred=True, start=18, end=24)],
        )

    def test_testicle_length_20(self) -> None:
        self.assertEqual(
            parse("; T=9x4 ; endoparasite "),
            [
                Testicle(
                    length1=9.0,
                    width1=4.0,
                    units_inferred=True,
                    start=2,
                    end=7,
                )
            ],
        )

    def test_testicle_length_21(self) -> None:
        self.assertEqual(
            parse("; T=9 ; endoparasite "),
            [
                Testicle(
                    length1=9,
                    units_inferred=True,
                    start=2,
                    end=5,
                )
            ],
        )

    def test_testicle_length_22(self) -> None:
        self.assertEqual(
            parse("TESTES 5-3.5 MM,"),
            [Testicle(length1=5, width1=3.5, start=0, end=15)],
        )

    def test_testicle_length_23(self) -> None:
        self.assertEqual(
            parse("reproductive data=T: R-2x4mm ; "),
            [
                Testicle(
                    length1=2,
                    width1=4,
                    start=18,
                    end=28,
                )
            ],
        )

    def test_testicle_length_24(self) -> None:
        self.assertEqual(
            parse("reproductive data=T: L-2x4mm ; "),
            [
                Testicle(
                    length1=2,
                    width1=4,
                    start=18,
                    end=28,
                )
            ],
        )

    def test_testicle_length_25(self) -> None:
        self.assertEqual(
            parse("testes (R) 6 x 1.5 & 5 x 2 mm"),
            [
                Testicle(
                    length1=6.0,
                    width1=1.5,
                    length2=5.0,
                    width2=2.0,
                    start=0,
                    end=29,
                ),
            ],
        )

    def test_testicle_length_27(self) -> None:
        self.assertEqual(
            parse("; reproductive data=5x3 inguinal ;"),
            [],
        )

    def test_testicle_length_28(self) -> None:
        self.assertEqual(
            parse("; reproductive data=Testes .5' , scrotal"),
            [
                Testicle(
                    position="scrotal",
                    length1=0.5,
                    units_inferred=True,
                    start=20,
                    end=40,
                )
            ],
        )

    def test_testicle_length_29(self) -> None:
        self.assertEqual(
            parse("; reproductive data=TESTES NOT DESCENDED - 6 MM age"),
            [Testicle(position="not descended", length1=6, start=20, end=47)],
        )

    def test_testicle_length_31(self) -> None:
        self.assertEqual(
            parse("reproductive data=Right testicle: 20x9 mm ;"),
            [
                Testicle(
                    length1=20.0,
                    width1=9.0,
                    start=24,
                    end=41,
                )
            ],
        )

    def test_testicle_length_32(self) -> None:
        self.assertEqual(
            parse("; reproductive data=Testes scrotal, 32x11"),
            [
                Testicle(
                    length1=32,
                    position="scrotal",
                    width1=11,
                    units_inferred=True,
                    start=20,
                    end=41,
                )
            ],
        )

    def test_testicle_length_33(self) -> None:
        self.assertEqual(
            parse("; reproductive data=test R 20mm L x 6 mm ;"),
            [Testicle(length1=20, length2=6, start=20, end=40)],
        )

    def test_testicle_length_34(self) -> None:
        self.assertEqual(
            parse("; reproductive data=T R 20mm L 6 mm ;"),
            [Testicle(length1=20, length2=6, start=20, end=35)],
        )

    def test_testicle_length_35(self) -> None:
        self.assertEqual(parse("; reproductive data=t=233mg ;"), [])

    def test_testicle_length_36(self) -> None:
        self.assertEqual(
            parse("test ing. 4mm"),
            [
                Testicle(
                    length1=4.0,
                    start=0,
                    end=13,
                    position="inguinal",
                )
            ],
        )
