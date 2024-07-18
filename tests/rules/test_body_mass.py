import unittest

from ranges.pylib.rules.body_mass import BodyMass
from ranges.pylib.rules.total_length import TotalLength
from tests.setup import parse


class TestBodyMass(unittest.TestCase):
    def test_body_mass_01(self):
        """It handles a total length before the mass."""
        self.assertEqual(
            parse("TL (mm) 44,Weight (g) 0.77 xx"),
            [
                TotalLength(length=44, start=0, end=10),
                BodyMass(mass=0.77, start=11, end=26),
            ],
        )

    def test_body_mass_02(self):
        """It handles a prefix key."""
        self.assertEqual(
            parse("body mass=20 g"),
            [BodyMass(mass=20, start=0, end=14)],
        )

    def test_body_mass_03(self):
        """It handles a compound value."""
        self.assertEqual(
            parse("Weight=22 lbs., 7 oz.;"),
            [
                BodyMass(
                    mass=10177.48,
                    start=0,
                    end=21,
                )
            ],
        )

    def test_body_mass_04(self):
        """It handles a compound value range."""
        self.assertEqual(
            parse("2 lbs. 3.1 - 4.5 oz "),
            [
                BodyMass(
                    mass=[995.06, 1034.75],
                    ambiguous=True,
                    start=0,
                    end=19,
                )
            ],
        )

    def test_body_mass_05(self):
        # It handles an estimated value.
        self.assertEqual(
            parse('"weight":"[139.5] g" }'),
            [
                BodyMass(
                    mass=139.5,
                    estimated=True,
                    start=1,
                    end=19,
                )
            ],
        )

    def test_body_mass_06(self):
        """It handles other units."""
        self.assertEqual(
            parse('"weight":"94 gr."'),
            [BodyMass(mass=94, start=1, end=16)],
        )

    def test_body_mass_07(self):
        """It handles no space between the mass and units."""
        self.assertEqual(
            parse('{"measurements":"20.2g,}'),
            [BodyMass(mass=20.2, ambiguous=True, start=14, end=22)],
        )

    def test_body_mass_08(self):
        """It handles a leader only key."""
        self.assertEqual(
            parse("Body: 15 g"),
            [BodyMass(mass=15, start=0, end=10)],
        )

    def test_body_mass_09(self):
        """It handles the units being in the key."""
        self.assertEqual(
            parse('{ "massingrams"="20.1" }'),
            [BodyMass(mass=20.1, start=3, end=21)],
        )

    def test_body_mass_10(self):
        """It handles commas in the mass."""
        self.assertEqual(
            parse('"weight":"1,192.0g" }'),
            [BodyMass(mass=1192, start=1, end=18)],
        )

    def test_body_mass_11(self):
        """It handles inferring the units."""
        self.assertEqual(
            parse('"weight":"1,192.0" }'),
            [BodyMass(mass=1192, units_inferred=True, start=1, end=17)],
        )

    def test_body_mass_12(self):
        """It parses a weight range."""
        self.assertEqual(
            parse('"weight: 20.5-31.8gms'),
            [BodyMass(mass=[20.5, 31.8], start=1, end=21)],
        )

    def test_body_mass_13(self):
        """It parses a weight range without units."""
        self.assertEqual(
            parse('"weight: 20.5-32'),
            [
                BodyMass(
                    mass=[20.5, 32],
                    units_inferred=True,
                    start=1,
                    end=16,
                )
            ],
        )

    def test_body_mass_14(self):
        """It handles other units."""
        self.assertEqual(
            parse("Body: 1.2 kg"),
            [BodyMass(mass=1200, start=0, end=12)],
        )

    def test_body_mass_15(self):
        """It should not parse_fields this."""
        self.assertEqual(parse("Specimen #'s - 5491,5492"), [])

    def test_body_mass_16(self):
        """It parses a zero mass."""
        self.assertEqual(
            parse("body mass=0 g"),
            [BodyMass(mass=0, start=0, end=13)],
        )

    def test_body_mass_17(self):
        """It parses a different key."""
        self.assertEqual(
            parse("wt=10 g"),
            [BodyMass(mass=10, start=0, end=7)],
        )

    def test_body_mass_18(self):
        """It parses a mass without a leading zero."""
        self.assertEqual(
            parse("weight=.65 kg;"),
            [BodyMass(mass=650, start=0, end=13)],
        )

    def test_body_mass_19(self):
        """It skips weights that are not a body mass."""
        self.assertEqual(parse("bacu wt=10 g"), [])

    def test_body_mass_20(self):
        self.assertEqual(
            parse("Verbatim weight=10;weight=10 g"),
            [
                BodyMass(start=9, end=18, mass=10.0, units_inferred=True),
                BodyMass(start=19, end=30, mass=10.0),
            ],
        )
