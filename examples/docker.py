from SICAR import Sicar
from SICAR.drivers import Paddle

# from SICAR.drivers import Paddle

# Create Sicar instance
car = Sicar(email="sicar@sicar.com", driver=Paddle)
# car = Sicar(email="sicar@sicar.com", driver=Paddle)

# Download all shapefiles (cities) in Roraima state
car.download_state(state="RR", folder="data/Roraima", debug=True)

# Download all shapefiles (cities) in Brazil
# car.download_country(base_folder="/Brazil")
