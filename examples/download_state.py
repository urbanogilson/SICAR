# examples/download_state.py
<<<<<<< HEAD
"""Example script to download data from SICAR using environment variables."""

import os
import argparse
from SICAR import Sicar, Polygon, State
from SICAR.drivers import Paddle, Tesseract

parser = argparse.ArgumentParser(description="Download SICAR state polygon.")
parser.add_argument("--state", type=str, default=os.getenv("STATE", "DF"))
parser.add_argument("--polygon", type=str, default=os.getenv("POLYGON", "APPS"))
parser.add_argument("--folder", type=str, default=os.getenv("FOLDER", "data/DF"))
parser.add_argument("--tries", type=int, default=int(os.getenv("TRIES", "25")))
parser.add_argument("--debug", type=lambda x: str(x).lower() == "true", default=os.getenv("DEBUG", "False"))
parser.add_argument("--timeout", type=int, default=int(os.getenv("TIMEOUT", "30")))
parser.add_argument("--max_retries", type=int, default=int(os.getenv("MAX_RETRIES", "5")))
args = parser.parse_args()

# Read parameters from environment variables with reasonable defaults
state = State[args.state] if args.state in State.__members__ else State[os.getenv("STATE", "DF")]
polygon = Polygon[args.polygon] if args.polygon in Polygon.__members__ else Polygon[os.getenv("POLYGON", "APPS")]
folder = args.folder
tries = args.tries
debug = args.debug
chunk_size = 1024
timeout = args.timeout
max_retries = args.max_retries

# Create Sicar instance (default driver is Tesseract)
car = Sicar(driver=Tesseract)
# car = Sicar(driver=Paddle)

# Download APPS polygons for the Roraima state
car.download_state(
    state=state,
    polygon=polygon,
    folder=folder,
    tries=tries,
    debug=debug,
    chunk_size=chunk_size,
    timeout=timeout,
    max_retries=max_retries,
=======
from SICAR import Sicar, Polygon, State
from SICAR.drivers import Paddle, Tesseract

parser = argparse.ArgumentParser(description="Download SICAR state polygon.")
parser.add_argument("--state", type=str, default=os.getenv("STATE", "DF"))
parser.add_argument("--polygon", type=str, default=os.getenv("POLYGON", "APPS"))
parser.add_argument("--folder", type=str, default=os.getenv("FOLDER", "data/DF"))
parser.add_argument("--tries", type=int, default=int(os.getenv("TRIES", "25")))
parser.add_argument("--debug", type=lambda x: str(x).lower() == "true", default=os.getenv("DEBUG", "False"))
parser.add_argument("--timeout", type=int, default=int(os.getenv("TIMEOUT", "30")))
parser.add_argument("--max_retries", type=int, default=int(os.getenv("MAX_RETRIES", "5")))
args = parser.parse_args()

# Read parameters from environment variables with reasonable defaults
state = State[args.state] if args.state in State.__members__ else State[os.getenv("STATE", "DF")]
polygon = Polygon[args.polygon] if args.polygon in Polygon.__members__ else Polygon[os.getenv("POLYGON", "APPS")]
folder = args.folder
tries = args.tries
debug = args.debug
chunk_size = 1024
timeout = args.timeout
max_retries = args.max_retries

# Create Sicar instance (default driver is Tesseract)
car = Sicar(driver=Tesseract)
# car = Sicar(driver=Paddle)

# Download APPS polygons for the Roraima state
car.download_state(
    state=State.DF, polygon=Polygon.APPS, folder="data/DF", debug=True
>>>>>>> dffc5aa (Revert "Add shell script runner and env-based example" (#11))
)

# Download APPS polygons for all states in Brazil
# car.download_country(polygon=Polygon.APPS, folder="/Brazil")

# Get release date for all states and print the one for the chosen state
release_dates = car.get_release_dates()
print(f"Release date for {state.name} is: {release_dates.get(state)}")

