import unittest

from ranges.rules.gonad import Gonad
from tests.setup import parse


class TestGonadSize(unittest.TestCase):
    def test_gonad_size_01(self) -> None:
        self.assertEqual(
            parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Gonad(
                    length1=3,
                    units_inferred=True,
                    start=1,
                    end=21,
                ),
                Gonad(
                    length1=2,
                    units_inferred=True,
                    start=25,
                    end=45,
                ),
            ],
        )

    def test_gonad_size_02(self) -> None:
        self.assertEqual(
            parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [
                Gonad(
                    length1=12,
                    start=1,
                    end=21,
                ),
                Gonad(
                    width1=5,
                    start=25,
                    end=43,
                ),
            ],
        )

    def test_gonad_03(self) -> None:
        self.assertEqual(
            parse("tag# 1089; bag# 156; no gonads"),
            [],
        )

    def test_gonad_04(self) -> None:
        self.assertEqual(
            parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Gonad(
                    length1=3,
                    units_inferred=True,
                    start=1,
                    end=21,
                ),
                Gonad(
                    length1=2,
                    units_inferred=True,
                    start=25,
                    end=45,
                ),
            ],
        )

    def test_gonad_05(self) -> None:
        self.maxDiff = None
        self.assertEqual(
            parse(
                "left gonad width1=9.1 mm; right gonad width=9.2 mm; "
                "right gonad length=16.1 mm; left gonad length=16.2 mm"
            ),
            [
                Gonad(start=5, end=24, width1=9.1),
                Gonad(start=32, end=50, width1=9.2),
                Gonad(start=58, end=78, length1=16.1),
                Gonad(start=85, end=105, length1=16.2),
            ],
        )

    def test_gonad_06(self) -> None:
        self.assertEqual(
            parse('"gonadLengthInMM":"9mm w.o./epid", '),
            [Gonad(length1=9, start=1, end=22)],
        )
