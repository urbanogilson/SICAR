# download_car/drivers/paddle.py
"""
PaddleOCR Driver Module.

This module provides an implementation of the Captcha driver using PaddleOCR.
The Paddle driver utilizes PaddleOCR to extract text from captcha images.

Note:
    This driver requires the paddlepaddle and paddleocr libraries to be installed.

Classes:
    Paddle: Implementation of the Captcha driver using PaddleOCR.
"""

from paddleocr import PaddleOCR
import itertools
import re
from PIL import Image

from download_car.drivers.captcha import Captcha


class Paddle(Captcha):
    """
    Implementation of the Captcha driver using PaddleOCR.

    This driver utializes PaddleOCR to extract text from captcha images.

    Note:
        This driver requires the paddlepaddle and paddleocr libraries to be installed.
    """

    def __init__(self):
        """
        Initialize the PaddleOCR instance.

        Note:
            The `use_angle_cls` parameter is set to False to disable text angle detection.
            The `lang` parameter is set to "en" to specify the English language.
            The `use_space_char` parameter is set to False to disable space character output.
            The `show_log` parameter is set to False to suppress PaddleOCR's logging messages.
        """
        self.ocr = PaddleOCR(
            use_angle_cls=False, lang="en", use_space_char=False, show_log=False
        )

    def get_captcha(self, captcha: Image) -> str:
        """
        Extract text from the provided captcha image.

        Parameters:
            captcha (Image): The captcha image.

        Returns:
            str: The extracted text from the captcha.

        Note:
            This method processes the captcha image, improves its quality, and uses PaddleOCR's ocr method to perform
            optical character recognition. The extracted text is then cleaned using regular expressions to remove
            non-alphanumeric characters.
        """
        return re.sub(
            "[^A-Za-z0-9]+",
            "",
            list(
                itertools.chain.from_iterable(
                    self.ocr.ocr(self._process_captcha(captcha), det=False, cls=False)
                )
            )[0][0],
        )
