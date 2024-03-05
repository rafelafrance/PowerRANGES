# import unittest
#
# from ranges.pylib.rules.body_mass import BodyMass
# from tests.setup import parse
#
#
# class TestBodyMass(unittest.TestCase):
#     def test_parse_01(self):
#         self.assertEqual(
#             parse("TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx"),
#             [BodyMass(mass=0.77, units_inferred=False, start=22, end=37)],
#         )
#
#     def test_parse_02(self):
#         self.assertEqual(
#             parse("Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g"),
#             [
#                 BodyMass(
#                     mass=62,
#                     units_inferred=False,
#                     shorthand=True,
#                     start=41,
#                     end=55,
#                 )
#             ],
#         )
#
#     def test_parse_03(self):
#         self.assertEqual(
#             parse("body mass=20 g"),
#             [BodyMass(mass=20, units_inferred=False, start=0, end=14)],
#         )
#
#     def test_parse_04(self):
#         self.assertEqual(
#             parse("2 lbs. 3.1 - 4.5 oz "),
#             [
#                 BodyMass(
#                     mass=[995.06, 1034.75],
#                     ambiguous=True,
#                     units_inferred=False,
#                     start=0,
#                     end=19,
#                 )
#             ],
#         )
#
#     def test_parse_05(self):
#         self.assertEqual(
#             parse(
#                 '{"totalLengthInMM":"x", "earLengthInMM":"20", '
#                 '"weight":"[139.5] g" }'
#             ),
#             [
#                 BodyMass(
#                     mass=139.5,
#                     units_inferred=False,
#                     estimated=True,
#                     start=47,
#                     end=65,
#                 )
#             ],
#         )
#
#     def test_parse_06(self):
#         self.assertEqual(
#             parse(
#                 '{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
#                 '"molt":"No molt",'
#                 ' "stomach contents":"Not recorded", "weight":"94 gr."'
#             ),
#             [BodyMass(mass=94, units_inferred=False, start=101, end=115)],
#         )
#
#     def test_parse_07(self):
#         self.assertEqual(
#             parse('{"measurements":"20.2g, SVL 89.13mm" }'),
#             [BodyMass(mass=20.2, units_inferred=False, start=2, end=22)],
#         )
#
#     def test_parse_08(self):
#         self.assertEqual(
#             parse("Body: 15 g"),
#             [BodyMass(mass=15, units_inferred=False, start=0, end=10)],
#         )
#
#     def test_parse_09(self):
#         self.assertEqual(
#             parse('{ "massingrams"="20.1" }'),
#             [BodyMass(mass=20.1, units_inferred=False, start=3, end=21)],
#         )
#
#     def test_parse_10(self):
#         self.assertEqual(
#             parse(
#                 ' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
#                 '"weight":"1,192.0" }'
#             ),
#             [BodyMass(mass=1192, units_inferred=True, start=54, end=70)],
#         )
#
#     def test_parse_11(self):
#         self.assertEqual(
#             parse('"weight: 20.5-31.8'),
#             [BodyMass(mass=[20.5, 31.8], units_inferred=True, start=1, end=18)],
#         )
#
#     def test_parse_12(self):
#         self.assertEqual(
#             parse('"weight: 20.5-32'),
#             [BodyMass(mass=[20.5, 32], units_inferred=True, start=1, end=16)],
#         )
#
#     def test_parse_13(self):
#         self.assertEqual(
#             parse('"weight: 21-31.8'),
#             [BodyMass(mass=[21, 31.8], units_inferred=True, start=1, end=16)],
#         )
#
#     def test_parse_14(self):
#         self.assertEqual(
#             parse('"weight: 21-32'),
#             [BodyMass(mass=[21, 32], units_inferred=True, start=1, end=14)],
#         )
#
#     def test_parse_15(self):
#         self.assertEqual(parse("Specimen #'s - 5491,5492"), [])
#
#     def test_parse_16(self):
#         self.assertEqual(
#             parse("body mass=0 g"),
#             [BodyMass(mass=0, units_inferred=False, start=0, end=13)],
#         )
#
#     def test_parse_17(self):
#         self.assertEqual(
#             parse("2 lbs. 3.1 oz "),
#             [
#                 BodyMass(
#                     mass=995.06,
#                     ambiguous=True,
#                     units_inferred=False,
#                     start=0,
#                     end=13,
#                 )
#             ],
#         )
#
#     def test_parse_18(self):
#         self.assertEqual(
#             parse("wt=10 g"),
#             [BodyMass(mass=10, units_inferred=False, start=0, end=7)],
#         )
#
#     def test_parse_19(self):
#         self.assertEqual(
#             parse("w.t.=10 g"),
#             [BodyMass(mass=10, units_inferred=False, start=0, end=9)],
#         )
#
#     def test_parse_20(self):
#         self.assertEqual(
#             parse("; weight = [50.8] g ;"),
#             [
#                 BodyMass(
#                     mass=50.8,
#                     units_inferred=False,
#                     estimated=True,
#                     start=2,
#                     end=19,
#                 )
#             ],
#         )
#
#     def test_parse_21(self):
#         self.assertEqual(
#             parse("ear from notch=9 mm; weight=.65 kg; reproductive data"),
#             [BodyMass(mass=650, units_inferred=False, start=21, end=34)],
#         )
#
#     def test_parse_22(self):
#         self.assertEqual(
#             parse("; weight=22 oz; Verbatim weight=1lb 6oz;"),
#             [
#                 BodyMass(mass=623.69, units_inferred=False, start=2, end=14),
#                 BodyMass(
#                     mass=623.69,
#                     units_inferred=False,
#                     start=25,
#                     end=39,
#                 ),
#             ],
#         )
#
#     def test_parse_23(self):
#         self.assertEqual(parse("bacu wt=0.09"), [])
#
#     def test_parse_24(self):
#         self.assertEqual(parse("femur wt=1.05"), [])
#
#     def test_parse_25(self):
#         self.assertEqual(
#             parse("Weight=22 lbs., 7 oz.; Length=41 in. T.L."),
#             [
#                 BodyMass(
#                     mass=10177.48,
#                     units_inferred=False,
#                     start=0,
#                     end=20,
#                 )
#             ],
#         )
#
#     def test_parse_26(self):
#         self.assertEqual(
#             parse('{"earLengthInmm":"X", "weightInlbs":"22"}'),
#             [BodyMass(mass=9979.03, units_inferred=False, start=23, end=39)],
#         )
#
#     def test_parse_27(self):
#         self.assertEqual(parse("; unformatted measurements=g 0.24 mm ;"), [])
#
#     def test_parse_28(self):
#         self.assertEqual(
#             parse("143-63-20-17-22=13"),
#             [
#                 BodyMass(
#                     mass=13,
#                     units_inferred=True,
#                     shorthand=True,
#                     start=0,
#                     end=18,
#                 )
#             ],
#         )
#
#     def test_parse_29(self):
#         self.assertEqual(
#             parse(
#                 '{"earLengthInMM":"15 mm", "hindfootLengthInMM":'
#                 '"hind_foot_length]", "measurements":"38", "tail":"40 mm", '
#                 '"totalLength":"96 mm", "weight":"11.7 g" }'
#             ),
#             [BodyMass(mass=11.7, units_inferred=False, start=129, end=144)],
#         )
#
#     def test_parse_30(self):
#         self.assertEqual(parse("Other Measurements: ratio=.33"), [])
#
#     def test_parse_31(self):
#         self.assertEqual(
#             parse(
#                 """
#                 Body: 12 gm; Body and tail: 109 mm; Tail: 43 mm;
#                 Hind Foot: 11 mm; Ear: 13 mm
#                 """
#             ),
#             [BodyMass(mass=12, units_inferred=False, start=0, end=11)],
#         )
