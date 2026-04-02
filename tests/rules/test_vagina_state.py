import unittest

from ranges.rules.vagina_state import VaginaState
from tests.setup import parse


class TestVaginaState(unittest.TestCase):
    def test_vagina_state_01(self) -> None:
        self.assertEqual(
            parse("reproductive data=perf, Pelvis mod. Sep,"),
            [VaginaState(state="open", start=18, end=22)],
        )

    def test_vagina_state_02(self) -> None:
        self.assertEqual(
            parse("reproductive data=Perforate."),
            [VaginaState(state="open", start=18, end=27)],
        )

    def test_vagina_state_03(self) -> None:
        self.assertEqual(
            parse("reproductive data=Uterus clear; OV: No CH ;"),
            [VaginaState(state="open", start=32, end=34)],
        )

    def test_vagina_state_04(self) -> None:
        self.assertEqual(
            parse("reproductive data=Vag. Open."),
            [VaginaState(state="open", start=18, end=27)],
        )

    def test_vagina_state_05(self) -> None:
        self.assertEqual(
            parse("reproductive data=perf, vag. plug,"),
            [VaginaState(state="open, plugged", start=18, end=33)],
        )

    def test_vagina_state_06(self) -> None:
        self.assertEqual(
            parse("vagina swollen"),
            [VaginaState(state="swollen", start=0, end=14)],
        )

    def test_vagina_state_07(self) -> None:
        self.assertEqual(
            parse("reproductive data=imp, lightly healed,"),
            [VaginaState(state="closed", start=18, end=21)],
        )

    def test_vagina_state_08(self) -> None:
        self.assertEqual(
            parse("reproductive data=vulva closed,"),
            [VaginaState(state="closed", start=18, end=30)],
        )
