import unittest
from SICAR.drivers import Manual
from pathlib import Path
from unittest.mock import patch


class TestManualDriver(unittest.TestCase):
    _captcha = "Ca7Qk"

    @classmethod
    def setUpClass(self):
        self._driver = Manual()

    @patch("builtins.input", return_value=_captcha)
    def test_get_captcha(self, mock_input):
        self.assertEqual(
            self._driver._get_captcha(
                Path("SICAR/tests/captchas/{}.png".format(self._captcha))
            ),
            self._captcha,
        )


if __name__ == "__main__":
    unittest.main()
