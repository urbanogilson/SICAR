import unittest
from unittest.mock import MagicMock, patch, ANY, call
from PIL import Image
import numpy as np
import cv2
from SICAR.drivers import Captcha
import numpy as np


class MockCaptcha(Captcha):
    def get_captcha(self, captcha: Image) -> str:
        return "ABCD1234"


class CaptchaTests(unittest.TestCase):
    def setUp(self):
        self.captcha = MockCaptcha()

    def test_get_captcha(self):
        captcha_image = MagicMock(spec=Image.Image)
        self.assertEqual(self.captcha.get_captcha(captcha_image), "ABCD1234")

    def test_png_to_jpg(self):
        captcha_image = MagicMock(spec=Image.Image)

        named_temp_png = MagicMock()
        named_temp_png.__enter__.return_value.name = "temp.png"
        named_temp_jpg = MagicMock()
        named_temp_jpg.__enter__.return_value.name = "temp.jpg"

        with (
            patch(
                "tempfile.NamedTemporaryFile",
                side_effect=[
                    named_temp_png,
                    named_temp_jpg,
                ],
            ) as mock_tempfile,
            patch("matplotlib.image.imread") as imread_mock,
            patch("matplotlib.image.imsave") as imsave_mock,
            patch("cv2.imread") as cv2_imread_mock,
        ):
            imread_mock.return_value = np.array([[0, 255], [255, 0]])
            imsave_mock.return_value = None
            cv2_imread_mock.return_value = np.array([[0, 255], [255, 0]])

            result = self.captcha._png_to_jpg(captcha_image)

            captcha_image.save.assert_called_once_with("temp.png")

            self.assertEqual(mock_tempfile.call_count, 2)
            self.assertEqual(
                mock_tempfile.call_args_list,
                [call(suffix=".png"), call(suffix=".jpg")],
            )
            imsave_mock.assert_called_once_with(
                "temp.jpg",
                ANY,  # np array is ambiguous
                cmap="gray",
                vmin=0,
                vmax=255,
            )
            imread_mock.assert_called_once()
            cv2_imread_mock.assert_called_once_with("temp.jpg", -1)

            np.testing.assert_array_equal(result, np.array([[0, 255], [255, 0]]))

    def test_improve_image(self):
        image = np.random.randint(0, 256, size=(10, 10), dtype=np.uint8)

        result = self.captcha._improve_image(image)

        # Assert the image processing steps

        expected_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2
        )[1]
        expected_image = cv2.dilate(
            expected_image, np.ones((3, 2), np.uint8), iterations=1
        )
        expected_image = cv2.erode(
            expected_image, np.ones((4, 1), np.uint8), iterations=2
        )
        expected_image = cv2.dilate(
            expected_image, np.ones((3, 1), np.uint8), iterations=2
        )
        expected_image = cv2.erode(
            expected_image, np.ones((2, 1), np.uint8), iterations=2
        )

        np.testing.assert_array_equal(result, expected_image)

    @patch("cv2.cvtColor")
    def test_process_captcha(self, cv2_mock):
        cv2_mock.return_value = np.random.randint(0, 256, size=(10, 10), dtype=np.uint8)
        captcha_image = Image.new("RGB", (10, 10))
        self.captcha._png_to_jpg = MagicMock(return_value=None)
        self.captcha._process_captcha(captcha_image)
        self.captcha._png_to_jpg.assert_called_once_with(captcha_image)
