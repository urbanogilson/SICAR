from pathlib import Path
import unittest
from SICAR import Sicar, State, Polygon


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_download_state(self):
        # self.assertIsInstance(
        #     self._car.download_state(State.AL, Polygon.HYDROGRAPHY, debug=True),
        #     Path,
        # )
        pass
