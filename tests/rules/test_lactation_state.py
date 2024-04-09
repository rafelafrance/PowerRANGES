import unittest

from ranges.pylib.rules.lactation_state import LactationState
from tests.setup import parse


class TestLactationState(unittest.TestCase):
    def test_parse_01(self):
        self.assertEqual(
            parse("lactating"),
            [
                LactationState(
                    trait="lactation_state", state="lactating", start=0, end=9
                )
            ],
        )

    def test_parse_02(self):
        self.assertEqual(
            parse("not lactating"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=0, end=13
                )
            ],
        )

    def test_parse_03(self):
        self.assertEqual(
            parse("post lact."),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=0, end=9
                )
            ],
        )

    def test_parse_04(self):
        self.assertEqual(
            parse("non-lactating"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=0, end=13
                )
            ],
        )

    def test_parse_05(self):
        self.assertEqual(
            parse("lactating?"),
            [
                LactationState(
                    trait="lactation_state", state="lactating", start=0, end=9
                )
            ],
        )

    def test_parse_06(self):
        self.assertEqual(
            parse("recently lactating"),
            [
                LactationState(
                    trait="lactation_state", state="lactating", start=9, end=18
                )
            ],
        )

    def test_parse_07(self):
        self.assertEqual(
            parse("small mammaries, no lactation,"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=17, end=29
                )
            ],
        )

    def test_parse_08(self):
        self.assertEqual(
            parse("just finished lactating"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=5, end=23
                )
            ],
        )

    def test_parse_09(self):
        self.assertEqual(
            parse("reproductive data=non-lactating, non-pregnant"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=18, end=31
                )
            ],
        )

    def test_parse_10(self):
        self.assertEqual(
            parse("Tail pencil; Not nursing,"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=13, end=24
                )
            ],
        )

    def test_parse_11(self):
        self.assertEqual(
            parse("no. 8552; suckling"),
            [
                LactationState(
                    trait="lactation_state", state="lactating", start=10, end=18
                )
            ],
        )

    def test_parse_12(self):
        self.assertEqual(
            parse("reproductive data=OEL;"),
            [
                LactationState(
                    trait="lactation_state", state="lactating", start=18, end=21
                )
            ],
        )

    def test_parse_13(self):
        self.assertEqual(
            parse("reproductive data=OSN;"),
            [
                LactationState(
                    trait="lactation_state", state="not lactating", start=18, end=21
                )
            ],
        )
