# SICAR

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/urbanogilson/SICAR)](https://github.com/urbanogilson/SICAR/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/urbanogilson/SICAR?style=social)](https://github.com/urbanogilson/SICAR/stargazers/)
[![GitHub issues](https://img.shields.io/github/issues/urbanogilson/SICAR)](https://github.com/urbanogilson/SICAR/issues/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/urbanogilson/SICAR.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/urbanogilson/SICAR/context:python)

## What is SICAR?

This tool is designed for students, researchers, data scientists or anyone who would like to have access to [SICAR](https://car.gov.br/publico/imoveis/index) files.

## How to use SICAR?

### Run on your computer

SICAR was developed and tested with Python 3.8.

To install SICAR using pip
```sh
pip install git+https://github.com/urbanogilson/SICAR@v0.2
```

```python
from SICAR import Sicar
import pprint

# Create Sicar instance
car = Sicar(email = "name@domain.com")

# Get cities codes in Roraima
cities_codes = car.get_cities_codes(state='RR')

pprint.pprint(cities_codes)
# {'Alto Alegre': '1400050',
#  'Amajari': '1400027',
#  'Boa Vista': '1400100',
#  'Bonfim': '1400159',
#  'Cantá': '1400175',
#  'Caracaraí': '1400209',
#  'Caroebe': '1400233',
#  'Iracema': '1400282',
#  'Mucajaí': '1400308',
#  'Normandia': '1400407',
#  'Pacaraima': '1400456',
#  'Rorainópolis': '1400472',
#  'São João da Baliza': '1400506',
#  'São Luiz': '1400605',
#  'Uiramutã': '1400704'}

# Download 'Alto Alegre': '1400050'
car.download_city_code('1400050', folder='Roraima')
```

### Run with Google Colab

Using Google Colab, you don't need to install the dependencies on your computer and you can save files directly to your Google Drive.

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/src/example.ipynb)


### Run with Docker

Update the the entry point file [./examples/docker.py](./examples/docker.py) to dowload data based on your needs.

Generate docker image
```sh
# using the docker build script
./docker-build.sh
```

Run to download all data defined in the [./examples/docker.py](./examples/docker.py) entry point to an external directory.

Make an external directory to store the downloaded data, /my/local/data/dir, and use a volume parameter in the run command to point to it.
```sh
# run the docker image in detached mode
docker run -d --rm -v /my/local/data/dir:/data softwarevale/download-sicar:v0.1
```

### To-Do

- [ ] Download CSV files
- [ ] Add tests
  
