import unittest

from ranges.rules.lactation_state import LactationState
from tests.setup import parse


class TestLactationState(unittest.TestCase):
    def test_lactation_state_01(self) -> None:
        self.assertEqual(
            parse("lactating"),
            [LactationState(lactation=True, description="lactating", start=0, end=9)],
        )

    def test_lactation_state_02(self) -> None:
        self.assertEqual(
            parse("not lactating"),
            [
                LactationState(
                    lactation=False, description="not lactating", start=0, end=13
                )
            ],
        )

    def test_lactation_state_03(self) -> None:
        self.assertEqual(
            parse("post lact."),
            [LactationState(lactation=False, description="post lact", start=0, end=9)],
        )

    def test_lactation_state_04(self) -> None:
        self.assertEqual(
            parse("non-lactating"),
            [
                LactationState(
                    lactation=False, description="non-lactating", start=0, end=13
                )
            ],
        )

    def test_lactation_state_05(self) -> None:
        self.assertEqual(
            parse("lactating?"),
            [LactationState(lactation=True, description="lactating", start=0, end=9)],
        )

    def test_lactation_state_06(self) -> None:
        self.assertEqual(
            parse("recently lactating"),
            [
                LactationState(
                    lactation=False, description="recently lactating", start=0, end=18
                )
            ],
        )

    def test_lactation_state_07(self) -> None:
        self.assertEqual(
            parse("no lactation,"),
            [
                LactationState(
                    lactation=False, description="no lactation", start=0, end=12
                )
            ],
        )

    def test_lactation_state_08(self) -> None:
        self.assertEqual(
            parse("just finished lactating"),
            [
                LactationState(
                    lactation=False, description="finished lactating", start=5, end=23
                )
            ],
        )

    def test_lactation_state_09(self) -> None:
        self.assertEqual(
            parse("reproductive data=non-lactating,"),
            [
                LactationState(
                    lactation=False, description="non-lactating", start=18, end=31
                )
            ],
        )

    def test_lactation_state_10(self) -> None:
        self.assertEqual(
            parse("Tail pencil; Not nursing,"),
            [
                LactationState(
                    lactation=False, description="Not nursing", start=13, end=24
                )
            ],
        )

    def test_lactation_state_11(self) -> None:
        self.assertEqual(
            parse("no. 8552; suckling"),
            [LactationState(lactation=True, description="suckling", start=10, end=18)],
        )

    def test_lactation_state_12(self) -> None:
        self.assertEqual(
            parse("; NIPPLES INDICATE PREVIOUS LACTATION"),
            [
                LactationState(
                    lactation=False, description="PREVIOUS LACTATION", start=19, end=37
                )
            ],
        )
