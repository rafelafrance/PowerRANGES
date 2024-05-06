# import unittest
#
# from ranges.pylib.rules.pregnancy_state import PregnancyState
# from tests.setup import parse
#
#
# class TestScrotalState(unittest.TestCase):
#     def test_scrotal_state_01(self):
#         self.assertEqual(
#             parse("testes not-scrotal"),
#             [PregnancyState(state="testes not-scrotal", start=0, end=18)],
#         )
#
#     def test_scrotal_state_02(self):
#         self.assertEqual(
#             parse("testes no scrotum"),
#             [PregnancyState(state="testes no scrotum", start=0, end=17)],
#         )
#
#     def test_scrotal_state_03(self):
#         self.assertEqual(
#             parse("testis nscr"),
#             [PregnancyState(state="testis nscr", start=0, end=11)],
#         )
#
#     def test_scrotal_state_04(self):
#         self.assertEqual(
#             parse("testes ns"), [PregnancyState(state="testes ns", start=0, end=9)]
#         )
#
#     def test_scrotal_state_05(self):
#         self.assertEqual(
#             parse("t nscr"), [PregnancyState(state="t nscr", start=0, end=6)]
#         )
#
#     def test_scrotal_state_06(self):
#         self.assertEqual(
#             parse("t ns"), [{"end": 4, "start": 0, "state": "t ns"}]
#         )
#
#     def test_scrotal_state_07(self):
#         self.assertEqual(
#             parse(
#                 "weight=36 g; reproductive data=testes: 11x7 mm (scrotal)"
#             ),
#             [PregnancyState(state="scrotal", start=48, end=55)],
#         )
#
#     def test_scrotal_state_08(self):
#         self.assertEqual(
#             parse("non-scrotal, sem. ves. 14 mm "),
#             [PregnancyState(state="non-scrotal", start=0, end=11)],
#         )
#
#     def test_scrotal_state_09(self):
#         self.assertEqual(
#             parse(
#                 "sex=male ; age class=adult ; reproductive data=scrotal ; "
#                 "hind foot with claw=32 mm; weight=82 g; weight=78 g; "
#                 "weight=87 g; weight=94 g; reproductive data=nonscrotal ; "
#                 "sex=male ; sex=male ; reproductive data=nonscrotal ; "
#                 "reproductive data=nonscrotal ; sex=male ; hind foot with "
#                 "claw=32 mm; hind foot with claw=34 mm; hind foot with "
#                 "claw=34 mm; age class=adult ; age class=adult ; "
#                 "age class=adult"
#             ),
#             [
#                 PregnancyState(state="scrotal", start=47, end=54),
#                 PregnancyState(state="nonscrotal", start=154, end=164),
#                 PregnancyState(state="nonscrotal", start=207, end=217),
#                 PregnancyState(state="nonscrotal", start=238, end=248),
#             ],
#         )
#
#     def test_scrotal_state_10(self):
#         self.assertEqual(
#             parse("reproductive data=NS ;"),
#             [PregnancyState(state="ns", start=0, end=20)],
#         )
#
#     def test_scrotal_state_11(self):
#         self.assertEqual(
#             parse("reproductive data=SCR ;"),
#             [PregnancyState(state="scr", start=18, end=21)],
#         )
