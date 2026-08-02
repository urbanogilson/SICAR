import unittest
from unittest.mock import MagicMock, patch

import cv2
import paddleocr
from PIL import Image

from SICAR.drivers import Paddle


class PaddleTestCase(unittest.TestCase):
    @patch("SICAR.drivers.paddle.cv2.cvtColor")
    @patch("re.sub")
    @patch("SICAR.drivers.paddle.Paddle._process_captcha")
    @patch("SICAR.drivers.paddle.TextRecognition")
    def test_get_captcha(
        self, text_recognition_mock, process_captcha_mock, re_mock, cvtcolor_mock
    ):
        captcha_image = MagicMock(spec=Image.Image)

        paddle = Paddle()

        text_recognition_mock.assert_called_once_with(
            model_name="en_PP-OCRv4_mobile_rec"
        )

        paddle.ocr.predict = MagicMock(return_value=[{"rec_text": "ABC123"}])

        result = paddle.get_captcha(captcha_image)

        process_captcha_mock.assert_called_once_with(captcha_image)
        cvtcolor_mock.assert_called_once_with(
            process_captcha_mock.return_value, cv2.COLOR_GRAY2BGR
        )
        paddle.ocr.predict.assert_called_once_with(cvtcolor_mock.return_value)
        re_mock.assert_called_once_with("[^A-Za-z0-9]+", "", "ABC123")

        self.assertEqual(result, re_mock.return_value)

    @patch("paddleocr.TextRecognition", side_effect=ImportError)
    def test_paddle_import_failure(self, paddle_mock):
        with self.assertRaises(ImportError):
            paddleocr.TextRecognition()
