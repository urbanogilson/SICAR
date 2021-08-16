from pathlib import Path
import re
from PIL import Image
from SICAR.drivers.captcha import Captcha


class Manual(Captcha):
    def _get_captcha(self, captcha: Path) -> str:
        Image.open(captcha).show()
        return re.sub("[^A-Za-z0-9]+", "", input("Captcha: "))
