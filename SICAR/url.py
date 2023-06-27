class Url:
    """
    Class representing CAR URLs for various resources.

    Attributes:
        _BASE (str): Base URL for the website.
        _INDEX (str): URL for the index of properties.
        _DOWNLOADS (str): URL for downloading shapefile files related to municipalities.
        _CSV (str): URL for downloading CSV files related to municipalities.
        _CAPTCHA (str): URL for CAPTCHA-related resources.
        _SHAPEFILE (str): URL for downloading shapefile resources related to municipalities.
    """

    _BASE = "https://www.car.gov.br/publico"
    _INDEX = f"{_BASE}/imoveis/index"
    _DOWNLOADS = f"{_BASE}/municipios/downloads"
    _CSV = f"{_BASE}/municipios/csv"
    _CAPTCHA = f"{_BASE}/municipios/captcha"
    _SHAPEFILE = f"{_BASE}/municipios/shapefile"
