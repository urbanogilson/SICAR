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
from datetime import datetime
import time
from html import unescape
import random


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

    def __init__(self, email: str = "sicar@sicar.com"):
        self.__validate_email(email)
        self.email = email
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            }
        )
        self.__get(self.__base_url)

    def __get(self, url: str):
        response = self.session.get(url)
        assert response.ok, "Oh no! Failed to access " + url
        return response

    def __validate_email(self, email: str):
        if not re.search(
            r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$", email
        ):
            raise Exception("Email {} not valid!".format(email))

        return True

    def auto_download(
        self,
        city_code: str,
        tries: int = 25,
        path: str = "temp/",
        debug: bool = False,
    ):
        while tries > 0:
            try:
                self.get_captcha()
                captcha = self.process_captcha()

                if len(captcha) == 5:
                    self.download_shapefile(city_code, captcha, path)
                    return True
                else:
                    if debug:
                        print("Try {} - Short Captcha: {}".format(tries, captcha))
                    time.sleep(0.75 + random.random() + random.random())

            except:
                if debug:
                    print("Try {} - Invalid Captcha: {}".format(tries, captcha))
                time.sleep(1 + random.random() + random.random())

            tries -= 1

    def download_shapefile(self, city_code, captcha: str, path: str = "temp/"):
        query = {
            "municipio[id]": city_code,
            "email": self.email,
            "captcha": captcha,
        }

        response = self.session.get(
            self.__shapefile_url + urlencode(query), stream=True
        )

        assert response.ok, "Oh no! Failed to get shapefile"

        filename = response.headers["Content-Disposition"].split("filename=")[-1]

        with open(path + filename, "wb") as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)

        return True

    def get_cities_codes(self, state: str = "MG"):
        if state not in self.__states:
            raise Exception("State {} not valid!".format(state))

        query = {"sigla": state}
        response = self.__get(self.__downloads_url + urlencode(query))
        cities_codes = re.findall(r'(?<=data-municipio=")(.*)(?=")', response.text)

        return dict(zip(list(map(unescape, cities_codes[0::3])), cities_codes[1::3]))

    def get_captcha(self, filename: str = "captcha", path: str = "temp/"):
        captchaUrl = "https://car.gov.br/publico/municipios/captcha?id={}".format(
            int(random.random() * 1000000)
        )

        response = self.session.get(captchaUrl, stream=True)

        assert response.ok, "Oh no! Failed to get captcha"

        with open(path + filename + ".png", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        return path + filename + ".png"

    def improve_image(self, image):
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2)
        image = cv2.dilate(image, np.ones((3, 2), np.uint8), iterations=1)
        image = cv2.erode(image, np.ones((4, 1), np.uint8), iterations=2)
        image = cv2.dilate(image, np.ones((3, 1), np.uint8), iterations=2)
        image = cv2.erode(image, np.ones((2, 1), np.uint8), iterations=2)
        return image

    def png_to_jpg(self, filename: str = "captcha", path: str = "temp/"):
        mpimg.imsave(
            "{}{}.jpg".format(path, filename),
            mpimg.imread(path + filename + ".png", 0),
            cmap="gray",
            vmin=0,
            vmax=255,
        )

        return "{}{}.jpg".format(path, filename)

    def process_captcha(self, filename="captcha", path="temp/"):

        self.png_to_jpg(filename, path)

        img = cv2.cvtColor(cv2.imread(path + filename + ".jpg", -1), cv2.COLOR_BGR2GRAY)

        res = self.improve_image(img)

        mpimg.imsave("{}processed_{}.jpg".format(path, filename), res, cmap="gray")

        custom_l_psm_config = r"-l eng --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        return re.sub(
            "[^A-Za-z0-9]+",
            "",
            pytesseract.image_to_string(
                "{}processed_{}.jpg".format(path, filename), config=custom_l_psm_config
            ),
        )