import unittest

from ranges.rules.sex import Sex
from tests.setup import parse


class TestSex(unittest.TestCase):
    def test_sex_01(self) -> None:
        self.assertEqual(parse("sex=female ?"), [Sex(sex="female?", start=0, end=12)])

    def test_sex_02(self) -> None:
        self.assertEqual(
            parse("sex=unknown ;"),
            [Sex(sex="unknown", start=0, end=11)],
        )

    def test_sex_03(self) -> None:
        self.assertEqual(
            parse("sex=F "),
            [Sex(sex="female", start=0, end=5)],
        )

    def test_sex_04(self) -> None:
        self.assertEqual(
            parse("words male female unknown more words"),
            [
                Sex(sex="male", start=6, end=10),
                Sex(sex="female", start=11, end=17),
            ],
        )

    def test_sex_05(self) -> None:
        self.assertEqual(
            parse("words male female male more words"),
            [
                Sex(sex="male", start=6, end=10),
                Sex(sex="female", start=11, end=17),
                Sex(sex="male", start=18, end=22),
            ],
        )

    def test_sex_06(self) -> None:
        self.assertEqual(parse("Respective sex and msmt. in mm"), [])

    def test_sex_07(self) -> None:
        self.assertEqual(
            parse("male or female"),
            [
                Sex(sex="male", start=0, end=4),
                Sex(sex="female", start=8, end=14),
            ],
        )

    def test_sex_08(self) -> None:
        self.assertEqual(
            parse("sex=unknown "),
            [Sex(sex="unknown", start=0, end=11)],
        )

    def test_sex_09(self) -> None:
        self.assertEqual(parse("sex=female?"), [Sex(sex="female?", start=0, end=11)])

    def test_sex_10(self) -> None:
        self.assertEqual(
            parse("sex=not recorded ;"),
            [Sex(sex="unknown", start=0, end=16)],
        )

    def test_sex_11(self) -> None:
        self.assertEqual(
            parse("sex=male ; sex=male ;"),
            [
                Sex(sex="male", start=0, end=8),
                Sex(sex="male", start=11, end=19),
            ],
        )
