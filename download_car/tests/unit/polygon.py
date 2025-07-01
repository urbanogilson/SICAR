# download_car/tests/unit/polygon.py
import unittest
from download_car.url import Url


class UrlTestCase(unittest.TestCase):
    def test_base_url(self):
        self.assertEqual(Url._BASE, "https://consultapublica.car.gov.br/publico")

    def test_index_url(self):
        self.assertEqual(
            Url._INDEX, "https://consultapublica.car.gov.br/publico/imoveis/index"
        )

    def test_downloads_url(self):
        self.assertEqual(
            Url._DOWNLOAD_BASE,
            "https://consultapublica.car.gov.br/publico/estados/downloadBase",
        )

    def test_captcha_url(self):
        self.assertEqual(
            Url._RECAPTCHA,
            "https://consultapublica.car.gov.br/publico/municipios/ReCaptcha",
        )
