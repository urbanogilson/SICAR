# download_car/url.py
"""
URL Class Module.

This module defines a class representing CAR URLs for various resources.

Classes:
    Url: Class representing CAR URLs for various resources.
        Attributes:
            _BASE (str): Base URL for the website.
            _INDEX (str): URL for the index of properties.
            _DOWNLOAD_BASE (str): URL for downloading polygon files related to states.
            _RECAPTCHA (str): URL for CAPTCHA-related resources.
"""


class Url:
    """
    Class representing CAR URLs for various resources.

    Attributes:
        _BASE (str): Base URL for the website.
        _INDEX (str): URL for the index of properties.
        _DOWNLOAD_BASE (str): URL for downloading polygon files related to states.
        _RECAPTCHA (str): URL for CAPTCHA-related resources.
    """

    _BASE = "https://consultapublica.car.gov.br/publico"
    _INDEX = f"{_BASE}/imoveis/index"
    _DOWNLOAD_BASE = f"{_BASE}/estados/downloadBase"
    _RECAPTCHA = f"{_BASE}/municipios/ReCaptcha"
    _RELEASE_DATE = f"{_BASE}/estados/downloads"
