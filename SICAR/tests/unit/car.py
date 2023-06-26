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

from SICAR.sicar import Sicar
from SICAR.output_format import OutputFormat
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
from SICAR.state import State


class MockCaptcha(Captcha):
    def get_captcha(self, captcha):
        return "mocked_captcha"


class SicarTestCase(unittest.TestCase):
    def setUp(self):
        self.mocked_captcha = MockCaptcha
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_create_sicar_instance_with_valid_email(self):
        sicar = Sicar(driver=self.mocked_captcha, email="valid@example.com")
        self.assertIsInstance(sicar, Sicar)
        self.assertEqual(sicar._email, "valid@example.com")

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
            "https://car.gov.br/publico/municipios/downloads?sigla=AC"
        )

        self.assertEqual(cities_codes, {"CityA": "123", "CityB": "456"})

    def test_get_cities_codes_with_valid_state_string(self):
        mock_response = MagicMock()
        mock_response.text = 'data-municipio="CityA"\ndata-municipio="123"\ndata-municipio="123"\ndata-municipio="CityB"\ndata-municipio="456"\ndata-municipio="456"\n'
        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=mock_response)

        cities_codes = sicar.get_cities_codes("AC")

        sicar._get.assert_called_once_with(
            "https://car.gov.br/publico/municipios/downloads?sigla=AC"
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
            f"https://car.gov.br/publico/municipios/captcha?id={int(random.random() * 1000000)}",
            stream=True,
        )
        Image.open.assert_called_once()
        self.assertEqual(captcha_image, mock_image)

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
        response_mock.headers.get.return_value = "filename.zip"
        response_mock.iter_content.return_value = [b"chunk1", b"chunk2"]
        response_mock.headers.get.return_value = 4096
        mock_get.return_value = response_mock
        mock_open.return_value.__enter__.return_value = MagicMock()
        sicar = Sicar(driver=self.mocked_captcha)
        result = sicar._download_shapefile(city_code, captcha, folder)
        mock_get.assert_called_once_with(
            r"https://car.gov.br/publico/municipios/shapefile?municipio%5Bid%5D=123&email=sicar%40sicar.com&captcha=abc123",
            stream=True,
        )
        mock_path.assert_called_once_with(f"{folder}/SHAPE_{city_code}")
        mock_open.assert_called_once_with(
            PosixPath(f"{folder}/SHAPE_{city_code}.zip"), "wb"
        )
        mock_open.return_value.__enter__.return_value.write.assert_called()
        self.assertEqual(result, Path)

    def test_download_shapefile_failed_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "shapefiles"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=MagicMock(ok=False))

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
        response_mock.headers.get.return_value = "filename.zip"
        response_mock.iter_content.return_value = [b"chunk1", b"chunk2"]
        response_mock.headers.get.return_value = 4096
        mock_get.return_value = response_mock
        mock_open.return_value.__enter__.return_value = MagicMock()
        sicar = Sicar(driver=self.mocked_captcha)
        result = sicar._download_csv(city_code, captcha, folder)
        mock_get.assert_called_once_with(
            r"https://car.gov.br/publico/municipios/csv?municipio%5Bid%5D=123&email=sicar%40sicar.com&captcha=abc123",
            stream=True,
        )
        mock_path.assert_called_once_with(f"{folder}/CSV_{city_code}")
        mock_open.assert_called_once_with(
            PosixPath(f"{folder}/CSV_{city_code}.csv"), "wb"
        )
        mock_open.return_value.__enter__.return_value.write.assert_called()
        self.assertEqual(result, Path)

    def test_download_csv_failed_response(self):
        city_code = "12345"
        captcha = "captcha_code"
        folder = "csvs"
        chunk_size = 1024

        sicar = Sicar(driver=self.mocked_captcha)
        sicar._get = MagicMock(return_value=MagicMock(ok=False))

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
