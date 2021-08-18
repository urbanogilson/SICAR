class EmailNotValidException(Exception):
    """Exception raised for errors in the input email.

    Attributes:
        email -- email address which caused the error
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__("Email {} not valid!".format(self.email))


class UrlNotOkException(Exception):
    """Exception raised when the input url is not ok.

    Attributes:
        url -- url address which caused the error
    """

    def __init__(self, url: str):
        self.url = url
        super().__init__("Oh no! Failed to access {}!".format(self.url))


class StateCodeNotValidException(Exception):
    """Exception raised when the input state is not a brazian state code.

    Attributes:
        state -- state code which caused the error
    """

    def __init__(self, state: str):
        self.state = state
        super().__init__("State code {} not valid!".format(self.state))


class FailedToDownloadCaptchaException(Exception):
    """Exception raised when the captcha download failed."""

    def __init__(self, message: str = "Failed to download captcha!"):
        self.message = message
        super().__init__(self.message)


class FailedToDownloadShapefileException(Exception):
    """Exception raised when the shapefile download failed."""

    def __init__(self, message: str = "Failed to download shapefile!!"):
        self.message = message
        super().__init__(self.message)
