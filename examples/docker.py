from SICAR import Sicar, Polygon, State
from SICAR.drivers import Paddle, Tesseract

# Create Sicar instance
car = Sicar(driver=Tesseract)
# car = Sicar(driver=Paddle)

# Download APPS polygons for the Roraima state
car.download_state(
    state=State.DF, polygon=Polygon.APPS, folder="data/DF", debug=True
)

# Download APPS polygons for all states in Brazil
# car.download_country(polygon=Polygon.APPS, folder="/Brazil")

# Get release date for all states
release_dates = car.get_release_dates()
# get a single state value
print(f"Release date for DF is: {release_dates.get(State.DF)}")

