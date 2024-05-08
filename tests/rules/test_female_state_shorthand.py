import unittest

from ranges.pylib.rules.female_state_shorthand import FemaleStateShorthand
from tests.setup import parse


class TestFemaleStateShorthand(unittest.TestCase):
    def test_female_state_shorthand_01(self):
        self.assertEqual(
            parse("oen"),
            [
                FemaleStateShorthand(
                    vagina_state="open",
                    nipple_state="enlarged",
                    lactation_state="not lactating",
                    start=0,
                    end=3,
                )
            ],
        )

    def test_female_state_shorthand_02(self):
        self.assertEqual(
            parse("cmlac"),
            [
                FemaleStateShorthand(
                    vagina_state="closed",
                    nipple_state="medium",
                    lactation_state="lactating",
                    start=0,
                    end=5,
                )
            ],
        )
