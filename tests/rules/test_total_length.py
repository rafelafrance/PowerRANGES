import unittest

from ranges.pylib.rules.total_length import TotalLength
from tests.setup import parse


class TestTotalLength(unittest.TestCase):
    def test_total_length_01(self):
        self.assertEqual(
            parse('{"totalLengthInMM":"123" };'),
            [TotalLength(trait="total_length", length=123, start=2, end=23)],
        )

    def test_total_length_02(self):
        """It handles a total length without units."""
        self.assertEqual(
            parse("measurements: ToL=230;"),
            [
                TotalLength(
                    trait="total_length",
                    length=230,
                    units_inferred=True,
                    start=14,
                    end=21,
                ),
            ],
        )

    def test_total_length_03(self):
        """It handles a total length with units."""
        self.assertEqual(
            parse(" total length=231 mm;"),
            [
                TotalLength(trait="total_length", length=231, start=0, end=19),
            ],
        )

    def test_total_length_04(self):
        """It parses a snout-vent length."""
        self.assertEqual(
            parse("snout-vent length=54 mm;"),
            [
                TotalLength(trait="total_length", length=54, start=0, end=23),
            ],
        )

    def test_total_length_05(self):
        """It parses a compound total length."""
        self.assertEqual(
            parse("t.l.= 2 feet 3.1 - 4.5 inches "),
            [
                TotalLength(
                    trait="total_length",
                    length=[688.34, 723.9],
                    start=0,
                    end=29,
                )
            ],
        )

    def test_total_length_06(self):
        """It parses a compound total length without a key."""
        self.assertEqual(
            parse("2 ft. 3.1 - 4.5 in. "),
            [
                TotalLength(
                    trait="total_length",
                    length=[688.34, 723.9],
                    ambiguous=True,
                    start=0,
                    end=19,
                )
            ],
        )

    def test_total_length_07(self):
        """It handles different units."""
        self.assertEqual(
            parse("total length= 2 ft."),
            [TotalLength(trait="total_length", length=609.6, start=0, end=19)],
        )

    def test_total_length_08(self):
        """It handles an ambiguous key."""
        self.assertEqual(
            parse("length=8 mm"),
            [
                TotalLength(
                    trait="total_length",
                    length=8,
                    ambiguous=True,
                    start=0,
                    end=11,
                )
            ],
        )

    # def test_total_length_017(self):
    #     self.assertEqual(
    #         parse("another; length=8 mm"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=8,
    #                 ambiguous=True,
    #                 start=9,
    #                 end=20,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_018(self):
    #     self.assertEqual(
    #         parse("another; TL_120, noise"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=120,
    #                 units_inferred=True,
    #                 start=9,
    #                 end=15,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_019(self):
    #     self.assertEqual(
    #         parse("another; TL - 101.3mm, noise"),
    #         [TotalLength(trait="total_length", length=101.3, start=9, end=21)],
    #     )
    #
    # def test_total_length_020(self):
    #     self.assertEqual(
    #         parse("before; TL153, after"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=153,
    #                 units_inferred=True,
    #                 start=8,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_021(self):
    #     self.assertEqual(
    #         parse("before; Total length in catalog and specimen tag as 117, after"),
    #         [],
    #     )
    #
    # def test_total_length_022(self):
    #     self.assertEqual(
    #         parse("before Snout vent lengths range from 16 to 23 mm. noise"),
    #         [TotalLength(trait="total_length", length=[16, 23], start=7, end=48)],
    #     )
    #
    # def test_total_length_023(self):
    #     self.assertEqual(
    #         parse("Size=13 cm TL"),
    #         [TotalLength(trait="total_length", length=130, start=5, end=13)],
    #     )
    #
    # def test_total_length_024(self):
    #     self.assertEqual(
    #         parse("det_comments:31.5-58.3inTL"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=[800.1, 1480.82],
    #                 start=13,
    #                 end=26,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_025(self):
    #     self.assertEqual(
    #         parse("SVL52mm"),
    #         [TotalLength(trait="total_length", length=52, start=0, end=7)],
    #     )
    #
    # def test_total_length_026(self):
    #     self.assertEqual(
    #         parse(
    #             "snout-vent length=221 mm; total length=257 mm; " "tail length=36 mm"
    #         ),
    #         [
    #             TotalLength(trait="total_length", length=221, start=0, end=24),
    #             TotalLength(trait="total_length", length=257, start=26, end=45),
    #         ],
    #     )
    #
    # def test_total_length_027(self):
    #     self.assertEqual(
    #         parse("SVL 209 mm, total 272 mm, 4.4 g."),
    #         [
    #             TotalLength(trait="total_length", length=209, start=0, end=10),
    #             TotalLength(trait="total_length", length=272, start=12, end=24),
    #         ],
    #     )
    #
    # def test_total_length_028(self):
    #     self.assertEqual(
    #         parse('{"time collected":"0712-0900", "length":"12.0" }'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=12,
    #                 ambiguous=True,
    #                 units_inferred=True,
    #                 start=32,
    #                 end=45,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_029(self):
    #     self.assertEqual(
    #         parse(
    #             '{"time collected":"1030", "water depth":"1-8", '
    #             '"bottom":"abrupt lava cliff dropping off to sand at '
    #             '45 ft.", "length":"119-137" }'
    #         ),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=[119, 137],
    #                 ambiguous=True,
    #                 units_inferred=True,
    #                 start=109,
    #                 end=125,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_030(self):
    #     self.assertEqual(
    #         parse("TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx"),
    #         [
    #             TotalLength(trait="total_length", length=44, start=0, end=10),
    #             TotalLength(trait="total_length", length=38, start=11, end=21),
    #         ],
    #     )
    #
    # def test_total_length_031(self):
    #     self.assertEqual(
    #         parse('{"totalLengthInMM":"270-165-18-22-31", '),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=270,
    #                 start=2,
    #                 end=36,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_032(self):
    #     self.assertEqual(
    #         parse('{"length":"20-29" }'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=[20, 29],
    #                 ambiguous=True,
    #                 units_inferred=True,
    #                 start=2,
    #                 end=16,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_033(self):
    #     self.assertEqual(
    #      parse("field measurements on fresh dead specimen were " "157-60-20-19-21g"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=157,
    #                 start=6,
    #                 end=63,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_034(self):
    #     self.assertEqual(
    #         parse("f age class: adult; standard length: 63-107mm"),
    #         [TotalLength(trait="total_length", length=[63, 107], start=20, end=45)],
    #     )
    #
    # def test_total_length_035(self):
    #     self.assertEqual(parse("Rehydrated in acetic acid 7/1978-8/1987."), [])
    #
    # def test_total_length_036(self):
    #     self.assertEqual(
    #         parse("age class: adult; standard length: 18.0-21.5mm"),
    #         [TotalLength(trait="total_length", length=[18, 21.5], start=18, end=46)],
    #     )
    #
    # def test_total_length_037(self):
    #     self.assertEqual(
    #         parse("age class: adult; standard length: 18-21.5mm"),
    #         [TotalLength(trait="total_length", length=[18, 21.5], start=18, end=44)],
    #     )
    #
    # def test_total_length_038(self):
    #     self.assertEqual(
    #         parse("age class: adult; standard length: 18.0-21mm"),
    #         [TotalLength(trait="total_length", length=[18, 21], start=18, end=44)],
    #     )
    #
    # def test_total_length_039(self):
    #     self.assertEqual(
    #         parse("age class: adult; standard length: 18-21mm"),
    #         [TotalLength(trait="total_length", length=[18, 21], start=18, end=42)],
    #     )
    #
    # def test_total_length_040(self):
    #     self.assertEqual(
    #         parse(
    #             "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
    #             "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"
    #         ),
    #         [],
    #     )
    #
    # def test_total_length_041(self):
    #     self.assertEqual(
    #         parse("20-28mm SL"),
    #         [TotalLength(trait="total_length", length=[20, 28], start=0, end=10)],
    #     )
    #
    # def test_total_length_042(self):
    #     self.assertEqual(
    #         parse("29mm SL"),
    #         [TotalLength(trait="total_length", length=29, start=0, end=7)],
    #     )
    #
    # def test_total_length_043(self):
    #     self.assertEqual(
    #         parse('{"measurements":"159-?-22-16=21.0" }'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=159,
    #                 start=2,
    #                 end=33,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_045(self):
    #     self.assertEqual(
    #         parse("Meas: L: 21.0"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=21,
    #                 units_inferred=True,
    #                 start=0,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_046(self):
    #     self.assertEqual(
    #         parse("Meas: L: 21.0 cm"),
    #         [TotalLength(trait="total_length", length=210, start=0, end=16)],
    #     )
    #
    # def test_total_length_047(self):
    #     self.assertEqual(
    #         parse("LABEL. LENGTH 375 MM."),
    #         [TotalLength(trait="total_length", length=375, start=0, end=20)],
    #     )
    #
    # def test_total_length_048(self):
    #     self.assertEqual(
    #         parse("SL=12mm"),
    #         [TotalLength(trait="total_length", length=12, start=0, end=7)],
    #     )
    #
    # def test_total_length_049(self):
    #     self.assertEqual(
    #         parse("Size=SL 12-14 mm"),
    #         [TotalLength(trait="total_length", length=[12, 14], start=5, end=16)],
    #     )
    #
    # def test_total_length_050(self):
    #     self.assertEqual(parse("SV 1.2"), [])
    #
    # def test_total_length_051(self):
    #     self.assertEqual(
    #         parse(" Length: 123 mm SL"),
    #         [TotalLength(trait="total_length", length=123, start=1, end=18)],
    #     )
    #
    # def test_total_length_052(self):
    #     self.assertEqual(
    #         parse(" Length: 12-34 mmSL"),
    #         [TotalLength(trait="total_length", length=[12, 34], start=1, end=19)],
    #     )
    #
    # def test_total_length_053(self):
    #     self.assertEqual(
    #         parse("Measurements: L: 21.0 cm"),
    #         [TotalLength(trait="total_length", length=210, start=0, end=24)],
    #     )
    #
    # def test_total_length_054(self):
    #     self.assertEqual(
    #         parse("SVL=44"),
    #         [
    #             TotalLength(
    #              trait="total_length", length=44, units_inferred=True, start=0, end=6
    #             )
    #         ],
    #     )
    #
    # def test_total_length_055(self):
    #     self.assertEqual(parse("SVL=0 g"), [])
    #
    # def test_total_length_056(self):
    #     self.assertEqual(
    #         parse("SVL=44"),
    #         [
    #             TotalLength(
    #               trait="total_length", length=44, units_inferred=True, start=0, end=6
    #             )
    #         ],
    #     )
    #
    # def test_total_length_057(self):
    #     self.assertEqual(
    #         parse("TL=50"),
    #         [
    #             TotalLength(
    #              trait="total_length", length=50, units_inferred=True, start=0, end=5
    #             )
    #         ],
    #     )
    #
    # def test_total_length_058(self):
    #     self.assertEqual(
    #         parse("SVL=44mm"),
    #         [TotalLength(trait="total_length", length=44, start=0, end=8)],
    #     )
    #
    # def test_total_length_059(self):
    #     self.assertEqual(parse("SV 1.4, TAIL 1.0 CM. HATCHLING"), [])
    #
    # def test_total_length_060(self):
    #     self.assertEqual(
    #         parse("LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=263.52,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=16,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_061(self):
    #     self.assertEqual(
    #         parse(
    #             "tail length in mm: -; total length in mm: -; "
    #             "wing chord in mm: 81.0R; wing spread in mm: -"
    #         ),
    #         [],
    #     )
    #
    # def test_total_length_062(self):
    #     self.assertEqual(
    #         parse("76 cm S.L., 4.7 kg"),
    #         [TotalLength(trait="total_length", length=760, start=0, end=10)],
    #     )
    #
    # def test_total_length_063(self):
    #     self.assertEqual(parse("set mark: 661 1-5 64-61"), [])
    #
    # def test_total_length_064(self):
    #     self.assertEqual(
    #         parse('{"totalLength":"970", "wing":"390" }'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=970,
    #                 units_inferred=True,
    #                 start=2,
    #                 end=19,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_065(self):
    #     self.assertEqual(
    #         parse("LENGTH: 117MM. SOFT self.parserTS COLOR ON LABEL."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=117,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_066(self):
    #     self.assertEqual(
    #         parse("Meas:Length (L): 5"),
    #         [
    #             TotalLength(
    #              trait="total_length", length=5, units_inferred=True, start=0, end=18
    #             )
    #         ],
    #     )
    #
    # def test_total_length_067(self):
    #     self.assertEqual(
    #         parse("Size=41-148mm SL"),
    #         [TotalLength(trait="total_length", length=[41, 148], start=5, end=16)],
    #     )
    #
    # def test_total_length_068(self):
    #     self.assertEqual(
    #         parse("Size=105 mm TL, 87.1 mm PCL"),
    #         [TotalLength(trait="total_length", length=105, start=5, end=14)],
    #     )
    #
    # def test_total_length_069(self):
    #     self.assertEqual(
    #         parse("Total Length: 185-252 mm"),
    #         [TotalLength(trait="total_length", length=[185, 252], start=0, end=24)],
    #     )
    #
    # def test_total_length_070(self):
    #     self.assertEqual(
    #         parse("Total Length: 185 - 252 mm"),
    #         [TotalLength(trait="total_length", length=[185, 252], start=0, end=26)],
    #     )
    #
    # def test_total_length_071(self):
    #     self.assertEqual(
    #         parse('"bottom":"rock?", "length":"278" }'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=278,
    #                 ambiguous=True,
    #                 units_inferred=True,
    #                 start=19,
    #                 end=31,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_072(self):
    #     self.assertEqual(
    #         parse("[308]-190-45-20"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=308,
    #                 estimated=True,
    #                 start=0,
    #                 end=15,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_073(self):
    #     self.assertEqual(
    #         parse('"{"measurements":"[308]-190-45-20" }"'),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=308,
    #                 estimated=True,
    #                 start=3,
    #                 end=33,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_074(self):
    #     self.assertEqual(
    #         parse("308-190-45-20-11-22"),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=308,
    #                 start=0,
    #                 end=19,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_081(self):
    #     self.assertEqual(
    #         parse("LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=9.52,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=13,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_082(self):
    #     self.assertEqual(
    #         parse("LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN."),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=9.52,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=15,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_083(self):
    #     self.assertEqual(
    #         parse("unformatted measurements=42-51 mm SL"),
    #         [TotalLength(trait="total_length", length=[42, 51], start=25, end=36)],
    #     )
    #
    # def test_total_length_084(self):
    #   self.assertEqual(parse("verbatim collector=R. D. Svihla 31-605 ; sex=male"), [])
    #
    # def test_total_length_085(self):
    #     self.assertEqual(parse("Cataloged by: R.L. Humphrey, 31 January 1995"), [])
    #
    # def test_total_length_086(self):
    #     self.assertEqual(
    #         parse("measurement on tag for T. L. (141 mm) cannot be correct"),
    #         [TotalLength(trait="total_length", length=141, start=23, end=36)],
    #     )
    #
    # def test_total_length_087(self):
    #     self.assertEqual(
    #         parse("L: 275. T: 65.; "),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=275,
    #                 units_inferred=True,
    #                 ambiguous=True,
    #                 start=0,
    #                 end=6,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_088(self):
    #     self.assertEqual(
    #         parse(
    #             "unformatted measurements=L-11&#34;, T-3.125&#34;, "
    #             "HF-1.5&#34; ; sex=male ; hind foot with claw=1.5 in; "
    #             "total length=11 in; tail length=3.125 in   | .  "
    #             "4/12/39 . | 1.5 TRUE"
    #         ),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=11.0,
    #                 units_inferred=True,
    #                 ambiguous=True,
    #                 start=25,
    #                 end=29,
    #             ),
    #             TotalLength(trait="total_length", length=279.4, start=103, end=121),
    #         ],
    #     )
    #
    # def test_total_length_093(self):
    #     self.assertEqual(
    #         parse('{"measurements":"TL=216.4 cm (+ 5 cm)" }'),
    #         [TotalLength(trait="total_length", length=2164, start=17, end=28)],
    #     )
    #
    # def test_total_length_094(self):
    #     self.assertEqual(
    #         parse("t.l.= 2 feet, 4.5 inches "),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=723.9,
    #                 start=0,
    #                 end=24,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_095(self):
    #     target = (
    #         "The length reported (2560 cm = 85 feet) is a bit "
    #         "large for B. physalus and is more in keeping with B. "
    #         "musculus. Redman, N. (2014). Whales' Bones of France, "
    #         "Southern Europe, Middle East and North Africa. "
    #         "Teddington, England, Redman Publishing. "
    #         "p. 24-25, 41-42"
    #     )
    #     self.assertEqual(parse(target), [])
    #
    # def test_total_length_096(self):
    #     self.assertEqual(parse("ELEV;1100 FT / 1500 FT?"), [])
    #
    # def test_total_length_097(self):
    #     self.assertEqual(
    #         parse(
    #             "This belongs with individual smaller than "
    #             "comparative specimen #4700 in 80-90 cmbd"
    #         ),
    #         [],
    #     )
    #
    # def test_total_length_099(self):
    #     self.assertEqual(
    #         parse('{"measurements":"TL=225 cm (265cm est) flukes cutoff", '),
    #         [TotalLength(trait="total_length", length=2250, start=17, end=26)],
    #     )
    #
    # def test_total_length_100(self):
    #     self.assertEqual(
    #         parse(
    #             '{"measurements":"Weight=56700 TotalLength=1260 Tail=810 '
    #             'HindFoot=470" }'
    #         ),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=1260,
    #                 units_inferred=True,
    #                 start=30,
    #                 end=46,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_101(self):
    #     self.assertEqual(parse("VERY YOUNG. LAST SPECIMEN CATALOGUED IN 1997."), [])
    #
    # def test_total_length_102(self):
    #     self.assertEqual(
    #         parse(
    #             '{"measurements":"Weight=42700 TotalLength=1487.5 ' 'HindFoot=400" }'
    #         ),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=1487.5,
    #                 units_inferred=True,
    #                 start=30,
    #                 end=48,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_103(self):
    #     self.assertEqual(
    #         parse(
    #             "Tail=239.0 mm; Hind Foot=74.0 mm (81.0 mm); Ear=34.0 mm.; "
    #             "Weight=560 g; Length=522.0 mm"
    #         ),
    #         [
    #             TotalLength(
    #                 trait="total_length",
    #                 length=522,
    #                 ambiguous=True,
    #                 start=72,
    #                 end=87,
    #             )
    #         ],
    #     )
    #
    # def test_total_length_104(self):
    #     self.assertEqual(parse("; trap identifier=SV01 S29/40 ;"), [])
    #
    # def test_total_length_105(self):
    #     self.assertEqual(parse("vagina opened; 4 embryos, R=3, L=1, CRL=28mm"), [])
    #
    # def test_total_length_107(self):
    #     self.assertEqual(parse("""Body: 14 g"""), [])
    #
    # def test_total_length_108(self):
    #     self.assertEqual(
    #         parse(
    #             """Body: 12 gm; Body and tail: 109 mm; Tail: 43 mm;
    #                 Hind Foot: 11 mm; Ear: 13 mm"""
    #         ),
    #         [TotalLength(trait="total_length", length=109, start=13, end=34)],
    #     )
    #
    # def test_total_length_109(self):
    #     self.assertEqual(
    #         parse("""Note in catalog: Recatalogued from 115818-850"""),
    #         [],
    #     )
