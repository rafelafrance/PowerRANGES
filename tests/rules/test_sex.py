import unittest

from ranges.pylib.rules.sex import Sex
from tests.setup import parse


class TestSex(unittest.TestCase):
    def test_sex_01(self):
        self.assertEqual(
            parse("sex=female ?"), [Sex(trait="sex", sex="female?", start=0, end=12)]
        )

    def test_sex_02(self):
        self.assertEqual(
            parse("sex=unknown ;"),
            [Sex(trait="sex", sex="unknown", start=0, end=11)],
        )

    def test_sex_03(self):
        self.assertEqual(
            parse("sex=F "),
            [Sex(trait="sex", sex="female", start=0, end=5)],
        )

    def test_sex_04(self):
        self.assertEqual(
            parse("words male female unknown more words"),
            [
                Sex(trait="sex", sex="male", start=6, end=10),
                Sex(trait="sex", sex="female", start=11, end=17),
            ],
        )

    def test_sex_05(self):
        self.assertEqual(
            parse("words male female male more words"),
            [
                Sex(trait="sex", sex="male", start=6, end=10),
                Sex(trait="sex", sex="female", start=11, end=17),
                Sex(trait="sex", sex="male", start=18, end=22),
            ],
        )

    def test_sex_06(self):
        self.assertEqual(parse("Respective sex and msmt. in mm"), [])

    def test_sex_07(self):
        self.assertEqual(
            parse("male or female"),
            [
                Sex(trait="sex", sex="male", start=0, end=4),
                Sex(trait="sex", sex="female", start=8, end=14),
            ],
        )

    def test_sex_08(self):
        self.assertEqual(
            parse("sex=unknown "),
            [Sex(trait="sex", sex="unknown", start=0, end=11)],
        )

    def test_sex_09(self):
        self.assertEqual(
            parse("sex=female?"), [Sex(trait="sex", sex="female?", start=0, end=11)]
        )

    def test_sex_10(self):
        self.assertEqual(
            parse("sex=not recorded ;"),
            [Sex(trait="sex", sex="unknown", start=0, end=16)],
        )

    def test_sex_11(self):
        self.assertEqual(
            parse("sex=male ; sex=male ;"),
            [
                Sex(trait="sex", sex="male", start=0, end=8),
                Sex(trait="sex", sex="male", start=11, end=19),
            ],
        )
