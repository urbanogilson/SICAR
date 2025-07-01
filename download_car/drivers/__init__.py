# download_car/drivers/__init__.py
"""Drivers."""

from download_car.drivers.captcha import Captcha
from download_car.drivers.tesseract import Tesseract

try:
    from download_car.drivers.paddle import Paddle
except ImportError:
    pass
