import unittest
from SICAR.drivers import Paddle
from pathlib import Path


class TestPaddleDriver(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._driver = Paddle()
        self._captchas = list(Path("SICAR/tests/captchas").glob("*.png"))

    def test_get_captcha(self):
        for captcha in self._captchas:
            self.assertEqual(
                self._driver._get_captcha(captcha),
                captcha.stem,
            )


if __name__ == "__main__":
    unittest.main()
