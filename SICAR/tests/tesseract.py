import unittest
from SICAR.drivers import Tesseract
from pathlib import Path


class TestTesseractDriver(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._driver = Tesseract()
        self._captcha = "Ca7Qk"

    def test_get_captcha(self):
        self.assertEqual(
            self._driver._get_captcha(
                Path(f"SICAR/tests/captchas/{self._captcha}.png")
            ),
            self._captcha,
        )


if __name__ == "__main__":
    unittest.main()
