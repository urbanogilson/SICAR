from SICAR import Sicar
from SICAR.drivers import Tesseract

# Create Sicar instance
car = Sicar(email="sicar@sicar.com", driver=Tesseract)

# Download all shapefiles (cities) in Brazil
car.download_country(base_folder="/Brazil")