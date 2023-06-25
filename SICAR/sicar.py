# import requests

# import random
# from urllib.parse import urlencode
# import re
# import shutil
# from pathlib import Path
# import time
# from html import unescape
# from tqdm import tqdm

# import os
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from SICAR.exceptions import (
#     FailedToDownloadCaptchaException,
#     FailedToDownloadShapefileException,
#     FailedToDownloadCsvException,
#     EmailNotValidException,
#     StateCodeNotValidException,
#     UrlNotOkException,
# )
# from SICAR.drivers import Captcha, Tesseract

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# class Sicar:
#     """
#     Sicar
#     """

#     def __init__(
#         self,
#         driver: Captcha = Tesseract,
#         email: str = "sicar@sicar.com",
#         headers: Dict = None,
#     ):
#         self.__driver = driver()
#         self.__email = self._validate_email(email)
#         self._create_session(headers)
#         self._get(self.__base_url)


#     def _download_shapefile(
#         self,
#         city_code: str,
#         captcha: str,
#         folder: str = "shapefile",
#         chunk_size: int = 2048,
#     ) -> Path:
#         response = self._get(
#             "{}?{}".format(
#                 self.__shapefile_url,
#                 urlencode(
#                     {
#                         "municipio[id]": city_code,
#                         "email": self.__email,
#                         "captcha": captcha,
#                     }
#                 ),
#             ),
#             stream=True,
#         )

#         if not response.ok:
#             raise FailedToDownloadShapefileException()

#         path = Path(
#             os.path.join(
#                 folder, response.headers.get("filename", "SHAPE_{}".format(city_code))
#             )
#         ).with_suffix(".zip")

#         with open(path, "wb") as fd:
#             for chunk in tqdm(
#                 iterable=response.iter_content(chunk_size),
#                 total=float(response.headers.get("Content-Length", 0)) / chunk_size,
#                 unit="KB",
#                 unit_scale=True,
#                 unit_divisor=1024,
#                 desc="Downloading shapefile city code {}".format(city_code),
#             ):
#                 fd.write(chunk)

#         return path

#     def _download_csv(
#         self,
#         city_code: str,
#         captcha: str,
#         folder: str = "csv",
#         chunk_size: int = 2048,
#     ) -> Path:
#         response = self._get(
#             "{}?{}".format(
#                 self.__csv_url,
#                 urlencode(
#                     {
#                         "municipio[id]": city_code,
#                         "email": self.__email,
#                         "captcha": captcha,
#                     }
#                 ),
#             ),
#             stream=True,
#         )

#         if not response.ok:
#             raise FailedToDownloadCsvException()

#         path = Path(
#             os.path.join(
#                 folder, response.headers.get("filename", "CSV_{}".format(city_code))
#             )
#         ).with_suffix(".csv")

#         with open(path, "wb") as fd:
#             for chunk in tqdm(
#                 iterable=response.iter_content(chunk_size),
#                 total=float(response.headers.get("Content-Length", 0)) / chunk_size,
#                 unit="KB",
#                 unit_scale=True,
#                 unit_divisor=1024,
#                 desc="Downloading csv city code {}".format(city_code),
#             ):
#                 fd.write(chunk)

#         return path

#     def download_city_code(
#         self,
#         city_code: str,
#         tries: int = 25,
#         output_format: OutputFormat = OutputFormat.SHAPEFILE,
#         folder: str = "temp",
#         debug: bool = False,
#     ) -> Path:
#         Path(folder).mkdir(parents=True, exist_ok=True)
#         captcha = ""

#         while tries > 0:
#             try:
#                 captcha = self.__driver._get_captcha(
#                     self._download_captcha(folder=folder)
#                 )

#                 if len(captcha) == 5:
#                     if debug:
#                         print(
#                             "Try {} - Requesting {} with captcha: {}".format(
#                                 tries, output_format, captcha
#                             )
#                         )
#                     if output_format is OutputFormat.CSV:
#                         return self._download_csv(
#                             city_code=city_code, captcha=captcha, folder=folder
#                         )
#                     return self._download_shapefile(
#                         city_code=city_code, captcha=captcha, folder=folder
#                     )
#                 else:
#                     if debug:
#                         print("Invalid Captcha: {}".format(captcha))

#                     time.sleep(0.75 + random.random() + random.random())

#             except Exception:
#                 if debug:
#                     print("Try {} - Incorrect captcha: {} :-(".format(tries, captcha))
#                 tries -= 1
#                 time.sleep(1 + random.random() + random.random())

#         return False

#     def download_cities(
#         self,
#         cities_codes: dict,
#         output_format: OutputFormat = OutputFormat.SHAPEFILE,
#         tries: int = 25,
#         folder: str = "temp",
#         debug: bool = False,
#     ):
#         failed = {}

#         for city, code in cities_codes.items():
#             if not self.download_city_code(
#                 city_code=code,
#                 output_format=output_format,
#                 tries=tries,
#                 folder=folder,
#                 debug=debug,
#             ):
#                 failed[city] = code

#         return failed if len(failed) else True

#     def download_state(
#         self,
#         state: str,
#         output_format: OutputFormat = OutputFormat.SHAPEFILE,
#         tries: int = 25,
#         folder: str = None,
#         debug: bool = False,
#     ):
#         cities_codes = self.get_cities_codes(state=state)

#         return self.download_cities(
#             cities_codes=cities_codes,
#             output_format=output_format,
#             tries=tries,
#             folder=folder if type(folder) is str else state,
#             debug=debug,
#         )

#     def download_country(
#         self,
#         output_format: OutputFormat = OutputFormat.SHAPEFILE,
#         base_folder: str = "Brazil",
#         debug: bool = False,
#     ):
#         for state in self.__states:
#             folder = "{}/{}".format(base_folder, state)
#             Path(folder).mkdir(parents=True, exist_ok=True)

#             details = self.download_state(
#                 state=state, output_format=output_format, folder=folder, debug=debug
#             )

#             if isinstance(details, dict):
#                 # store log file with failed codes
#                 with open(folder + "/failed_codes.txt", "w") as f:
#                     print(details, file=f)


from SICAR.url import Url
from SICAR.output_format import OutputFormat
from SICAR.drivers import Captcha, Tesseract

from typing import Dict

from SICAR.exceptions import (
    EmailNotValidException,
    UrlNotOkException,
    StateCodeNotValidException,
    FailedToDownloadCaptchaException,
    FailedToDownloadShapefileException,
    FailedToDownloadCsvException,
)

import requests
import re
import random
from urllib.parse import urlencode
from html import unescape
from PIL import Image
import io
from SICAR.state import State

import shutil
import tempfile
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import shutil
from pathlib import Path
import time

# import time
# from html import unescape
from tqdm import tqdm

import os


class Sicar(Url):
    """
    Class representing the Sicar system.

    Sicar is a system for managing environmental rural properties in Brazil.

    It inherits from the Url class to provide access to URLs related to the Sicar system.

    Attributes:
        driver (Captcha): The driver used for handling captchas. Default is Tesseract.
        email (str): The personal email for communication or identification purposes. Default is "sicar@sicar.com".
        headers (Dict): Additional headers for HTTP requests. Default is None.

    """

    def __init__(
        self,
        driver: Captcha = Tesseract,
        email: str = "sicar@sicar.com",
        headers: Dict = None,
    ):
        """
        Initializes an instance of the Sicar class.

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
        # self._get(self._INDEX)

    def _create_session(self, headers: Dict = None):
        """
        Creates a new session for making HTTP requests.

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

    def _validate_email(self, email: str) -> str:
        """
        Validates the format of an email address.

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
        Sends a GET request to the specified URL using the session.

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
        Retrieves the codes of cities in a given state.

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
        response = self._get(
            "{}?{}".format(
                self._CAPTCHA, urlencode({"id": int(random.random() * 1000000)})
            ),
            stream=True,
        )

        if not response.ok:
            raise FailedToDownloadCaptchaException()

        return Image.open(io.BytesIO(response.content))

    def _download_shapefile(
        self,
        city_code: str | int,
        captcha: str,
        folder: str,
        chunk_size: int = 1024,
    ) -> Path:
        """
        Downloads the shapefile for the specified city code.

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
        response = self._get(f"{self._SHAPEFILE}?{query}", stream=True)

        if not response.ok:
            raise FailedToDownloadShapefileException()

        path = Path(os.path.join(folder, f"SHAPE_{city_code}")).with_suffix(".zip")

        total_size = int(response.headers.get("Content-Length", 0))

        with open(path, "wb") as fd:
            with tqdm(total=total_size, unit="iB", unit_scale=True) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    progress_bar.update(len(chunk))

        return Path

    def download_city_code(
        self,
        city_code: str | int,
        tries: int = 25,
        output_format: OutputFormat = OutputFormat.SHAPEFILE,
        folder: Path | str = Path("temp"),
        chunk_size: int = 1024,
        debug: bool = False,
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

            except FailedToDownloadCaptchaException as error:
                if debug:
                    print(f"[{tries:02d}] - {error} When requesting {info}")
            except FailedToDownloadShapefileException as error:
                if debug:
                    print(f"[{tries:02d}] - {error} When requesting {info}")
            finally:
                tries -= 1
                time.sleep(random.random() + random.random())

        return False
