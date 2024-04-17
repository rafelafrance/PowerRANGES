import unittest

from ranges.pylib.rules.lactation_state import LactationState
from tests.setup import parse


class TestLactationState(unittest.TestCase):
    def test_lactation_state_01(self):
        self.assertEqual(
            parse("lactating"),
            [LactationState(state="lactating", start=0, end=9)],
        )

    def test_lactation_state_02(self):
        self.assertEqual(
            parse("not lactating"),
            [LactationState(state="not lactating", start=0, end=13)],
        )

    def test_lactation_state_03(self):
        self.assertEqual(
            parse("post lact."),
            [LactationState(state="not lactating", start=0, end=9)],
        )

    def test_lactation_state_04(self):
        self.assertEqual(
            parse("non-lactating"),
            [LactationState(state="not lactating", start=0, end=13)],
        )

    def test_lactation_state_05(self):
        self.assertEqual(
            parse("lactating?"),
            [LactationState(state="lactating", start=0, end=9)],
        )

    def test_lactation_state_06(self):
        self.assertEqual(
            parse("recently lactating"),
            [LactationState(state="not lactating", start=0, end=18)],
        )

    def test_lactation_state_07(self):
        self.assertEqual(
            parse("no lactation,"),
            [LactationState(state="not lactating", start=0, end=12)],
        )

    def test_lactation_state_08(self):
        self.assertEqual(
            parse("just finished lactating"),
            [LactationState(state="not lactating", start=5, end=23)],
        )

    def test_lactation_state_09(self):
        self.assertEqual(
            parse("reproductive data=non-lactating, non-pregnant"),
            [LactationState(state="not lactating", start=18, end=31)],
        )

    def test_lactation_state_10(self):
        self.assertEqual(
            parse("Tail pencil; Not nursing,"),
            [LactationState(state="not lactating", start=13, end=24)],
        )

    def test_lactation_state_11(self):
        self.assertEqual(
            parse("no. 8552; suckling"),
            [LactationState(state="lactating", start=10, end=18)],
        )

    def test_lactation_state_12(self):
        self.assertEqual(
            parse("; NIPPLES INDICATE PREVIOUS LACTATION"),
            [LactationState(state="not lactating", start=19, end=37)],
        )
