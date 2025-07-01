# download_car/tests/unit/state.py
import unittest
from download_car import State


class StateTestCase(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(State.AC.value, "AC")
        self.assertEqual(State.AL.value, "AL")
        self.assertEqual(State.AM.value, "AM")
        self.assertEqual(State.AP.value, "AP")
        self.assertEqual(State.BA.value, "BA")
        self.assertEqual(State.CE.value, "CE")
        self.assertEqual(State.DF.value, "DF")
        self.assertEqual(State.ES.value, "ES")
        self.assertEqual(State.GO.value, "GO")
        self.assertEqual(State.MA.value, "MA")
        self.assertEqual(State.MG.value, "MG")
        self.assertEqual(State.MS.value, "MS")
        self.assertEqual(State.MT.value, "MT")
        self.assertEqual(State.PA.value, "PA")
        self.assertEqual(State.PB.value, "PB")
        self.assertEqual(State.PE.value, "PE")
        self.assertEqual(State.PI.value, "PI")
        self.assertEqual(State.PR.value, "PR")
        self.assertEqual(State.RJ.value, "RJ")
        self.assertEqual(State.RN.value, "RN")
        self.assertEqual(State.RO.value, "RO")
        self.assertEqual(State.RR.value, "RR")
        self.assertEqual(State.RS.value, "RS")
        self.assertEqual(State.SC.value, "SC")
        self.assertEqual(State.SE.value, "SE")
        self.assertEqual(State.SP.value, "SP")
        self.assertEqual(State.TO.value, "TO")
