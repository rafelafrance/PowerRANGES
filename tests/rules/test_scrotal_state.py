import unittest

from ranges.pylib.rules.testes import Testes
from tests.setup import parse


class TestScrotalState(unittest.TestCase):
    def test_scrotal_state_01(self):
        self.assertEqual(
            parse("testes not-scrotal"),
            [Testes(state="testes not-scrotal", start=0, end=18)],
        )

    def test_scrotal_state_02(self):
        self.assertEqual(
            parse("testes no scrotum"),
            [Testes(state="testes no scrotum", start=0, end=17)],
        )

    def test_scrotal_state_03(self):
        self.assertEqual(
            parse("testis nscr"),
            [Testes(state="testis nscr", start=0, end=11)],
        )

    def test_scrotal_state_04(self):
        self.assertEqual(
            parse("testes ns"), [Testes(state="testes ns", start=0, end=9)]
        )

    def test_scrotal_state_05(self):
        self.assertEqual(parse("t nscr"), [Testes(state="t nscr", start=0, end=6)])

    def test_scrotal_state_06(self):
        self.assertEqual(parse("t ns"), [{"end": 4, "start": 0, "state": "t ns"}])

    def test_scrotal_state_07(self):
        self.assertEqual(
            parse("reproductive data=testes: 11x7 mm (scrotal)"),
            [Testes(state="scrotal", start=48, end=55)],
        )

    def test_scrotal_state_08(self):
        self.assertEqual(
            parse("non-scrotal, sem. ves. 14 mm "),
            [Testes(state="non-scrotal", start=0, end=11)],
        )

    def test_scrotal_state_09(self):
        self.assertEqual(
            parse("reproductive data=NS ;"),
            [Testes(state="ns", start=0, end=20)],
        )

    def test_scrotal_state_10(self):
        self.assertEqual(
            parse("reproductive data=SCR ;"),
            [Testes(state="scr", start=18, end=21)],
        )
