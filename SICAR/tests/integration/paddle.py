import unittest
from SICAR.drivers import Paddle
from pathlib import Path
from PIL import Image


class TestPaddleDriver(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._driver = Paddle()
        self._captchas = list(Path("SICAR/tests/integration/captchas").glob("*.png"))

    def test_get_captchas(self):
        for captcha in self._captchas:
            with self.subTest(
                msg="Checking paddle captcha detection", captcha_name=captcha.stem
            ):
                self.assertEqual(
                    self._driver.get_captcha(Image.open(captcha)),
                    captcha.stem,
                )
