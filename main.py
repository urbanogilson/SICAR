import requests
import random

session = requests.Session()

session.get('https://car.gov.br/publico/imoveis/index')

response = session.get('https://car.gov.br/publico/municipios/downloads')

f = session.get("https://car.gov.br/publico/municipios/shapefile?municipio%5Bid%5D=1200013&email=tuhubim%40mailinator.com&captcha=Ve5bh")

state = session.get('https://car.gov.br/publico/municipios/downloads?sigla=AP')

captchaUrl = 'https://car.gov.br/publico/municipios/captcha?id=' + str(int(random.random() * 1000000))
