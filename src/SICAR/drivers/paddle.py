"""
PaddleOCR Driver Module.

This module provides an implementation of the Captcha driver using PaddleOCR.
The Paddle driver utilizes PaddleOCR to extract text from captcha images.

Note:
    This driver requires the paddlepaddle and paddleocr libraries to be installed.

Classes:
    Paddle: Implementation of the Captcha driver using PaddleOCR.
"""

import re

import cv2
from paddleocr import TextRecognition
from PIL import Image

from SICAR.drivers.captcha import Captcha


class Paddle(Captcha):
    """
    Implementation of the Captcha driver using PaddleOCR.

    This driver utilizes PaddleOCR's text recognition to extract text from captcha images.

    Note:
        This driver requires the paddlepaddle and paddleocr libraries to be installed.
    """

    def __init__(self) -> None:
        """
        Initialize the PaddleOCR text recognition predictor.

        Note:
            The captcha is already a single, cropped line of text, so only recognition is
            needed (no detection). The English recognition model `en_PP-OCRv4_mobile_rec`
            is used to match the Latin alphanumeric characters used by SICAR captchas.
        """
        self.ocr = TextRecognition(model_name="en_PP-OCRv4_mobile_rec")

    def get_captcha(self, captcha: Image.Image) -> str:
        """
        Extract text from the provided captcha image.

        Parameters:
            captcha (Image): The captcha image.

        Returns:
            str: The extracted text from the captcha.

        Note:
            This method processes the captcha image, improves its quality, and uses PaddleOCR's
            text recognition to perform optical character recognition. The processed image is
            converted to a 3-channel (BGR) image as required by the recognition model, and the
            extracted text is cleaned using regular expressions to remove non-alphanumeric
            characters.
        """
        image = cv2.cvtColor(self._process_captcha(captcha), cv2.COLOR_GRAY2BGR)
        result = self.ocr.predict(image)
        return re.sub("[^A-Za-z0-9]+", "", result[0]["rec_text"])
