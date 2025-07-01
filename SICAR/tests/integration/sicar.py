# SICAR/tests/integration/sicar.py
import os
from pathlib import Path
import unittest
from unittest.mock import patch

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

    @patch("SICAR.sicar.Sicar._download_polygon")
    def test_download_resume(self, mock_download):
        state = State.RR
        polygon = Polygon.AREA_FALL
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / f"{state.value}_{polygon.value}.zip"

        def mock_download_side_effect(*args, **kwargs):
            if not path.exists():
                with open(path, "wb") as fd:
                    fd.write(b"Partial content")
            else:
                with open(path, "ab") as fd:
                    fd.write(b" - resumed content")

            return path

        mock_download.side_effect = mock_download_side_effect

        self._car.download_state(state, polygon, folder=folder, debug=True)
        downloaded_path = self._car.download_state(state, polygon, folder=folder, debug=True)

        self.assertTrue(downloaded_path.exists())

        with open(downloaded_path, "rb") as fd:
            content = fd.read()

        self.assertIn(b"Partial content", content)
        self.assertIn(b"resumed content", content)

    def test_get_release_dates(self):
        self.assertIsInstance(self._car.get_release_dates(), dict)
