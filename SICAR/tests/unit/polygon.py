import unittest
from SICAR.url import Url


class UrlTestCase(unittest.TestCase):
    def test_base_url(self):
        self.assertEqual(Url._BASE, "https://www.car.gov.br/publico")

    def test_index_url(self):
        self.assertEqual(Url._INDEX, "https://www.car.gov.br/publico/imoveis/index")

    def test_downloads_url(self):
        self.assertEqual(
            Url._DOWNLOAD_BASE, "https://www.car.gov.br/publico/estados/downloadBase"
        )

    def test_captcha_url(self):
        self.assertEqual(
            Url._RECAPTCHA, "https://www.car.gov.br/publico/municipios/ReCaptcha"
        )
