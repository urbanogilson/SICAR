import unittest
from SICAR.drivers import Tesseract
from pathlib import Path
from PIL import Image
import os


class TestTesseractDriver(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._driver = Tesseract()
        self._captchas = Path("SICAR/tests/integration/captchas")

    def test_get_captcha_AbgBy(self):
        captcha = Path(os.path.join(self._captchas, "AbgBy")).with_suffix(".png")
        self.assertEqual(
            self._driver.get_captcha(Image.open(captcha)),
            captcha.stem,
        )

    def test_get_captcha_Ca7Qk(self):
        captcha = Path(os.path.join(self._captchas, "Ca7Qk")).with_suffix(".png")
        self.assertEqual(
            self._driver.get_captcha(Image.open(captcha)),
            captcha.stem,
        )

    def test_get_captcha_ZS7pc(self):
        captcha = Path(os.path.join(self._captchas, "ZS7pc")).with_suffix(".png")
        self.assertEqual(
            self._driver.get_captcha(Image.open(captcha)),
            captcha.stem,
        )
