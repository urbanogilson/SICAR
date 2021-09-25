import requests
import random
from urllib.parse import urlencode
import re
import shutil
from pathlib import Path
import time
from html import unescape
from tqdm import tqdm
from typing import Dict
import os
from SICAR.exceptions import (
    FailedToDownloadCaptchaException,
    FailedToDownloadShapefileException,
    EmailNotValidException,
    StateCodeNotValidException,
    UrlNotOkException,
)
from SICAR.drivers import Captcha, Tesseract


class Sicar:
    """
    Sicar
    """

    __base_url = "https://car.gov.br/publico/imoveis/index"

    __downloads_url = "https://car.gov.br/publico/municipios/downloads"

    __capctha_url = "https://car.gov.br/publico/municipios/captcha"

    __shapefile_url = "https://car.gov.br/publico/municipios/shapefile"

    __states = [
        "AC",
        "AL",
        "AM",
        "AP",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MG",
        "MS",
        "MT",
        "PA",
        "PB",
        "PE",
        "PI",
        "PR",
        "RJ",
        "RN",
        "RO",
        "RR",
        "RS",
        "SC",
        "SE",
        "SP",
        "TO",
    ]

    def __init__(
        self,
        driver: Captcha = Tesseract,
        email: str = "sicar@sicar.com",
        headers: Dict = None,
    ):
        self.__driver = driver()
        self.__email = self._validate_email(email)
        self._create_session(headers)
        self._get(self.__base_url)

    def __str__(self):
        return "SICAR - {}".format(self.__email)

    def get_base_url(self) -> str:
        return self.__base_url

    def _get(self, url: str, *args, **kwargs):
        response = self.__session.get(url, *args, **kwargs)

        if not response.ok:
            raise UrlNotOkException(url)

        return response

    def _validate_email(self, email: str) -> str:
        if not re.search(
            r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$", email
        ):
            raise EmailNotValidException(email)

        return email

    def _create_session(self, headers: Dict = None):
        self.__session = requests.Session()
        self.__session.headers.update(
            headers
            if type(headers) is dict
            else {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            }
        )

    def get_cities_codes(self, state: str = "AM") -> Dict:
        """Get cities and codes by state

        Args:
            state (str, optional): A brazilian state code. Defaults to "AM".

        Raises:
            Exception: StateCodeNotValidException.

        Returns:
            dict: Cities and codes by state
        """
        state = state.upper()

        if state not in self.__states:
            raise StateCodeNotValidException(state)

        cities_codes = re.findall(
            r'(?<=data-municipio=")(.*)(?=")',
            self._get(
                "{}?{}".format(self.__downloads_url, urlencode({"sigla": state}))
            ).text,
        )

        return dict(zip(list(map(unescape, cities_codes[0::3])), cities_codes[1::3]))

    def _download_captcha(
        self, filename: str = "captcha", folder: str = "temp"
    ) -> Path:
        response = self._get(
            "{}?{}".format(
                self.__capctha_url, urlencode({"id": int(random.random() * 1000000)})
            ),
            stream=True,
        )

        if not response.ok:
            raise FailedToDownloadCaptchaException()

        path = Path(os.path.join(folder, filename)).with_suffix(".png")

        with open(path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        return path

    def _download_shapefile(
        self,
        city_code: str,
        captcha: str,
        folder: str = "shapefile",
        chunk_size: int = 2048,
    ) -> Path:
        response = self._get(
            "{}?{}".format(
                self.__shapefile_url,
                urlencode(
                    {
                        "municipio[id]": city_code,
                        "email": self.__email,
                        "captcha": captcha,
                    }
                ),
            ),
            stream=True,
        )

        if not response.ok:
            raise FailedToDownloadShapefileException()

        path = Path(
            os.path.join(
                folder, response.headers.get("filename", "SHAPE_{}".format(city_code))
            )
        ).with_suffix(".zip")

        with open(path, "wb") as fd:
            for chunk in tqdm(
                iterable=response.iter_content(chunk_size),
                total=float(response.headers.get("Content-Length", 0)) / chunk_size,
                unit="KB",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading shapefile city code {}".format(city_code),
            ):
                fd.write(chunk)

        return path

    def download_city_code(
        self, city_code: str, tries: int = 25, folder: str = "temp", debug: bool = False
    ):
        Path(folder).mkdir(parents=True, exist_ok=True)
        captcha = ""

        while tries > 0:
            try:
                captcha = self.__driver._get_captcha(
                    self._download_captcha(folder=folder)
                )

                if len(captcha) == 5:
                    if debug:
                        print(
                            "Try {} - Requesting shape file with captcha: {}".format(
                                tries, captcha
                            )
                        )

                    return self._download_shapefile(
                        city_code=city_code, captcha=captcha, folder=folder
                    )
                else:
                    if debug:
                        print("Invalid Captcha: {}".format(captcha))

                    time.sleep(0.75 + random.random() + random.random())

            except Exception:
                if debug:
                    print("Try {} - Incorret captcha: {} :-(".format(tries, captcha))
                tries -= 1
                time.sleep(1 + random.random() + random.random())

        return False

    def download_cities(
        self,
        cities_codes: dict,
        tries: int = 25,
        folder: str = "temp",
        debug: bool = False,
    ):
        failed = {}

        for city, code in cities_codes.items():
            if not self.download_city_code(
                city_code=code, tries=tries, folder=folder, debug=debug
            ):
                failed[city] = code

        return failed if len(failed) else True

    def download_state(
        self, state: str, tries: int = 25, folder: str = None, debug: bool = False
    ):
        cities_codes = self.get_cities_codes(state=state)

        return self.download_cities(
            cities_codes=cities_codes,
            tries=tries,
            folder=folder if type(folder) is str else state,
            debug=debug,
        )

    def download_country(self, base_folder: str = "Brazil", debug: bool = False):
        for state in self.__states:
            folder = "{}/{}".format(base_folder, state)
            Path(folder).mkdir(parents=True, exist_ok=True)

            details = self.download_state(state=state, folder=folder, debug=debug)

            if isinstance(details, dict):
                # store log file with failed codes
                with open(folder + "/failed_codes.txt", "w") as f:
                    print(details, file=f)
