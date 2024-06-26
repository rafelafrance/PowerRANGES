import unittest

from ranges.pylib.rules.length_shorthand import LengthShorthand
from tests.setup import parse


class TestLengthShorthand(unittest.TestCase):
    def test_length_shorthand_01(self):
        """It handles a space between the length and mass measurements."""
        self.assertEqual(
            parse("762-292-121-76 2435.0g"),
            [
                LengthShorthand(
                    total_length=762,
                    tail_length=292,
                    hind_foot_length=121,
                    ear_length=76,
                    body_mass=2435,
                    start=0,
                    end=22,
                )
            ],
        )

    def test_length_shorthand_02(self):
        """It handles a forearm length."""
        self.assertEqual(
            parse("Note in catalog: 83-0-17-23-fa64-35g"),
            [
                LengthShorthand(
                    total_length=83,
                    tail_length=0,
                    hind_foot_length=17,
                    ear_length=23,
                    forearm_length=64,
                    body_mass=35,
                    start=17,
                    end=36,
                )
            ],
        )

    def test_length_shorthand_03(self):
        """It handles a forearm and tragus length."""
        self.assertEqual(
            parse("82-00-15-21-tr7-fa63-41g"),
            [
                LengthShorthand(
                    total_length=82,
                    tail_length=0,
                    hind_foot_length=15,
                    ear_length=21,
                    tragus_length=7,
                    forearm_length=63,
                    body_mass=41,
                    start=0,
                    end=24,
                )
            ],
        )

    def test_length_shorthand_04(self):
        # It handles the equals sign "=" separator
        self.assertEqual(
            parse("unformatted measurements=77-30-7-12=5.4"),
            [
                LengthShorthand(
                    total_length=77,
                    tail_length=30,
                    hind_foot_length=7,
                    ear_length=12,
                    body_mass=5.4,
                    start=25,
                    end=39,
                ),
            ],
        )

    def test_length_shorthand_05(self):
        """It handles field labels after the numbers."""
        self.assertEqual(
            parse("""{"measurements":"78-39-5-14-8(TR)-30(FA)" }"""),
            [
                LengthShorthand(
                    total_length=78,
                    tail_length=39,
                    hind_foot_length=5,
                    ear_length=14,
                    tragus_length=8,
                    forearm_length=30,
                    start=17,
                    end=40,
                ),
            ],
        )

    def test_length_shorthand_06(self):
        """It handles field labels without parentheses."""
        self.assertEqual(
            parse("""{"measurements":"78-39-5-14-8TR-30FA" }"""),
            [
                LengthShorthand(
                    total_length=78,
                    tail_length=39,
                    hind_foot_length=5,
                    ear_length=14,
                    tragus_length=8,
                    forearm_length=30,
                    start=17,
                    end=36,
                )
            ],
        )

    def test_length_shorthand_07(self):
        """It handles an estimated body mass with units."""
        self.maxDiff = None
        self.assertEqual(
            parse("Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62g]"),
            [
                LengthShorthand(
                    total_length=91,
                    tail_length=0,
                    hind_foot_length=17,
                    ear_length=22,
                    body_mass=62,
                    body_mass_estimated=True,
                    start=41,
                    end=57,
                )
            ],
        )

    def test_length_shorthand_08(self):
        """It handles an estimated body mass without units."""
        self.assertEqual(
            parse("Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62] x"),
            [
                LengthShorthand(
                    total_length=91,
                    tail_length=0,
                    hind_foot_length=17,
                    ear_length=22,
                    body_mass=62,
                    body_mass_estimated=True,
                    start=41,
                    end=56,
                )
            ],
        )

    def test_length_shorthand_09(self):
        """It handles noise in place of the body mass."""
        self.assertEqual(
            parse('{"measurements":"242-109-37-34=N/D" }'),
            [
                LengthShorthand(
                    total_length=242,
                    tail_length=109,
                    hind_foot_length=37,
                    ear_length=34,
                    start=17,
                    end=30,
                )
            ],
        )

    def test_length_shorthand_10(self):
        """It handles other units."""
        self.maxDiff = None
        self.assertEqual(
            parse('{"measurements":"90-30-16-7=6.9GMS" }'),
            [
                LengthShorthand(
                    start=17,
                    end=34,
                    total_length=90.0,
                    tail_length=30.0,
                    hind_foot_length=16.0,
                    ear_length=7.0,
                    body_mass=6.9,
                )
            ],
        )

    def test_length_shorthand_11(self):
        """It handles unlabeled bat measurements."""
        self.assertEqual(
            parse("143-63-20-17-22=13"),
            [
                LengthShorthand(
                    total_length=143,
                    tail_length=63,
                    hind_foot_length=20,
                    ear_length=17,
                    forearm_length=22,
                    body_mass=13,
                    start=0,
                    end=18,
                )
            ],
        )

    def test_length_shorthand_12(self):
        """It handles a missing measurement."""
        self.assertEqual(
            parse('{"measurements":"159-?-22-16=21.0" }'),
            [
                LengthShorthand(
                    total_length=159,
                    hind_foot_length=22,
                    ear_length=16,
                    body_mass=21,
                    start=17,
                    end=33,
                )
            ],
        )

    def test_length_shorthand_13(self):
        """It handles a missing body mass."""
        self.assertEqual(
            parse('{"measurements":"159-?-22-16" }'),
            [
                LengthShorthand(
                    total_length=159,
                    hind_foot_length=22,
                    ear_length=16,
                    start=17,
                    end=28,
                )
            ],
        )

    def test_length_shorthand_14(self):
        """It handles an estimated total length."""
        self.assertEqual(
            parse('{"measurements":"[159]-?-22-16" }'),
            [
                LengthShorthand(
                    total_length=159,
                    total_length_estimated=True,
                    hind_foot_length=22,
                    ear_length=16,
                    start=17,
                    end=30,
                )
            ],
        )

    def test_length_shorthand_15(self):
        """It handles 3-form shorthand notation."""
        self.assertEqual(
            parse('{"measurements":"210-92-30" }'),
            [
                LengthShorthand(
                    total_length=210,
                    tail_length=92,
                    hind_foot_length=30,
                    start=1,
                    end=27,
                )
            ],
        )
