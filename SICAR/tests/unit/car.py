import unittest
from unittest.mock import MagicMock, patch
from typing import Dict
import re
import requests
import random
import io
from PIL import Image
from pathlib import Path
from tqdm import tqdm
from urllib.parse import urlencode

from SICAR.sicar import Sicar
from SICAR.url import Url
from SICAR.exceptions import (
    EmailNotValidException,
    UrlNotOkException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadShapefileException,
)
from SICAR.drivers import Captcha
from SICAR.state import State


class MockCaptcha(Captcha):
    def get_captcha(self, captcha):
        return "mocked_captcha"


class SicarTestCase(unittest.TestCase):
    def setUp(self):
        self.mocked_captcha = MockCaptcha

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

    # @patch.object(Sicar, "_get")
    # @patch("builtins.open", new_callable=MagicMock)
    # @patch("pathlib.Path", new_callable=MagicMock)
    # @patch("tqdm.tqdm", new_callable=MagicMock)
    # def test_download_shapefile_success(
    #     self, mock_tqdm, mock_path, mock_open, mock_get
    # ):
    #     city_code = "123"
    #     captcha = "abc123"
    #     response_mock = MagicMock()
    #     response_mock.ok = True
    #     response_mock.headers.get.return_value = "filename.zip"
    #     response_mock.iter_content.return_value = [b"chunk1", b"chunk2"]
    #     response_mock.headers.get.return_value = 4096
    #     mock_get.return_value = response_mock
    #     shapefile_path = "shapefile/filename.zip"
    #     mock_path.return_value = MagicMock()
    #     mock_open.return_value.__enter__.return_value = MagicMock()

    #     sicar = Sicar(driver=self.mocked_captcha)
    #     result = sicar._download_shapefile(city_code, captcha)

    #     mock_get.assert_called_once_with(
    #         urlencode(
    #             "https://car.gov.br/publico/municipios/shapefile?municipio[id]=123&email=sicar@sicar.com&captcha=abc123"
    #         ),
    #         stream=True,
    #     )
    #     mock_path.assert_called_once_with(shapefile_path)
    #     mock_open.assert_called_once_with(mock_path.return_value, "wb")
    #     mock_tqdm.assert_called_once_with(
    #         iterable=response_mock.iter_content.return_value,
    #         total=float(response_mock.headers.get.return_value) / 2048,
    #         unit="KB",
    #         unit_scale=True,
    #         unit_divisor=1024,
    #         desc=f"Downloading shapefile city code '{city_code}'",
    #     )
    #     mock_open.return_value.__enter__.return_value.write.assert_called()
    #     self.assertIsNone(result)

    # @patch.object(Sicar, "_get")
    # def test_download_shapefile_failure(self, mock_get):
    #     city_code = "123"
    #     captcha = "abc123"
    #     response_mock = MagicMock()
    #     response_mock.ok = False
    #     mock_get.return_value = response_mock

    #     sicar = Sicar(driver=self.mocked_captcha)

    #     with self.assertRaises(FailedToDownloadShapefileException):
    #         sicar._download_shapefile(city_code, captcha)

    #     mock_get.assert_called_once_with(
    #         "https://car.gov.br/publico/municipios/shapefile?municipio[id]=123&email=sicar@sicar.com&captcha=abc123",
    #         stream=True,
    #     )


if __name__ == "__main__":
    unittest.main()
