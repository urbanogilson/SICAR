import unittest
from unittest.mock import MagicMock, patch, call
from typing import Dict
import re
import requests
import random
from urllib.parse import quote
import io
from PIL import Image
from pathlib import Path, PosixPath
from tqdm import tqdm
from urllib.parse import urlencode
import sys

from SICAR import Sicar
from SICAR import OutputFormat
from SICAR.url import Url
from SICAR.exceptions import (
    EmailNotValidException,
    UrlNotOkException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadShapefileException,
    FailedToDownloadCsvException,
)
from SICAR.drivers import Captcha
from SICAR import State


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
        Sicar(driver=self.mocked_captcha, email="valid@example.com")
        mock_get.assert_called_once_with("https://www.car.gov.br/publico/imoveis/index")
        self.mock_initialize_cookies.start()

    def test_create_sicar_instance_with_valid_email(self):
        sicar = Sicar(driver=self.mocked_captcha, email="valid@example.com")
        self.assertIsInstance(sicar, Sicar)
        self.assertEqual(sicar._email, "valid@example.com")

    def test_ocr_driver_integration(self):
        sicar = Sicar(driver=self.mocked_captcha, email="valid@example.com")
        captcha_image = Image.new("RGB", (10, 10))
        self.assertEqual(sicar._driver.get_captcha(captcha_image), "mocked_captcha")

    def test_create_sicar_instance_with_invalid_email(self):
        with self.assertRaises(EmailNotValidException):
            Sicar(driver=self.mocked_captcha, email="invalid_email")

    @patch("requests.Session")
    def test_create_session_with_custom_headers(self, mock_session):
        sicar = Sicar(driver=self.mocked_captcha, headers={"Custom-Header": "Value"})
        mock_session.assert_called_once()
        sicar._session.headers.update.assert_called_once_with(
            {"Custom-Header": "Value"}
        )

    @patch("requests.Session")
    def test_create_session_with_default_headers(self, mock_session):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_session.assert_called_once()
        sicar._session.headers.update.assert_called_once_with(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            }
        )

    def test_validate_email_with_valid_email(self):
        sicar = Sicar(driver=self.mocked_captcha)
        email = "valid@example.com"
        validated_email = sicar._validate_email(email)
        self.assertEqual(validated_email, email)

    def test_validate_email_with_invalid_email(self):
        sicar = Sicar(driver=self.mocked_captcha)
        invalid_email = "invalid_email"
        with self.assertRaises(EmailNotValidException):
            sicar._validate_email(invalid_email)

    def test_get_with_successful_response(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(return_value=MagicMock(ok=True))
        response = sicar._get("https://example.com")
        sicar._session.get.assert_called_once_with("https://example.com", verify=False)
        self.assertIsInstance(response, MagicMock)

    def test_get_with_unsuccessful_response(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(return_value=MagicMock(ok=False))
        with self.assertRaises(UrlNotOkException):
            sicar._get("https://example.com")

    def test_get_cities_codes_with_valid_state_enum(self):
        mock_response = MagicMock()
        mock_response.text = 'data-municipio="CityA"\ndata-municipio="123"\ndata-municipio="123"\ndata-municipio="CityB"\ndata-municipio="456"\ndata-municipio="456"\n'
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)

        cities_codes = sicar.get_cities_codes(State.AC)

        sicar._get.assert_called_once_with(
            "https://www.car.gov.br/publico/municipios/downloads?sigla=AC"
        )

        self.assertEqual(cities_codes, {"CityA": "123", "CityB": "456"})

    def test_get_cities_codes_with_valid_state_string(self):
        mock_response = MagicMock()
        mock_response.text = 'data-municipio="CityA"\ndata-municipio="123"\ndata-municipio="123"\ndata-municipio="CityB"\ndata-municipio="456"\ndata-municipio="456"\n'
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)

        cities_codes = sicar.get_cities_codes("AC")

        sicar._get.assert_called_once_with(
            "https://www.car.gov.br/publico/municipios/downloads?sigla=AC"
        )

        self.assertEqual(cities_codes, {"CityA": "123", "CityB": "456"})

    def test_get_cities_codes_with_invalid_state_code(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(side_effect=UrlNotOkException)

        with self.assertRaises(StateCodeNotValidException):
            sicar.get_cities_codes("INVALID")

        sicar._get.assert_not_called()

    @patch("random.random", lambda: 0.1)
    def test_download_captcha_success(self):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.content = b"mocked_image_data"
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)
        mock_image = MagicMock(spec=Image.Image)
        Image.open = MagicMock(return_value=mock_image)

        captcha_image = sicar._download_captcha()

        sicar._get.assert_called_once_with(
            f"https://www.car.gov.br/publico/municipios/captcha?id={int(random.random() * 1000000)}"
        )
        Image.open.assert_called_once()
        self.assertEqual(captcha_image, mock_image)

    @patch("random.random", lambda: 0.1)
    def test_download_captcha_invalid_image(self):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.content = b"invalid_captcha_image"
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)

        with self.assertRaises(FailedToDownloadCaptchaException):
            sicar._download_captcha()

        sicar._get.assert_called_once()

    def test_download_captcha_failure(self):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=MagicMock(ok=False))

        with self.assertRaises(FailedToDownloadCaptchaException):
            sicar._download_captcha()

        sicar._get.assert_called_once()

    @patch.object(Sicar, "_get")
    @patch("builtins.open", new_callable=MagicMock)
    @patch.object(Path, "__init__", return_value=None)
    @patch("tqdm.tqdm", side_effect=lambda *args, **kwargs: MagicMock())
    def test_download_shapefile_success(
        self, mock_tqdm, mock_path, mock_open, mock_get
    ):
        city_code = "123"
        captcha = "abc123"
        folder = "shapefiles"
        response_mock = MagicMock()
        response_mock.ok = True
        response_mock.headers.return_value = {
            "Content-Type": "application/zip",
            "Content-Length": 4096,
        }
        response_mock.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_get.return_value = response_mock
        mock_open.return_value.__enter__.return_value = MagicMock()
        sicar = Sicar(driver=self.mocked_captcha)
        result = sicar._download_shapefile(city_code, captcha, folder)
        mock_get.assert_called_once_with(
            r"https://www.car.gov.br/publico/municipios/shapefile?municipio%5Bid%5D=123&email=sicar%40sicar.com&captcha=abc123",
            stream=True,
        )
        mock_path.assert_called_once_with(f"{folder}/SHAPE_{city_code}")
        mock_open.assert_called_once_with(
            PosixPath(f"{folder}/SHAPE_{city_code}.zip"), "wb"
        )
        mock_open.return_value.__enter__.return_value.write.assert_called()
        self.assertEqual(result, PosixPath(f"{folder}/SHAPE_{city_code}.zip"))

    def test_download_shapefile_failed_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "shapefiles"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(return_value=MagicMock(ok=False))

        with self.assertRaises(FailedToDownloadShapefileException):
            sicar._download_shapefile(city_code, captcha, folder, chunk_size)

    def test_download_shapefile_html_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "shapefiles"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(
            return_value=MagicMock(ok=True, headers={"Content-Type": "text/html"})
        )

        with self.assertRaises(FailedToDownloadShapefileException):
            sicar._download_shapefile(city_code, captcha, folder, chunk_size)

    @patch.object(Sicar, "_get")
    @patch("builtins.open", new_callable=MagicMock)
    @patch.object(Path, "__init__", return_value=None)
    @patch("tqdm.tqdm", side_effect=lambda *args, **kwargs: MagicMock())
    def test_download_csv_success(self, mock_tqdm, mock_path, mock_open, mock_get):
        city_code = "123"
        captcha = "abc123"
        folder = "csvs"
        response_mock = MagicMock()
        response_mock.ok = True
        response_mock.headers.return_value = {
            "Content-Type": "text/csv",
            "Content-Length": 4096,
        }
        response_mock.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_get.return_value = response_mock
        mock_open.return_value.__enter__.return_value = MagicMock()
        sicar = Sicar(driver=self.mocked_captcha)
        result = sicar._download_csv(city_code, captcha, folder)
        mock_get.assert_called_once_with(
            r"https://www.car.gov.br/publico/municipios/csv?municipio%5Bid%5D=123&email=sicar%40sicar.com&captcha=abc123",
            stream=True,
        )
        mock_path.assert_called_once_with(f"{folder}/CSV_{city_code}")
        mock_open.assert_called_once_with(
            PosixPath(f"{folder}/CSV_{city_code}.csv"), "wb"
        )
        mock_open.return_value.__enter__.return_value.write.assert_called()
        self.assertEqual(result, PosixPath(f"{folder}/CSV_{city_code}.csv"))

    def test_download_csv_failed_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "csvs"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(return_value=MagicMock(ok=False))

        with self.assertRaises(FailedToDownloadCsvException):
            sicar._download_csv(city_code, captcha, folder, chunk_size)

    def test_download_csv_html_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "csvs"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._session.get = MagicMock(
            return_value=MagicMock(ok=True, headers={"Content-Type": "text/html"})
        )

        with self.assertRaises(FailedToDownloadCsvException):
            sicar._download_csv(city_code, captcha, folder, chunk_size)

    @patch("pathlib.Path.mkdir")
    def test_download_city_code_valid_captcha(self, mock_mkdir):
        # Mock city code, tries, output format, folder, and chunk size
        city_code = "12345"
        tries = 25
        output_format = OutputFormat.SHAPEFILE
        folder = "temp"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_shapefile = MagicMock(return_value=Path("shapefile.zip"))
        sicar._download_shapefile = mock_download_shapefile

        result = sicar.download_city_code(
            city_code, output_format, folder, tries, debug=False, chunk_size=chunk_size
        )

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_download_captcha.assert_called_once()

        mock_get_captcha.assert_called_once_with(mock_download_captcha.return_value)

        mock_download_shapefile.assert_called_once_with(
            city_code=city_code, captcha="ABCDE", folder=folder, chunk_size=chunk_size
        )

        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path("shapefile.zip"))

    @patch("pathlib.Path.mkdir")
    def test_download_city_code_valid_captcha_csv_format(self, mock_mkdir):
        # Mock city code, tries, output format, folder, and chunk size
        city_code = "12345"
        tries = 25
        output_format = OutputFormat.CSV
        folder = "temp"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_csv = MagicMock(return_value=Path("shapefile.csv"))
        sicar._download_csv = mock_download_csv

        result = sicar.download_city_code(
            city_code, output_format, folder, tries, debug=False, chunk_size=chunk_size
        )

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_download_captcha.assert_called_once()

        mock_get_captcha.assert_called_once_with(mock_download_captcha.return_value)

        mock_download_csv.assert_called_once_with(
            city_code=city_code, captcha="ABCDE", folder=folder, chunk_size=chunk_size
        )

        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path("shapefile.csv"))

    @patch("pathlib.Path.mkdir")
    @patch("time.sleep", return_value=None)
    def test_download_city_code_invalid_captcha(self, mock_time, mock_mkdir):
        # Mock city code, tries, output format, folder, and chunk size
        city_code = "12345"
        tries = 25
        output_format = OutputFormat.SHAPEFILE
        folder = "temp"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCD")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_shapefile = MagicMock(return_value=Path("shapefile.zip"))
        sicar._download_shapefile = mock_download_shapefile

        result = sicar.download_city_code(
            city_code, output_format, folder, tries, debug=False, chunk_size=chunk_size
        )

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        self.assertEqual(mock_download_captcha.call_count, tries)
        self.assertEqual(mock_get_captcha.call_count, tries)
        mock_get_captcha.assert_called_with(mock_download_captcha.return_value)

        mock_download_shapefile.assert_not_called()

        self.assertFalse(result)

    @patch("time.sleep", return_value=None)
    def test_download_city_code_invalid_captcha_failed_to_download_captcha_exception(
        self, mock_time
    ):
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=MagicMock(ok=False))
        sicar.download_city_code(
            "12345", OutputFormat.SHAPEFILE, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("time.sleep", return_value=None)
    def test_download_city_code_invalid_captcha_failed_to_download_shapefile_exception(
        self, mock_time
    ):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_shapefile = MagicMock()
        mock_download_shapefile.side_effect = FailedToDownloadShapefileException()
        sicar._download_shapefile = mock_download_shapefile

        sicar.download_city_code(
            "12345", OutputFormat.SHAPEFILE, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("time.sleep", return_value=None)
    def test_download_city_code_invalid_captcha_failed_to_download_csv_exception(
        self, mock_time
    ):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="ABCDE")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_csv = MagicMock()
        mock_download_csv.side_effect = FailedToDownloadCsvException()
        sicar._download_csv = mock_download_csv

        sicar.download_city_code(
            "12345", OutputFormat.CSV, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("time.sleep", return_value=None)
    def test_download_city_code_invalid_captcha_debug(self, mock_time):
        sicar = Sicar(driver=self.mocked_captcha)
        mock_download_captcha = MagicMock(return_value=Image.Image)
        sicar._download_captcha = mock_download_captcha

        mock_get_captcha = MagicMock(return_value="invalid")
        sicar._driver.get_captcha = mock_get_captcha

        mock_download_shapefile = MagicMock(return_value=Path("shapefile.zip"))
        sicar._download_shapefile = mock_download_shapefile

        sicar.download_city_code(
            "12345", OutputFormat.SHAPEFILE, "temp", 25, chunk_size=1024, debug=True
        )

    @patch("SICAR.sicar.Sicar.download_city_code")
    def test_download_cities_success(self, mock_download_city_code):
        cities_codes = {"City1": "123", "City2": "456"}
        tries = 25
        output_format = OutputFormat.SHAPEFILE
        folder = "temp"
        chunk_size = 1024
        debug = False
        mock_download_city_code.side_effect = (
            lambda city_code, output_format, folder, tries, debug, chunk_size: Path(
                f"{city_code}.zip"
            )
        )

        sicar = Sicar(driver=self.mocked_captcha)

        result = sicar.download_cities(
            cities_codes,
            output_format,
            folder,
            tries,
            debug=debug,
            chunk_size=chunk_size,
        )

        expected_result = {
            ("City1", "123"): Path("123.zip"),
            ("City2", "456"): Path("456.zip"),
        }
        self.assertEqual(result, expected_result)

        expected_calls = [
            call(
                city_code="123",
                output_format=output_format,
                folder=folder,
                tries=tries,
                debug=debug,
                chunk_size=chunk_size,
            ),
            call(
                city_code="456",
                output_format=output_format,
                folder=folder,
                tries=tries,
                debug=debug,
                chunk_size=chunk_size,
            ),
        ]
        mock_download_city_code.assert_has_calls(expected_calls)

    @patch("SICAR.sicar.Sicar.get_cities_codes")
    @patch("SICAR.sicar.Sicar.download_cities")
    def test_download_state(self, mock_download_cities, mock_get_cities_codes):
        sicar = Sicar(driver=self.mocked_captcha)
        state = State.MG
        output_format = OutputFormat.SHAPEFILE
        folder = "/path/to/folder"
        tries = 25
        debug = False
        chunk_size = 1024

        mock_get_cities_codes.return_value = {"City1": "123", "City2": "456"}

        mock_download_cities.return_value = {
            ("City1", "123"): Path("123.zip"),
            ("City2", "456"): Path("456.zip"),
        }

        result = sicar.download_state(
            state, output_format, folder, tries, debug, chunk_size
        )

        self.assertEqual(
            result,
            {("City1", "123"): Path("123.zip"), ("City2", "456"): Path("456.zip")},
        )

        mock_get_cities_codes.assert_called_once_with(state=state)

        expected_calls = [
            call(
                cities_codes={"City1": "123", "City2": "456"},
                output_format=output_format,
                folder=folder,
                tries=tries,
                debug=debug,
                chunk_size=chunk_size,
            )
        ]
        mock_download_cities.assert_has_calls(expected_calls)

    @patch("SICAR.sicar.Sicar.download_state")
    @patch("pathlib.Path.mkdir")
    def test_download_country(self, mock_mkdir, mock_download_state):
        sicar = Sicar(driver=self.mocked_captcha)
        output_format = OutputFormat.SHAPEFILE
        folder = "/path/to/folder"
        tries = 25
        debug = False
        chunk_size = 1024

        mock_download_state.return_value = {
            ("City1", "123"): Path("/path/to/123.zip"),
            ("City2", "456"): Path("/path/to/456.zip"),
        }

        sicar.download_country(output_format, folder, tries, debug, chunk_size)

        expected_calls = {"path": [], "download_state": []}
        for state in State:
            expected_calls["path"].append(call(parents=True, exist_ok=True))
            expected_calls["download_state"].append(
                call(
                    state=state,
                    output_format=output_format,
                    folder=folder,
                    tries=tries,
                    debug=debug,
                    chunk_size=chunk_size,
                )
            )

        mock_mkdir.assert_has_calls(expected_calls["path"])
        mock_download_state.assert_has_calls(expected_calls["download_state"])
