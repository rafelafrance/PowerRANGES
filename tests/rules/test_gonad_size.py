import unittest

from ranges.pylib.rules.gonad import Gonad
from tests.setup import parse


class TestGonadSize(unittest.TestCase):
    def test_gonad_size_01(self):
        self.assertEqual(
            parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Gonad(
                    length=3,
                    units_inferred=True,
                    start=1,
                    end=21,
                ),
                Gonad(
                    length=2,
                    units_inferred=True,
                    start=25,
                    end=45,
                ),
            ],
        )

    def test_gonad_size_02(self):
        self.assertEqual(
            parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [
                Gonad(
                    length=12,
                    start=1,
                    end=21,
                ),
                Gonad(
                    width=5,
                    start=25,
                    end=43,
                ),
            ],
        )

    def test_gonad_03(self):
        self.assertEqual(
            parse("tag# 1089; bag# 156; no gonads"),
            [],
        )

    def test_gonad_04(self):
        self.assertEqual(
            parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Gonad(
                    length=3,
                    units_inferred=True,
                    start=1,
                    end=21,
                ),
                Gonad(
                    length=2,
                    units_inferred=True,
                    start=25,
                    end=45,
                ),
            ],
        )

    def test_gonad_05(self):
        self.assertEqual(
            parse(
                "left gonad width=9.1 mm; right gonad width=9.2 mm; "
                "right gonad length=16.1 mm; left gonad length=16.2 mm"
            ),
            [
                Gonad(start=5, end=23, width=9.1),
                Gonad(start=31, end=49, width=9.2),
                Gonad(start=57, end=77, length=16.1),
                Gonad(start=84, end=104, length=16.2),
            ],
        )

    def test_gonad_06(self):
        self.assertEqual(
            parse('"gonadLengthInMM":"9mm w.o./epid", '),
            [Gonad(length=9, start=1, end=22)],
        )
