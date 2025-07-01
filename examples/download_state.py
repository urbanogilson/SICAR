# examples/download_state.py
"""Example script to download data from SICAR using environment variables."""

import os
from SICAR import Sicar, Polygon, State
from SICAR.drivers import Paddle, Tesseract

# Read parameters from environment variables with reasonable defaults
state = State[os.getenv("STATE", "DF")]
polygon = Polygon[os.getenv("POLYGON", "APPS")]
folder = os.getenv("FOLDER", "data/DF")
debug = os.getenv("DEBUG", "False").lower() == "true"

# Create Sicar instance (default driver is Tesseract)
car = Sicar(driver=Tesseract)
# car = Sicar(driver=Paddle)

# Download polygons for the chosen state
car.download_state(state=state, polygon=polygon, folder=folder, debug=debug)

# Get release date for all states and print the one for the chosen state
release_dates = car.get_release_dates()
print(f"Release date for {state.name} is: {release_dates.get(state)}")

