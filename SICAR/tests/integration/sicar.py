from pathlib import Path
import unittest
from SICAR import Sicar, OutputFormat


class TestSicarBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._car = Sicar()

    def test_get_cities_codes_valid_state(self):
        cities_codes = self._car.get_cities_codes("RR")
        self.assertIsInstance(
            cities_codes,
            dict,
        )
        self.assertEqual(len(cities_codes), 15)  # 15 cities in Roraima
        self.assertEqual(cities_codes["Alto Alegre"], "1400050")  # Verify city code

    def test_download_city_by_code_shapefile(self):
        self.assertIsInstance(
            self._car.download_city_code("3120870", debug=True),
            Path,
        )

    def test_download_city_by_code_csv(self):
        self.assertIsInstance(
            self._car.download_city_code(
                "3120870", output_format=OutputFormat.CSV, debug=True
            ),
            Path,
        )
