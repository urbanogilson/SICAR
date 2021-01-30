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


class Sicar:
    """
    Sicar
    """

    base_url = "https://car.gov.br/publico/imoveis/index"

    downloads_url = "https://car.gov.br/publico/municipios/downloads?"

    def __init__(self, email="example@sicar.com"):
        self.email = email
        self.session = requests.Session()
        self.get(self.base_url)

    def get(self, url):
        response = self.session.get(url)
        assert response.ok, "Oh no! Failed to access " + url
        return response

    def get_cities_code(self, state="AC"):
        query = {"sigla": state}
        response = self.get(self.downloads_url + urlencode(query))
        return re.findall(r'(?<="shapefile" data-municipio=")(.*)(?=")', response.text)

    def get_captcha(self, filename="captcha.png", path="temp/"):
        captchaUrl = "https://car.gov.br/publico/municipios/captcha?id={}".format(
            int(random.random() * 1000000)
        )
        response = self.session.get(captchaUrl, stream=True)

        with open(path + filename, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        return True

    def otsu_thresholding(self, image):
        ret, image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2
        )
        image = cv2.dilate(image, np.ones((3, 2), np.uint8), iterations=1)
        image = cv2.erode(image, np.ones((4, 1), np.uint8), iterations=2)
        image = cv2.dilate(image, np.ones((3, 1), np.uint8), iterations=2)
        image = cv2.erode(image, np.ones((2, 1), np.uint8), iterations=2)
        return image

    def png_to_jpg(self, filename="captcha.png", path="temp/"):
        image = path + filename
        mpimg.imsave(
            "{}/{}.jpg".format(path, filename),
            mpimg.imread(image, 0),
            cmap="gray",
            vmin=0,
            vmax=255,
        )

    def process_captcha(self, filename="captcha.png", path="temp/"):
        self.png_to_jpg(filename, path)
        img = cv2.cvtColor(cv2.imread(path + filename + ".jpg", -1), cv2.COLOR_BGR2GRAY)
        res = self.otsu_thresholding(img)
        name = datetime.now().strftime("%H_%M_%S")
        mpimg.imsave("{}/processed_{}.jpg".format(path, name), res, cmap="gray")
        return re.sub(
            "[^A-Za-z0-9]+",
            "",
            pytesseract.image_to_string("{}/processed_{}.jpg".format(path, name)),
        )