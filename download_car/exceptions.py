# download_car/exceptions.py
"""
Custom Exception Classes Module.

This module provides custom exception classes for specific error conditions.

Classes:
    UrlNotOkException: Exception raised when a URL is inaccessible or returns an error.
    StateCodeNotValidException: Exception raised when an invalid state code is encountered.
    FailedToDownloadCaptchaException: Exception raised when downloading a captcha fails.
    FailedToDownloadPolygonException: Exception raised when downloading a polygon fails.
    FailedToGetReleaseDateException: Exception raised when downloading release date fails.
"""


class UrlNotOkException(Exception):
    """
    Exception raised when a URL is inaccessible or returns an error.

    Attributes:
        url (str): The problematic URL.
    """

    def __init__(self, url: str):
        """
        Initialize an instance of UrlNotOkException.

        Parameters:
            url (str): The problematic URL.

        Returns:
            None
        """
        self.url = url
        super().__init__(f"Oh no! Failed to access {self.url}!")


class StateCodeNotValidException(Exception):
    """
    Exception raised when an invalid state code is encountered.

    Attributes:
        state (str): The invalid state code.
    """

    def __init__(self, state: str):
        """
        Initialize an instance of StateCodeNotValidException.

        Parameters:
            state (str): The invalid state code.

        Returns:
            None
        """
        self.state = state
        super().__init__(f"State code {self.state} not valid!")


class PolygonNotValidException(Exception):
    """
    Exception raised when an invalid polygon is encountered.

    Attributes:
        polygon (str): The invalid polygon.
    """

    def __init__(self, polygon: str):
        """
        Initialize an instance of PolygonNotValidException.

        Parameters:
            polygon (str): The invalid polygon.

        Returns:
            None
        """
        self.polygon = polygon
        super().__init__(f"Polygon {self.polygon} not valid!")


class FailedToDownloadCaptchaException(Exception):
    """Exception raised when downloading a captcha fails."""

    def __init__(self):
        """
        Initialize an instance of FailedToDownloadCaptchaException.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__("Failed to download captcha!")


class FailedToDownloadPolygonException(Exception):
    """Exception raised when downloading a polygon fails."""

    def __init__(self):
        """
        Initialize an instance of FailedToDownloadPolygonException.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__("Failed to download polygon!")


class FailedToGetReleaseDateException(Exception):
    """Exception raised when get release date fails."""

    def __init__(self):
        """
        Initialize an instance of FailedToGetReleaseDateException.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__("Failed to get release date!")
