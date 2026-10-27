import unittest

from ranges.rules.wingspan import Wingspan
from tests.setup import parse


class TestWingspan(unittest.TestCase):
    def test_wingspan_01(self) -> None:
        self.assertEqual(
            parse("wingspan: 30"),
            [Wingspan(length=30, units_inferred=True, start=0, end=12)],
        )

    def test_wingspan_02(self) -> None:
        self.assertEqual(
            parse("320 mm wingspan"),
            [Wingspan(length=320, start=0, end=15)],
        )
