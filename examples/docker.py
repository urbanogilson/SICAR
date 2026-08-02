import logging
import pprint

from SICAR import Polygon, Sicar, State
from SICAR.drivers import Tesseract

# Show SICAR's per-attempt download logs
logging.basicConfig(level=logging.INFO)
logging.getLogger("SICAR").setLevel(logging.DEBUG)

# Create Sicar instance
car = Sicar(driver=Tesseract)
# car = Sicar(driver=Paddle)

# Get release date for all states
release_dates = car.get_release_dates()
pprint.pprint(release_dates)

# Download APPS polygons for the Roraima state
car.download_state(state=State.RR, polygon=Polygon.AREA_FALL, folder="data/Roraima")

# Download APPS polygons for all states in Brazil
# car.download_country(polygon=Polygon.APPS, folder="/Brazil")
