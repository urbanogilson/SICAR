from pathlib import Path
import matplotlib.image as mpimg
from abc import ABC, abstractmethod


class Captcha(ABC):
    def _png_to_jpg(self, captcha: Path = Path("temp/captcha.png")) -> Path:
        captcha_jpg = captcha.with_suffix(".jpg")

        mpimg.imsave(
            captcha_jpg,
            mpimg.imread(captcha, 0),
            cmap="gray",
            vmin=0,
            vmax=255,
        )

        return captcha_jpg

    @abstractmethod
    def _get_captcha(self, captcha: Path = Path("temp/captcha.png")) -> str:
        pass
