import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
import random
from collections import Counter
import cv2
import pytesseract
import re
import sys
import requests
import random


def png_to_jpg(image, path=None):
    mpimg.imsave(
        "{}/{}.jpg".format(image.parent, image.stem),
        mpimg.imread(image, 0),
        cmap="gray",
        vmin=0,
        vmax=255,
    )


def pngs_to_jpgs(data_dir):
    images = list(data_dir.glob("*.png"))
    for image in images:
        png_to_jpg(image)


def otsu_thresholding(image):
    ret2, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2)
    image = cv2.dilate(image, np.ones((3, 2), np.uint8), iterations=1)
    image = cv2.erode(image, np.ones((4, 1), np.uint8), iterations=2)
    image = cv2.dilate(image, np.ones((3, 1), np.uint8), iterations=2)
    image = cv2.erode(image, np.ones((2, 1), np.uint8), iterations=2)
    return image


session = requests.Session()

session.get("https://car.gov.br/publico/imoveis/index")

response = session.get("https://car.gov.br/publico/municipios/downloads")

f = session.get(
    "https://car.gov.br/publico/municipios/shapefile?municipio%5Bid%5D=1200013&email=tuhubim%40mailinator.com&captcha=Ve5bh"
)

state = session.get("https://car.gov.br/publico/municipios/downloads?sigla=AP")

captchaUrl = "https://car.gov.br/publico/municipios/captcha?id=" + str(
    int(random.random() * 1000000)
)

data_dir = Path("dataset")

pngs_to_jpgs(data_dir)

images = list(data_dir.glob("*.jpg"))

c = 0

for image in images:
    img = cv2.cvtColor(cv2.imread(str(image), -1), cv2.COLOR_BGR2GRAY)
    res = otsu_thresholding(img)

    plt.imsave("dataset//processed/{}.jpg".format(image.stem), res, cmap="gray")

    captcha = re.sub(
        "[^A-Za-z0-9]+",
        "",
        pytesseract.image_to_string("dataset/processed/{}.jpg".format(image.stem)),
    )

    if image.stem == captcha:
        c += 1

    print(
        "Original: "
        + image.stem
        + " Processed: "
        + captcha
        + " Equal: "
        + str(image.stem == captcha)
    )

print(c, round(c / len(images) * 100, 2))