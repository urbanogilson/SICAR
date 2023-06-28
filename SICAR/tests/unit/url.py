import unittest
from SICAR.url import Url


class UrlTestCase(unittest.TestCase):
    def test_base_url(self):
        self.assertEqual(Url._BASE, "https://www.car.gov.br/publico")

    def test_index_url(self):
        self.assertEqual(Url._INDEX, "https://www.car.gov.br/publico/imoveis/index")

    def test_downloads_url(self):
        self.assertEqual(
            Url._DOWNLOADS, "https://www.car.gov.br/publico/municipios/downloads"
        )

    def test_csv_url(self):
        self.assertEqual(Url._CSV, "https://www.car.gov.br/publico/municipios/csv")

    def test_captcha_url(self):
        self.assertEqual(
            Url._CAPTCHA, "https://www.car.gov.br/publico/municipios/captcha"
        )

    def test_shapefile_url(self):
        self.assertEqual(
            Url._SHAPEFILE, "https://www.car.gov.br/publico/municipios/shapefile"
        )
