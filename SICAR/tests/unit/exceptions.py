import unittest
from SICAR.exceptions import (
    UrlNotOkException,
    PolygonNotValidException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadPolygonException,
    FailedToGetReleaseDateException,
)


class ExceptionTestCase(unittest.TestCase):
    def test_url_not_ok_exception(self):
        url = "https://gilsonurbano.com"
        with self.assertRaises(UrlNotOkException) as context:
            raise UrlNotOkException(url)
        self.assertEqual(str(context.exception), f"Oh no! Failed to access {url}!")

    def test_state_code_not_valid_exception(self):
        state = "XYZ"
        with self.assertRaises(StateCodeNotValidException) as context:
            raise StateCodeNotValidException(state)
        self.assertEqual(str(context.exception), f"State code {state} not valid!")

    def test_polygon_not_valid_exception(self):
        state = "XYZ"
        with self.assertRaises(PolygonNotValidException) as context:
            raise PolygonNotValidException(state)
        self.assertEqual(str(context.exception), f"Polygon {state} not valid!")

    def test_failed_to_download_captcha_exception(self):
        with self.assertRaises(FailedToDownloadCaptchaException) as context:
            raise FailedToDownloadCaptchaException()
        self.assertEqual(str(context.exception), "Failed to download captcha!")

    def test_failed_to_download_polygon_exception(self):
        with self.assertRaises(FailedToDownloadPolygonException) as context:
            raise FailedToDownloadPolygonException()
        self.assertEqual(str(context.exception), "Failed to download polygon!")

    def test_failed_to_get_release_dates_exception(self):
        with self.assertRaises(FailedToGetReleaseDateException) as context:
            raise FailedToGetReleaseDateException()
        self.assertEqual(str(context.exception), "Failed to get release date!")
