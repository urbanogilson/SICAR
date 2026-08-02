import os
import unittest
from pathlib import Path

from PIL import Image

from SICAR.drivers import Tesseract


class TestTesseractDriver(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._driver = Tesseract()
        self._captchas = Path(__file__).parent / "captchas"

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
