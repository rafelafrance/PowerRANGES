import unittest

from ranges.pylib.rules.shorthand_female_states import ShorthandFemaleStates
from tests.setup import parse


class TestFemaleStates(unittest.TestCase):
    def test_shorthand_female_states_state_01(self):
        self.assertEqual(
            parse("oen"),
            [
                ShorthandFemaleStates(
                    vagina_state="open",
                    nipple_state="enlarged",
                    lactation_state="not lactating",
                    start=0,
                    end=3,
                )
            ],
        )

    def test_shorthand_female_states_state_02(self):
        self.assertEqual(
            parse("cmlac"),
            [
                ShorthandFemaleStates(
                    vagina_state="closed",
                    nipple_state="medium",
                    lactation_state="lactating",
                    start=0,
                    end=5,
                )
            ],
        )
