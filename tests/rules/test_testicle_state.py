# """Test testes state notations."""
# # pylint: disable=missing-module-docstring,missing-class-docstring
# # pylint: disable=missing-function-docstring,too-many-public-methods
# import unittest
#
# from vertnet.parsers.testes_state import TESTES_STATE
# from vertnet.pylib.trait import Trait
#
#
# class TestTestesState(unittest.TestCase):
#     def test_parse_01(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#             "some words reproductive data=No testicles; more words"),
#             [Trait(value="no testicles", start=29, end=41)],
#         )
#
#     def test_parse_02(self):
#         self.assertEqual(
#             TESTES_STATE.parse("testes descended"),
#             [Trait(value="testes descended", start=0, end=16)],
#         )
#
#     def test_parse_03(self):
#         self.assertEqual(
#             TESTES_STATE.parse("testes undescended"),
#             [Trait(value="testes undescended", start=0, end=18)],
#         )
#
#     def test_parse_04(self):
#         self.assertEqual(
#             TESTES_STATE.parse("testes undesc."),
#             [Trait(value="testes undesc", start=0, end=13)],
#         )
#
#     def test_parse_05(self):
#         self.assertEqual(
#             TESTES_STATE.parse("testes undesc"),
#             [Trait(value="testes undesc", start=0, end=13)],
#         )
#
#     def test_parse_06(self):
#         self.assertEqual(
#             TESTES_STATE.parse("testes not fully descended"),
#             [Trait(value="testes not fully descended", start=0, end=26)],
#         )
#
#     def test_parse_07(self):
#         self.assertEqual(
#             TESTES_STATE.parse("tes undescend."),
#             [Trait(value="tes undescend", start=0, end=13)],
#         )
#
#     def test_parse_08(self):
#         self.assertEqual(
#             TESTES_STATE.parse("t abdominal"),
#             [Trait(value="t abdominal", start=0, end=11)],
#         )
#
#     def test_parse_09(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#                 "hind foot with claw=35 mm; "
#                 "reproductive data=Testes partially descended. "
#                 "Sperm present."
#             ),
#             [Trait(value="testes partially descended", start=45, end=71)],
#         )
#
#     def test_parse_10(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#                 "sex=male ; reproductive data=testis 5mm, abdominal "
#                 "; ear from notch=20 mm; "
#             ),
#             [Trait(value="testis 5mm, abdominal", start=29, end=50)],
#         )
#
#     def test_parse_11(self):
#         self.assertEqual(
#             TESTES_STATE.parse("tag# 1089; bag# 156; no gonads"),
#             [Trait(value="no gonads", ambiguous_key=True, start=21, end=30)],
#         )
#
#     def test_parse_12(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#                 "verbatim preservation date=8 October 1986 ; "
#                 "reproductive data=No testicles"
#             ),
#             [Trait(value="no testicles", start=62, end=74)],
#         )
#
#     def test_parse_13(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#                 "weight=53 g; reproductive data=testes decended, T=8x3 ;"
#             ),
#             [Trait(value="testes decended", start=31, end=46)],
#         )
#
#     def test_parse_14(self):
#         self.assertEqual(
#             TESTES_STATE.parse("weight=75.6 g; reproductive data=Testes small"),
#             [Trait(value="testes small", start=15, end=45)],
#         )
#
#     def test_parse_15(self):
#         self.assertEqual(
#             TESTES_STATE.parse("weight=75.6 g; reproductive data=small"),
#             [Trait(value="small", start=15, end=38)],
#         )
#
#     def test_parse_16(self):
#         self.assertEqual(
#             TESTES_STATE.parse("puncture wound in left abdominal region."), []
#         )
#
#     def test_parse_17(self):
#         self.assertEqual(TESTES_STATE.parse(" reproductive data=plsc"), [])
#
#     def test_parse_18(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#                 "junk before reproductive data=Testes small, not descended"
#             ),
#             [Trait(value="testes small, not descended", start=12, end=57)],
#         )
#
#     def test_parse_19(self):
#         self.assertEqual(
#             TESTES_STATE.parse("Mixed woods // TESTES NOT DESCENDED"),
#             [Trait(value="testes not descended", start=15, end=35)],
#         )
#
#     def test_parse_20(self):
#         self.assertEqual(TESTES_STATE.parse("reproductive data=Uteri small, clear"),
#         [])
#
#     def test_parse_21(self):
#         self.assertEqual(
#             TESTES_STATE.parse("; reproductive data=testes = 4x3 mm; "), []
#         )
#
#     def test_parse_22(self):
#         self.assertEqual(
#             TESTES_STATE.parse("Deciduous woods // TESTES DESCENDED, AND ENLARGED"),
#             [Trait(value="testes descended, and enlarged", start=19, end=49)],
#         )
#
#     def test_parse_23(self):
#         self.assertEqual(
#             TESTES_STATE.parse("Testis abd. Collected with 22 cal. pellet rifle."),
#             [Trait(value="testis abd", start=0, end=10)],
#         )
#
#     def test_parse_24(self):
#         self.assertEqual(
#             TESTES_STATE.parse(
#             "reproductive data=test 3.5x2, pt desc, Et not visib,"),
#             [Trait(value="test 3.5x2, pt desc", start=18, end=37)],
#         )
#     def test_scrotal_state_01(self):
#         self.assertEqual(
#             parse("testes not-scrotal"),
#             [Testes(state="testes not-scrotal", start=0, end=18)],
#         )
#
#     def test_scrotal_state_02(self):
#         self.assertEqual(
#             parse("testes no scrotum"),
#             [Testes(state="testes no scrotum", start=0, end=17)],
#         )
#
#     def test_scrotal_state_03(self):
#         self.assertEqual(
#             parse("testis nscr"),
#             [Testes(state="testis nscr", start=0, end=11)],
#         )
#
#     def test_scrotal_state_04(self):
#         self.assertEqual(
#             parse("testes ns"), [Testes(state="testes ns", start=0, end=9)]
#         )
#
#     def test_scrotal_state_05(self):
#         self.assertEqual(parse("t nscr"), [Testes(state="t nscr", start=0, end=6)])
#
#     def test_scrotal_state_06(self):
#         self.assertEqual(parse("t ns"), [{"end": 4, "start": 0, "state": "t ns"}])
#
#     def test_scrotal_state_07(self):
#         self.assertEqual(
#             parse("reproductive data=testes: 11x7 mm (scrotal)"),
#             [Testes(state="scrotal", start=48, end=55)],
#         )
#
#     def test_scrotal_state_08(self):
#         self.assertEqual(
#             parse("non-scrotal, sem. ves. 14 mm "),
#             [Testes(state="non-scrotal", start=0, end=11)],
#         )
#
#     def test_scrotal_state_09(self):
#         self.assertEqual(
#             parse("reproductive data=NS ;"),
#             [Testes(state="ns", start=0, end=20)],
#         )
#
#     def test_scrotal_state_10(self):
#         self.assertEqual(
#             parse("reproductive data=SCR ;"),
#             [Testes(state="scr", start=18, end=21)],
#         )
