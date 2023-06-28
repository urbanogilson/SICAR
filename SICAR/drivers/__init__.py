"""Drivers."""

from SICAR.drivers.captcha import Captcha
from SICAR.drivers.tesseract import Tesseract

try:
    from SICAR.drivers.paddle import Paddle
except ImportError:
    pass
