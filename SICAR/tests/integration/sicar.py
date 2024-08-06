from pathlib import Path
import unittest
from SICAR import Sicar, State, Polygon


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_download_state(self):
        self.assertIsInstance(
            self._car.download_state(State.RR, Polygon.AREA_FALL, debug=True),
            Path,
        )

    def test_refresh_update_date(self):
        self.assertIsInstance(self._car.get_release_dates(), dict)
