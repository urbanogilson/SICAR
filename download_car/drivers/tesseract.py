# download_car/drivers/tesseract.py
"""
Tesseract OCR Driver Module.

This module provides an implementation of the Captcha driver using Tesseract OCR.
The Tesseract driver utilizes Tesseract OCR to extract text from captcha images.

Note:
    This driver requires the pytesseract library and Tesseract OCR to be installed.

Classes:
    Tesseract: Implementation of the Captcha driver using Tesseract OCR.
"""

import re
import pytesseract
from PIL import Image

from download_car.drivers.captcha import Captcha


class Tesseract(Captcha):
    """
    Implementation of the Captcha driver using Tesseract OCR.

    This driver utilizes Tesseract OCR to extract text from captcha images.

    Note:
        This driver requires the pytesseract library and Tesseract OCR to be installed.
    """

    _custom_l_psm_config = r"-l eng --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    """
    Tesseract OCR configuration string for customizing the recognition process.

    This configuration string sets the language to English (-l eng), defines the page segmentation mode as
    single character (-psm 7), and specifies the whitelist of characters to be recognized.

    For this driver, the whitelist includes uppercase and lowercase alphabets (A-Z, a-z) and digits (0-9).

    Note:
        Modifying this configuration string can affect the recognition results and may require adjustments
        depending on the specific captcha format.
    """

    def get_captcha(self, captcha: Image) -> str:
        """
        Extract text from the provided captcha image.

        Parameters:
            captcha (Image): The captcha image.

        Returns:
            str: The extracted text from the captcha.

        Note:
            This method processes the captcha image, improves its quality, and uses pytesseract's image_to_string
            function to perform optical character recognition. The extracted text is then cleaned using regular
            expressions to remove non-alphanumeric characters.
        """
        return re.sub(
            "[^A-Za-z0-9]+",
            "",
            pytesseract.image_to_string(
                self._process_captcha(captcha),
                config=self._custom_l_psm_config,
            ),
        )
