import unittest
from PIL import Image
from unittest.mock import patch, MagicMock
from SICAR.drivers import Paddle
import paddleocr


class PaddleTestCase(unittest.TestCase):
    @patch.object(paddleocr.PaddleOCR, "__init__", return_value=None)
    @patch("re.sub")
    @patch("SICAR.drivers.paddle.Paddle._process_captcha")
    def test_get_captcha(self, process_captcha_mock, re_mock, paddle_mock):
        ocr_result = [(["ABC123", 0.99],)]
        captcha_image = MagicMock(spec=Image.Image)

        paddle = Paddle()
        paddle.ocr.ocr = MagicMock(return_value=ocr_result)

        paddle_mock.assert_called_once_with(
            use_angle_cls=False, lang="en", use_space_char=False, show_log=False
        )

        result = paddle.get_captcha(captcha_image)

        process_captcha_mock.assert_called_once_with(captcha_image)

        paddle.ocr.ocr.assert_called_once_with(
            process_captcha_mock.return_value, det=False, cls=False
        )

        re_mock.assert_called_once_with("[^A-Za-z0-9]+", "", "ABC123")

        self.assertEqual(result, re_mock.return_value)

    @patch("paddleocr.PaddleOCR", side_effect=ImportError)
    def test_paddle_import_failure(self, paddle_mock):
        with self.assertRaises(ImportError):
            paddleocr.PaddleOCR()
