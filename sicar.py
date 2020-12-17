import requests
import random
from urllib.parse import urlencode
import re

class Sicar():
    """
    Sicar
    """

    base_url = 'https://car.gov.br/publico/imoveis/index'

    downloads_url = 'https://car.gov.br/publico/municipios/downloads?'

    def __init__(self, email='example@sicar.com'):
        self.email = email
        self.session = requests.Session()
        self.get(self.base_url)
    pass

    def get(self, url):
        response = self.session.get(url)
        assert response.ok, 'Oh no! Failed to access ' + url
        return response

    def get_cities_code(self, state='AC'):
        query = {'sigla': state}
        response = self.get(self.downloads_url + urlencode(query))
        return re.findall(r'(?<="shapefile" data-municipio=")(.*)(?=")', response.text)

    