import requests
import random
from urllib.parse import urlencode
import re
import shutil
import pytesseract
from pathlib import Path
from cv2 import cv2
import numpy as np
import matplotlib.image as mpimg
import time
from html import unescape
from tqdm import tqdm


class Sicar:
    """
    Sicar
    """

    __base_url = "https://car.gov.br/publico/imoveis/index"

    __downloads_url = "https://car.gov.br/publico/municipios/downloads?"

    __shapefile_url = "https://car.gov.br/publico/municipios/shapefile?"

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

    def __init__(self, email: str = "sicar@sicar.com", headers: dict = None):
        self.__email = self.__validate_email(email)
        self.__create_session(headers)
        self.__get(self.__base_url)

    def __get(self, url: str):
        response = self.__session.get(url)
        assert response.ok, "Oh no! Failed to access " + url
        return response

    def __validate_email(self, email: str):
        if not re.search(
            r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$", email
        ):
            raise Exception("Email {} not valid!".format(email))

        return email

    def __create_session(self, headers: dict = None):
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

    def download_city_code(
        self, city_code: str, tries: int = 25, folder: str = "temp", debug: bool = False
    ):
        Path(folder).mkdir(parents=True, exist_ok=True)

        while tries > 0:
            try:
                self.__get_captcha(folder=folder)
                _, filename = self.__process_captcha(folder=folder)
                captcha = self.__get_captcha_ocr(filename=filename, folder=folder)

                if len(captcha) == 5:
                    if debug:
                        print(
                            "Try {} - Requesting shape file with captcha: {}".format(
                                tries, captcha
                            )
                        )
                    self.__download_shapefile(
                        city_code=city_code, captcha=captcha, folder=folder
                    )
                    return True
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

    def get_cities_codes(self, state: str = "AM"):
        """Get cities and codes by state

        Args:
            state (str, optional): A brazilian state code. Defaults to "AM".

        Raises:
            Exception: State code not valid.

        Returns:
            dict: Cities and codes by state
        """
        if state not in self.__states:
            raise Exception("State {} not valid!".format(state))

        cities_codes = re.findall(
            r'(?<=data-municipio=")(.*)(?=")',
            self.__get(self.__downloads_url + urlencode({"sigla": state})).text,
        )

        return dict(zip(list(map(unescape, cities_codes[0::3])), cities_codes[1::3]))

    def __download_shapefile(
        self, city_code: str, captcha: str, folder: str = "temp", chunk_size: int = 2048
    ):
        response = self.__session.get(
            self.__shapefile_url
            + urlencode(
                {
                    "municipio[id]": city_code,
                    "email": self.__email,
                    "captcha": captcha,
                }
            ),
            stream=True,
        )

        if not response.ok:
            raise Exception("Failed to get shapefile!")

        with open("{}/{}.zip".format(folder, city_code), "wb") as fd:
            for chunk in tqdm(
                iterable=response.iter_content(chunk_size),
                total=int(response.headers.get("Content-Length", False) or 0)
                / chunk_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading city {}".format(city_code),
            ):
                fd.write(chunk)

        return True

    def __get_captcha(self, filename: str = "captcha", folder: str = "temp"):
        response = self.__session.get(
            "https://car.gov.br/publico/municipios/captcha?id={}".format(
                int(random.random() * 1000000)
            ),
            stream=True,
        )

        if not response.ok:
            raise Exception("Failed to get captcha!")

        with open("{}/{}.png".format(folder, filename), "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        return "{}/{}.png".format(folder, filename)

    def __improve_image(self, image):
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2)
        image = cv2.dilate(image, np.ones((3, 2), np.uint8), iterations=1)
        image = cv2.erode(image, np.ones((4, 1), np.uint8), iterations=2)
        image = cv2.dilate(image, np.ones((3, 1), np.uint8), iterations=2)
        image = cv2.erode(image, np.ones((2, 1), np.uint8), iterations=2)
        return image

    def __png_to_jpg(self, filename: str = "captcha", folder: str = "temp"):
        mpimg.imsave(
            "{}/{}.jpg".format(folder, filename),
            mpimg.imread("{}/{}.png".format(folder, filename), 0),
            cmap="gray",
            vmin=0,
            vmax=255,
        )

        return "{}/{}.jpg".format(folder, filename)

    def __process_captcha(self, filename="captcha", folder="temp"):

        self.__png_to_jpg(filename, folder)

        img = cv2.cvtColor(
            cv2.imread("{}/{}.jpg".format(folder, filename), -1), cv2.COLOR_BGR2GRAY
        )

        res = self.__improve_image(img)

        mpimg.imsave("{}/processed_{}.jpg".format(folder, filename), res, cmap="gray")

        return folder, "processed_{}.jpg".format(filename)

    def __get_captcha_ocr(self, filename="processed_captcha.jpg", folder="temp"):
        custom_l_psm_config = r"-l eng --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        return re.sub(
            "[^A-Za-z0-9]+",
            "",
            pytesseract.image_to_string(
                "{}/{}".format(folder, filename),
                config=custom_l_psm_config,
            ),
        )