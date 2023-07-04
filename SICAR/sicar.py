"""
SICAR Class Module.

This module defines a class representing the Sicar system for managing environmental rural properties in Brazil.

Classes:
    Sicar: Class representing the Sicar system.
"""

import io
import os
import re
import time
import random
import requests
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm
from typing import Dict
from pathlib import Path
from html import unescape
from urllib.parse import urlencode

from SICAR.drivers import Captcha, Tesseract
from SICAR.output_format import OutputFormat
from SICAR.state import State
from SICAR.url import Url
from SICAR.exceptions import (
    EmailNotValidException,
    UrlNotOkException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadShapefileException,
    FailedToDownloadCsvException,
)

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Sicar(Url):
    """
    Class representing the Sicar system.

    Sicar is a system for managing environmental rural properties in Brazil.

    It inherits from the Url class to provide access to URLs related to the Sicar system.

    Attributes:
        _driver (Captcha): The driver used for handling captchas. Default is Tesseract.
        _email (str): The personal email for communication or identification purposes.
    """

    def __init__(
        self,
        driver: Captcha = Tesseract,
        email: str = "sicar@sicar.com",
        headers: Dict = None,
    ):
        """
        Initialize an instance of the Sicar class.

        Parameters:
            driver (Captcha): The driver used for handling captchas. Default is Tesseract.
            email (str): The personal email for communication or identification purposes. Default is "sicar@sicar.com".
            headers (Dict): Additional headers for HTTP requests. Default is None.

        Returns:
            None
        """
        self._driver = driver()
        self._email = self._validate_email(email)
        self._create_session(headers=headers)
        self._initialize_cookies()

    def _create_session(self, headers: Dict = None):
        """
        Create a new session for making HTTP requests.

        Parameters:
            headers (Dict): Additional headers for the session. Default is None.

        Returns:
            None
        """
        self._session = requests.Session()
        self._session.headers.update(
            headers
            if isinstance(headers, dict)
            else {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            }
        )

    def _initialize_cookies(self):
        """
        Initialize cookies by making the initial request and accepting any redirections.

        This method is intended to be called in the constructor to set up the session cookies.

        Returns:
            None
        """
        self._get(self._INDEX)

    def _validate_email(self, email: str) -> str:
        """
        Validate the format of an email address.

        Parameters:
            email (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            EmailNotValidException: If the email address format is not valid.
        """
        if not re.search(
            r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$", email
        ):
            raise EmailNotValidException(email)

        return email

    def _get(self, url: str, *args, **kwargs):
        """
        Send a GET request to the specified URL using the session.

        Parameters:
            url (str): The URL to send the GET request to.
            *args: Variable-length positional arguments.
            **kwargs: Variable-length keyword arguments.

        Returns:
            requests.Response: The response from the GET request.

        Raises:
            UrlNotOkException: If the response from the GET request is not OK (status code is not 200).

        Note:
            The SSL certificate verification is disabled by default using `verify=False`. This allows connections to servers
            with self-signed or invalid certificates. Disabling SSL certificate verification can expose your application to
            security risks, such as man-in-the-middle attacks. If the server has a valid SSL certificate issued by a trusted
            certificate authority, you can remove the `verify=False` parameter to enable SSL certificate verification by
            default.
        """
        response = self._session.get(url, verify=False, *args, **kwargs)

        if not response.ok:
            raise UrlNotOkException(url)

        return response

    def get_cities_codes(self, state: State | str) -> Dict:
        """
        Retrieve the codes of cities in a given state.

        Parameters:
            state (Union[State, str]): The state or state code to retrieve the cities for.

        Returns:
            Dict: A dictionary mapping city names to their corresponding codes.

        Raises:
            StateCodeNotValidException: If the state code is not valid.

        Note:
            If `state` is provided as a string, it will be converted to the corresponding State enum value. The state code
            must be valid, or a StateCodeNotValidException will be raised.
        """
        if isinstance(state, str):
            try:
                state = State(state.upper())
            except ValueError as error:
                raise StateCodeNotValidException(state) from error

        cities_codes = re.findall(
            r'(?<=data-municipio=")(.*)(?=")',
            self._get(
                "{}?{}".format(self._DOWNLOADS, urlencode({"sigla": state.value}))
            ).text,
        )

        return dict(zip(list(map(unescape, cities_codes[0::3])), cities_codes[1::3]))

    def _download_captcha(self) -> Image:
        """
        Download a captcha image from the SICAR system.

        Returns:
            Image: The captcha image.

        Raises:
            FailedToDownloadCaptchaException: If the captcha image fails to download.
        """
        url = f"{self._CAPTCHA}?{urlencode({'id': int(random.random() * 1000000)})}"
        response = self._get(url)

        if not response.ok:
            raise FailedToDownloadCaptchaException()

        try:
            captcha = Image.open(io.BytesIO(response.content))
        except UnidentifiedImageError as error:
            raise FailedToDownloadCaptchaException() from error

        return captcha

    def _download_shapefile(
        self,
        city_code: str | int,
        captcha: str,
        folder: str,
        chunk_size: int = 1024,
    ) -> Path:
        """
        Download the shapefile for the specified city code.

        Parameters:
            city_code (str | int): The code of the city for which to download the shapefile.
            captcha (str): The captcha value for verification.
            folder (str): The folder path where the shapefile will be saved.
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.

        Returns:
            Path: The path to the downloaded shapefile.

        Raises:
            FailedToDownloadShapefileException: If the shapefile download fails.

        Note:
            This method performs the shapefile download by making a GET request to the shapefile URL with the specified
            city code and captcha. The response is then streamed and saved to a file in chunks. A progress bar is displayed
            during the download. The downloaded file path is returned.
        """
        query = urlencode(
            {"municipio[id]": city_code, "email": self._email, "captcha": captcha}
        )

        try:
            response = self._get(f"{self._SHAPEFILE}?{query}", stream=True)
        except UrlNotOkException as error:
            raise FailedToDownloadShapefileException() from error

        content_length = int(response.headers.get("Content-Length", 0))

        content_type = response.headers.get("Content-Type", "")

        if content_length == 0 or not content_type.startswith("application/zip"):
            raise FailedToDownloadShapefileException()

        path = Path(os.path.join(folder, f"SHAPE_{city_code}")).with_suffix(".zip")

        with open(path, "wb") as fd:
            with tqdm(
                total=content_length,
                unit="iB",
                unit_scale=True,
                desc=f"Downloading Shapefile for city with code '{city_code}'",
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    progress_bar.update(len(chunk))
        return path

    def _download_csv(
        self,
        city_code: str | int,
        captcha: str,
        folder: str,
        chunk_size: int = 1024,
    ) -> Path:
        """
        Download the CSV file for the specified city code.

        Parameters:
            city_code (str | int): The code of the city for which to download the CSV file.
            captcha (str): The captcha value for verification.
            folder (str): The folder path where the downloaded CSV file will be saved.
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.

        Returns:
            Path: The path to the downloaded CSV file.

        Raises:
            FailedToDownloadCsvException: If the CSV file fails to download.

        Note:
            This method downloads the CSV file for the specified city code, using the provided captcha for verification.
            The downloaded CSV file is saved to the specified folder.
            The method returns the path to the downloaded CSV file.
        """
        query = urlencode(
            {"municipio[id]": city_code, "email": self._email, "captcha": captcha}
        )

        try:
            response = self._get(f"{self._CSV}?{query}", stream=True)
        except UrlNotOkException as error:
            raise FailedToDownloadCsvException() from error

        content_length = int(response.headers.get("Content-Length", 0))

        content_type = response.headers.get("Content-Type", "")

        if content_length == 0 or not content_type.startswith("text/csv"):
            raise FailedToDownloadCsvException()

        path = Path(os.path.join(folder, f"CSV_{city_code}")).with_suffix(".csv")

        with open(path, "wb") as fd:
            with tqdm(
                total=content_length,
                unit="iB",
                unit_scale=True,
                desc=f"Downloading CSV  file for city with code '{city_code}'",
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    progress_bar.update(len(chunk))
        return path

    def download_city_code(
        self,
        city_code: str | int,
        output_format: OutputFormat = OutputFormat.SHAPEFILE,
        folder: Path | str = Path("temp"),
        tries: int = 25,
        debug: bool = False,
        chunk_size: int = 1024,
    ) -> Path | bool:
        """
        Download the shapefile or other output format for the specified city code.

        Parameters:
            city_code (str | int): The code of the city for which to download the data.
            tries (int, optional): The number of attempts to download the data. Defaults to 25.
            output_format (OutputFormat, optional): The desired output format. Defaults to OutputFormat.SHAPEFILE.
            folder (Path | str, optional): The folder path where the downloaded data will be saved. Defaults to "temp".
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.
            debug (bool, optional): Whether to print debug information. Defaults to False.

        Returns:
            Path | bool: The path to the downloaded data if successful, or False if download fails.

        Note:
            This method attempts to download the shapefile or other output format for the specified city code.
            It tries multiple times, using a captcha for verification. The downloaded data is saved to the specified folder.
            The method returns the path to the downloaded data if successful, or False if the download fails after the specified number of tries.
        """
        Path(folder).mkdir(parents=True, exist_ok=True)

        captcha = ""
        info = f"city '{city_code}' in '{output_format}' format"

        while tries > 0:
            try:
                captcha = self._driver.get_captcha(self._download_captcha())

                if len(captcha) == 5:
                    if debug:
                        print(
                            f"[{tries:02d}] - Requesting {info} with captcha '{captcha}'"
                        )

                    if output_format is OutputFormat.CSV:
                        return self._download_csv(
                            city_code=city_code,
                            captcha=captcha,
                            folder=folder,
                            chunk_size=chunk_size,
                        )

                    return self._download_shapefile(
                        city_code=city_code,
                        captcha=captcha,
                        folder=folder,
                        chunk_size=chunk_size,
                    )
                elif debug:
                    print(
                        f"[{tries:02d}] - Invalid captcha '{captcha}' to request {info}"
                    )
            except (
                FailedToDownloadCaptchaException,
                FailedToDownloadShapefileException,
                FailedToDownloadCsvException,
            ) as error:
                if debug:
                    print(f"[{tries:02d}] - {error} When requesting {info}")
            finally:
                tries -= 1
                time.sleep(random.random() + random.random())

        return False

    def download_cities(
        self,
        cities_codes: Dict,
        output_format: OutputFormat = OutputFormat.SHAPEFILE,
        folder: Path | str = Path("temp"),
        tries: int = 25,
        debug: bool = False,
        chunk_size: int = 1024,
    ) -> Dict:
        """
        Download shapefiles or CSVs for multiple cities.

        Parameters:
            cities_codes (Dict): A dictionary mapping city names to their corresponding codes.
            output_format (OutputFormat, optional): The format of the files to download. Defaults to OutputFormat.SHAPEFILE.
            folder (Path | str, optional): The folder path where the downloaded files will be saved. Defaults to 'temp'.
            tries (int, optional): The number of download attempts allowed per city. Defaults to 25.
            debug (bool, optional): Whether to enable debug mode with additional print statements. Defaults to False.
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.

        Returns:
            Dict: A dictionary containing the results of the download operation.
                The keys are tuples of city name and code, and the values are the paths to the downloaded files.
                If a download fails for a city, the corresponding value will be False.
        """
        result = {}
        for city, code in cities_codes.items():
            result[(city, code)] = self.download_city_code(
                city_code=code,
                output_format=output_format,
                folder=folder,
                tries=tries,
                debug=debug,
                chunk_size=chunk_size,
            )
        return result

    def download_state(
        self,
        state: State | str,
        output_format: OutputFormat = OutputFormat.SHAPEFILE,
        folder: Path | str = Path("temp"),
        tries: int = 25,
        debug: bool = False,
        chunk_size: int = 1024,
    ):
        """
        Download shapefiles or CSVs for a state.

        Parameters:
            state (State | str): The state for which to download the files. It can be either a `State` enum value or a string representing the state's abbreviation.
            output_format (OutputFormat, optional): The format of the files to download. Defaults to OutputFormat.SHAPEFILE.
            folder (Path | str, optional): The folder path where the downloaded files will be saved. Defaults to 'temp'.
            tries (int, optional): The number of download attempts allowed per city. Defaults to 25.
            debug (bool, optional): Whether to enable debug mode with additional print statements. Defaults to False.
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.

        Returns:
            Dict: A dictionary containing the results of the download operation.
                The keys are tuples of city name and code, and the values are the paths to the downloaded files.
                If a download fails for a city, the corresponding value will be False.
        """
        cities_codes = self.get_cities_codes(state=state)

        return self.download_cities(
            cities_codes=cities_codes,
            output_format=output_format,
            folder=folder,
            tries=tries,
            debug=debug,
            chunk_size=chunk_size,
        )

    def download_country(
        self,
        output_format: OutputFormat = OutputFormat.SHAPEFILE,
        folder: Path | str = Path("brazil"),
        tries: int = 25,
        debug: bool = False,
        chunk_size: int = 1024,
    ):
        """
        Download shapefiles or CSVs for the entire country.

        Parameters:
            output_format (OutputFormat, optional): The format of the files to download. Defaults to OutputFormat.SHAPEFILE.
            folder (Path | str, optional): The folder path where the downloaded files will be saved. Defaults to 'brazil'.
            tries (int, optional): The number of download attempts allowed per city. Defaults to 25.
            debug (bool, optional): Whether to enable debug mode with additional print statements. Defaults to False.
            chunk_size (int, optional): The size of each chunk to download. Defaults to 1024.

        Returns:
            Dict: A dictionary containing the results of the download operation.
                The keys are the state abbreviations, and the values are dictionaries representing the results of downloading each state.
                Each state's dictionary follows the same structure as the result of the `download_state` method.
                If a download fails for a city within a state, the corresponding value will be False.
        """
        result = {}
        for state in State:
            Path(os.path.join(folder, f"{state}")).mkdir(parents=True, exist_ok=True)

            result[str(state)] = self.download_state(
                state=state,
                output_format=output_format,
                folder=folder,
                tries=tries,
                debug=debug,
                chunk_size=chunk_size,
            )
