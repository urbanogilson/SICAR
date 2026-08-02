import unittest
from pathlib import Path

from SICAR import Polygon, Sicar, State


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_download_state(self):
        self.assertIsInstance(
            self._car.download_state(State.RR, Polygon.AREA_FALL, debug=True),
            Path,
        )

    def test_get_release_dates(self):
        self.assertIsInstance(self._car.get_release_dates(), dict)
