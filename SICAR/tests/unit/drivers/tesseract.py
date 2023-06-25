import unittest
from PIL import Image
from unittest.mock import patch, MagicMock
from SICAR.drivers.tesseract import Tesseract


class TesseractTest(unittest.TestCase):
    @patch("pytesseract.image_to_string")
    @patch("re.sub")
    @patch("SICAR.drivers.tesseract.Tesseract._process_captcha")
    def test_get_captcha(self, process_captcha_mock, re_mock, pytesseract_mock):
        pytesseract_mock.return_value = "ABC123"
        captcha_image = MagicMock(spec=Image.Image)
        tesseract = Tesseract()

        result = tesseract.get_captcha(captcha_image)

        process_captcha_mock.assert_called_once_with(captcha_image)

        pytesseract_mock.assert_called_once_with(
            process_captcha_mock.return_value,
            config=tesseract._custom_l_psm_config,
        )

        re_mock.assert_called_once_with(
            "[^A-Za-z0-9]+", "", pytesseract_mock.return_value
        )

        self.assertEqual(result, re_mock.return_value)
