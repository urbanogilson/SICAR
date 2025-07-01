# download_car/drivers/captcha.py
"""
Captcha Abstract Base Class.

This class represents an abstract base class for a Captcha.

Classes:
    Captcha: Abstract base class representing a Captcha.
"""

from abc import ABC, abstractmethod
import tempfile
from PIL import Image
import matplotlib.image as mpimg
import numpy as np
import cv2


class Captcha(ABC):
    """
    Abstract base class representing a Captcha.

    This class defines the interface for getting a Captcha.

    Methods:
        get_captcha(captcha) -> str:
            Abstract method to get the Captcha value.

    """

    @abstractmethod
    def get_captcha(self, captcha: Image) -> str:
        """
        Abstract method to get the Captcha value.

        Parameters:
            captcha (str): The captcha value to process.

        Returns:
            str: The processed Captcha value.

        """

    def _png_to_jpg(self, captcha: Image) -> np.ndarray:
        """
        Convert a PNG image to a JPEG image represented as a NumPy array.

        Parameters:
            captcha (Image): The PNG image to convert.

        Returns:
            np.ndarray: The converted JPEG image represented as a NumPy array.

        Note:
            This method saves the input PNG image to a temporary file with a ".png" suffix. It then converts the PNG image
            to a JPEG image using matplotlib's `imsave` function, with the grayscale colormap. The resulting JPEG image is
            saved to another temporary file with a ".jpg" suffix.

            The saved JPEG image is then loaded using OpenCV's `imread` function, and the image data is returned as a NumPy
            array.
        """
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as png:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as jpg:
                captcha.save(png.name)
                mpimg.imsave(
                    jpg.name,
                    mpimg.imread(png.name, 0),
                    cmap="gray",
                    vmin=0,
                    vmax=255,
                )
                return cv2.imread(jpg.name, -1)

    def _improve_image(self, image: np.ndarray):
        """
        Apply image enhancement operations to improve OCR results.

        Parameters:
            image (np.ndarray): The input image as a NumPy array.

        Returns:
            np.ndarray: The improved image as a NumPy array.

        Note:
            This method applies a series of image enhancement operations, including thresholding, dilation, and erosion,
            to improve the visibility and clarity of characters in the image for OCR.
        """
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU + 2)
        image = cv2.dilate(image, np.ones((3, 2), np.uint8), iterations=1)
        image = cv2.erode(image, np.ones((4, 1), np.uint8), iterations=2)
        image = cv2.dilate(image, np.ones((3, 1), np.uint8), iterations=2)
        image = cv2.erode(image, np.ones((2, 1), np.uint8), iterations=2)
        return image

    def _process_captcha(self, captcha: Image):
        """
        Process the captcha image to enhance its quality for OCR.

        Parameters:
            captcha (Image): The captcha image.

        Returns:
            np.ndarray: The processed image as a NumPy array.

        Note:
            This method converts the captcha image from PNG to JPEG format, applies grayscale conversion using OpenCV,
            and performs image enhancement operations such as thresholding, dilation, and erosion to improve the
            visibility of characters for OCR.
        """
        return self._improve_image(
            cv2.cvtColor(self._png_to_jpg(captcha), cv2.COLOR_BGR2GRAY)
        )
