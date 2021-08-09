from sicar import Sicar

# Create Sicar instance
car = Sicar(email = "sicar@sicar.com")

car.download_all_from_list(base_folder="/data")