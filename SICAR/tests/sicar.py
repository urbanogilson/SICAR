from pathlib import Path
import unittest
from SICAR import Sicar, OutputFormat


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_get_base_url(self):
        self.assertRegex(self._car.get_base_url(), "car.gov.br")

    def test_download_city_by_code_shapefile(self):
        self.assertIsInstance(
            self._car.download_city_code("3120870"),
            Path,
        )

    def test_download_city_by_code_csv(self):
        self.assertIsInstance(
            self._car.download_city_code("3120870", output_format=OutputFormat.CSV),
            Path,
        )


if __name__ == "__main__":
    unittest.main()
