import unittest
from unittest.mock import MagicMock, patch, call
import random
import io
import httpx
from PIL import Image
from pathlib import Path, PosixPath
import sys

from SICAR import Sicar
from SICAR.state import State
from SICAR.polygon import Polygon
from SICAR.drivers import Captcha
from SICAR.exceptions import (
    PolygonNotValidException,
    UrlNotOkException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadPolygonException,
)


class MockCaptcha(Captcha):
    def get_captcha(self, captcha):
        return "mocked_captcha"


class SicarTestCase(unittest.TestCase):
    def setUp(self):
        self.mocked_captcha = MockCaptcha
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        self.mock_initialize_cookies = patch("SICAR.sicar.Sicar._initialize_cookies")
        self.mock_initialize_cookies.start()

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.mock_initialize_cookies.stop()

    @patch.object(Sicar, "_get")
    def test_initialize_cookies(self, mock_get):
        self.mock_initialize_cookies.stop()
        Sicar(driver=self.mocked_captcha)
        mock_get.assert_called_once_with("https://www.car.gov.br/publico/imoveis/index")
        self.mock_initialize_cookies.start()

    def test_ocr_driver_integration(self):
        sicar = Sicar(driver=self.mocked_captcha)
        captcha_image = Image.new("RGB", (10, 10))
        self.assertEqual(sicar._driver.get_captcha(captcha_image), "mocked_captcha")

    @patch("httpx.Client")
    def test_create_session_with_ssl_disabled(self, mock_session):
        Sicar(driver=self.mocked_captcha)
        mock_session.assert_called_once_with(verify=False)

    @patch("httpx.Client")
    def test_create_session_with_custom_headers(self, mock_session):
        sicar = Sicar(driver=self.mocked_captcha, headers={"Custom-Header": "Value"})
        mock_session.assert_called_once()
        sicar._session.headers.update.assert_called_once_with(
            {"Custom-Header": "Value"}
        )

    @patch("httpx.Client")
    def test_create_session_with_default_headers(self, mock_session):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_session.assert_called_once()
        sicar._session.headers.update.assert_called_once_with(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            }
        )

    def test_get_with_successful_response(self):
        with patch.object(httpx.Client, "get") as stream_mock:
            stream_mock.return_value = MagicMock(status_code=httpx.codes.OK)
            sicar = Sicar(driver=self.mocked_captcha)
            response = sicar._get("https://example.com")
            sicar._session.get.assert_called_once_with(url="https://example.com")
            self.assertIsInstance(response, MagicMock)

    def test_get_with_unsuccessful_response(self):
        sicar = Sicar(driver=self.mocked_captcha)
        with patch.object(httpx.Client, "get") as stream_mock:
            stream_mock.return_value = MagicMock(status_code=httpx.codes.NOT_FOUND)
            with self.assertRaises(UrlNotOkException):
                sicar._get("https://example.com")

    @patch("random.random", lambda: 0.1)
    def test_download_captcha_success(self):
        mock_response = MagicMock(
            status_code=httpx.codes.OK, content=b"mocked_image_data"
        )
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)
        mock_image = MagicMock(spec=Image.Image)
        Image.open = MagicMock(return_value=mock_image)

        captcha_image = sicar._download_captcha()

        sicar._get.assert_called_once_with(
            f"https://consultapublica.car.gov.br/publico/municipios/ReCaptcha?id={int(random.random() * 1000000)}"
        )
        Image.open.assert_called_once()
        self.assertEqual(captcha_image, mock_image)

    @patch("random.random", lambda: 0.1)
    def test_download_captcha_invalid_image(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(
            return_value=MagicMock(
                status_code=httpx.codes.OK, content=b"invalid_captcha_image"
            )
        )

        with self.assertRaises(FailedToDownloadCaptchaException):
            sicar._download_captcha()

        sicar._get.assert_called_once()

    def test_download_captcha_failure(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(
            return_value=MagicMock(status_code=httpx.codes.NOT_FOUND)
        )

        with self.assertRaises(FailedToDownloadCaptchaException):
            sicar._download_captcha()

        sicar._get.assert_called_once()

    @patch("builtins.open", new_callable=MagicMock)
    @patch.object(Path, "__init__", return_value=None)
    @patch("tqdm.tqdm", side_effect=lambda *args, **kwargs: MagicMock())
    def test_download_polygon_success(self, mock_tqdm, mock_path, mock_open):
        state = State.MG
        polygon = Polygon.APPS
        captcha = "abc123"
        folder = "polygons"
        response_mock = MagicMock()
        response_mock.status_code = httpx.codes.OK
        response_mock.headers = {
            "Content-Type": "application/zip",
            "Content-Length": 4096,
        }

        response_mock.iter_bytes = lambda: (
            (yield b"chunk1"),
            (yield b"chunk2"),
        )

        with patch.object(httpx.Client, "stream") as stream_mock:
            stream_mock.return_value.__enter__.return_value = response_mock
            sicar = Sicar(driver=self.mocked_captcha)
            result = sicar._download_polygon(state, polygon, captcha, folder)

        stream_mock.assert_called_once_with(
            "GET",
            r"https://consultapublica.car.gov.br/publico/estados/downloadBase?idEstado=MG&tipoBase=APPS&ReCaptcha=abc123",
        )
        mock_path.assert_called_once_with(f"{folder}/{state}_{polygon.value}")
        mock_open.assert_called_once_with(
            PosixPath(f"{folder}/{state}_{polygon.value}.zip"), "wb"
        )
        mock_open.return_value.__enter__.return_value.write.assert_called()
        self.assertEqual(result, PosixPath(f"{folder}/{state}_{polygon.value}.zip"))

    def test_download_polygon_failed_response(self):
        with patch.object(httpx.Client, "stream") as stream_mock:
            stream_mock.return_value.__enter__.return_value = MagicMock(
                status_code=httpx.codes.NOT_FOUND
            )

            sicar = Sicar(driver=self.mocked_captcha)

            with self.assertRaises(FailedToDownloadPolygonException):
                sicar._download_polygon(
                    state=State.MG,
                    polygon=Polygon.APPS,
                    captcha="abc123",
                    folder="polygons",
                    chunk_size=1024,
                )

    def test_download_polygon_fails_on_html_response(self):
        state = State.MG
        polygon = Polygon.APPS
        captcha = "abc123"
        folder = "polygons"
        chunk_size = 1024

        with patch.object(httpx.Client, "stream") as stream_mock:
            stream_mock.return_value.__enter__.return_value = MagicMock(
                status_code=httpx.codes.OK, headers={"Content-Type": "text/html"}
            )

            sicar = Sicar(driver=self.mocked_captcha)

            with self.assertRaises(FailedToDownloadPolygonException):
                sicar._download_polygon(state, polygon, captcha, folder, chunk_size)

    @patch("pathlib.Path.mkdir")
    def test_download_state_valid_captcha(self, mock_mkdir):
        state = State.MG
        polygon = Polygon.APPS
        tries = 25
        folder = "temp"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_polygon = MagicMock(return_value=Path("polygon.zip"))
        sicar._download_polygon = mock_download_polygon

        result = sicar.download_state(
            state, polygon, folder, tries, debug=False, chunk_size=chunk_size
        )

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_download_captcha.assert_called_once()

        mock_get_captcha.assert_called_once_with(mock_download_captcha.return_value)

        mock_download_polygon.assert_called_once_with(
            state=state,
            polygon=polygon,
            captcha="ABCDE",
            folder=folder,
            chunk_size=chunk_size,
        )

        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path("polygon.zip"))

    @patch("pathlib.Path.mkdir")
    @patch("time.sleep", return_value=None)
    def test_download_polygon_invalid_captcha(self, mock_time, mock_mkdir):
        state = State.MG
        polygon = Polygon.APPS
        tries = 25
        folder = "temp"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCD")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_polygon = MagicMock(return_value=Path("polygon.zip"))
        sicar._download_polygon = mock_download_polygon

        result = sicar.download_state(
            state, polygon, folder, tries, debug=False, chunk_size=chunk_size
        )

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        self.assertEqual(mock_download_captcha.call_count, tries)
        self.assertEqual(mock_get_captcha.call_count, tries)
        mock_get_captcha.assert_called_with(mock_download_captcha.return_value)

        mock_download_polygon.assert_not_called()

        self.assertFalse(result)

    @patch("time.sleep", return_value=None)
    def test_download_polygon_invalid_captcha_failed_to_download_captcha_exception(
        self, mock_time
    ):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(
            return_value=MagicMock(status_code=httpx.codes.NOT_FOUND)
        )
        sicar.download_state(
            State.MG, Polygon.APPS, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("time.sleep", return_value=None)
    def test_download_polygon_invalid_captcha_failed_to_download_polygon_exception(
        self, mock_time
    ):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_polygon = MagicMock()
        mock_download_polygon.side_effect = FailedToDownloadPolygonException()
        sicar._download_polygon = mock_download_polygon

        sicar.download_state(
            State.MG, Polygon.APPS, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("time.sleep", return_value=None)
    def test_download_state_invalid_captcha_debug(self, mock_time):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="invalid")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_polygon = MagicMock(return_value=Path("polygon.zip"))
        sicar._download_polygon = mock_download_polygon

        sicar.download_state(
            State.MG, Polygon.APPS, "temp", 25, chunk_size=1024, debug=True
        )

    def test_download_state_invalid_state_code(self):
        sicar = Sicar(driver=self.mocked_captcha)
        with self.assertRaises(StateCodeNotValidException):
            sicar.download_state(
                "INVALID_STATE", Polygon.APPS, "temp", 25, chunk_size=1024, debug=True
            )

    def test_download_state_invalid_polygon_code(self):
        sicar = Sicar(driver=self.mocked_captcha)
        with self.assertRaises(PolygonNotValidException):
            sicar.download_state(
                State.MG, "INVALID_POLYGON", "temp", 25, chunk_size=1024, debug=True
            )

    @patch("SICAR.sicar.Sicar.download_state")
    @patch("pathlib.Path.mkdir")
    def test_download_country(self, mock_mkdir, mock_download_state):
        sicar = Sicar(driver=self.mocked_captcha)
        state = State.MG
        polygon = Polygon.APPS
        tries = 25
        debug = False
        folder = "/path/to/folder"
        chunk_size = 1024

        mock_download_state.return_value = {
            "State1": Path("/path/to/123.zip"),
            "State2": Path("/path/to/456.zip"),
        }

        sicar.download_country(polygon, folder, tries, debug, chunk_size)

        expected_calls = {"path": [], "download_state": []}
        for state in State:
            expected_calls["path"].append(call(parents=True, exist_ok=True))
            expected_calls["download_state"].append(
                call(
                    state=state,
                    polygon=polygon,
                    folder=folder,
                    tries=tries,
                    debug=debug,
                    chunk_size=chunk_size,
                )
            )

        mock_mkdir.assert_has_calls(expected_calls["path"])
        mock_download_state.assert_has_calls(expected_calls["download_state"])
