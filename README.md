# SICAR

[English](README.md) | [Português (BR)](README.pt-br.md)

This tool is designed for students, researchers, data scientists, or anyone who would like to have access to [SICAR](https://car.gov.br/publico/imoveis/index) files.

## Badges

[![Open In Collab](.github/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/examples/colab.ipynb)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker Pulls](https://img.shields.io/docker/pulls/urbanogilson/sicar)](https://hub.docker.com/r/urbanogilson/sicar)
[![Coverage Status](https://coveralls.io/repos/github/urbanogilson/SICAR/badge.svg?branch=main)](https://coveralls.io/github/urbanogilson/SICAR?branch=main)
[![interrogate](.github/interrogate_badge.svg)](https://interrogate.readthedocs.io/)

## Features

- Download polygon
- Download state
- Download the entire country
- Tesseract, and PaddleOCR (Optional) drivers to automatically detect captcha

## Installation

Install SICAR with pip

```bash
pip install git+https://github.com/urbanogilson/SICAR
```

Prerequisite:

[Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (additional info on how to install the engine on Linux, Mac OSX, and Windows).

Optional: [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (additional info on how to install the engine on Linux, Mac OSX, and Windows).

If you don't want to install dependencies on your computer or don't know how to install them, we strongly recommend [Google Colab](#run-with-google-colab).

## Documentation

- [SICAR package - API](https://gilsonurbano.com/sicar-api/)
- [SICAR package - What is? Why?](https://gilsonurbano.com/posts/sicar/)
- [Data dictionary](#data-dictionary)

## Usage/Examples

```python
from SICAR import Sicar, State, Polygon
import pprint

# Create Sicar instance
car = Sicar()

# Get release data dates
state_dates = car.get_release_dates()
pprint.pprint(state_dates)
# {<State.AC: 'AC'>: '03/06/2025',
#  <State.AL: 'AL'>: '04/06/2025',
#  <State.AM: 'AM'>: '03/06/2025',
#  <State.AP: 'AP'>: '03/06/2025',
#  <State.BA: 'BA'>: '03/06/2025',
#  <State.CE: 'CE'>: '04/06/2025',
#  <State.DF: 'DF'>: '03/06/2025',
#  <State.ES: 'ES'>: '05/06/2025',
#  <State.GO: 'GO'>: '04/06/2025',
#  <State.MA: 'MA'>: '01/06/2025',
#  <State.MG: 'MG'>: '05/06/2025',
#  <State.MS: 'MS'>: '08/06/2025',
#  <State.MT: 'MT'>: '05/06/2025',
#  <State.PA: 'PA'>: '03/06/2025',
#  <State.PB: 'PB'>: '05/06/2025',
#  <State.PE: 'PE'>: '01/06/2025',
#  <State.PI: 'PI'>: '01/06/2025',
#  <State.PR: 'PR'>: '03/06/2025',
#  <State.RJ: 'RJ'>: '01/06/2025',
#  <State.RN: 'RN'>: '01/06/2025',
#  <State.RO: 'RO'>: '01/06/2025',
#  <State.RR: 'RR'>: '04/06/2025',
#  <State.RS: 'RS'>: '04/06/2025',
#  <State.SC: 'SC'>: '01/06/2025',
#  <State.SE: 'SE'>: '04/06/2025',
#  <State.SP: 'SP'>: '05/06/2025',
#  <State.TO: 'TO'>: '04/06/2025'}

# Download APPS polygon for the PA state
car.download_state(State.PA, Polygon.APPS)
```

### OCR drivers

[Optical character recognition (OCR)](https://en.wikipedia.org/wiki/Optical_character_recognition) drivers are used to recognize characters in a captcha.

We currently have two options for automating the download process.

#### [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Default)

```python
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Tesseract

# Create Sicar instance using Tesseract OCR
car = Sicar(driver=Tesseract)

# Download a state
car.download_state(State.SP, Polygon.LEGAL_RESERVE, folder='SICAR/SP')
```

#### [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

Install SICAR with pip and include Paddle dependencies

```bash
pip install 'SICAR[paddle] @  git+https://github.com/urbanogilson/SICAR'
```

```python
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Paddle

# Create Sicar instance using PaddleOCR
car = Sicar(driver=Paddle)

# Download a state
car.download_state(State.AM, Polygon.CONSOLIDATED_AREA, folder='SICAR/AM')
```

### Run with Google Colab

Using Google Colab, you don't need to install the dependencies on your computer and you can save files directly to your Google Drive.

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/examples/colab.ipynb)

### Run with Docker

Pull Image from Docker Hub [urbanogilson/sicar](https://hub.docker.com/r/urbanogilson/sicar)

```sh
docker pull urbanogilson/sicar:latest
```

Run the downloaded Docker Image using an entry point (file) from your machine (host)

```sh
docker run -i -v $(pwd):/sicar urbanogilson/sicar:latest -<./examples/docker.py
```

Note: Update the entry point file [./examples/docker.py](./examples/docker.py) or create a new one to download data based on your needs.

or pass a script through `STDIN`

```sh
docker run -i -v $(pwd):/sicar urbanogilson/sicar:latest -<<EOF
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Paddle

car = Sicar(driver=Paddle)

car.download_state(state='MG', polygon=Polygon.CONSOLIDATED_AREA, folder='MG')
EOF
```

Note: Using `$(pwd)` the container will save the download data into the current folder.

Optional: Make an external directory to store the downloaded data and use a volume parameter in the run command to point to it.

## Data dictionary

| **Attribute** | **Classification** | **Data type** | **Description** |
|---------------|--------------------|---------------|-----------------|
| cod_tema      | public | text   | Indicates the code of the land use theme that makes up the registration of the rural property or possession in the National Rural Environmental Registry System (Sicar). This data classifies the different areas of the property according to their characteristics and regulations. |
| nom_tema      | public | text   | Indicates the name of the theme or environmental land use category that makes up the registration of the rural property or possession in the Sicar. This data classifies the different areas of the property according to their characteristics and regulations, including, for example: Permanent Preservation Area (APP), Remnant of Native Vegetation, Legal Reserve, Restricted Use Area, Consolidated Rural Area, Administrative Easement, Path, Hydrography, Wetland, Areas with Altitude Higher than 1800 meters, Areas with Slopes Higher than 45 degrees, Hilltops, Plateau Edges, Fallow Area, Mangrove and Restinga. |
| cod_imovel    | public | text   | Unique registration number assigned to each rural property or possession in the Sicar at the moment of its registration. |
| mod_fiscal    | public | number | Agrarian unit of measurement that varies by municipality and is used to classify the size of a rural property or possession (small, medium, large) in the Sicar, according to current legislation. |
| num_area      | public | number | Total gross area of the rural property informed by the owner or possessor at the moment of registration in the Sicar. |
| ind_status    | public | text   | Status of the registration in CAR, according to Normative Instruction no. 2, of May 6, 2014, of the Ministry of the Environment (https://www.car.gov.br/leis/IN_CAR.pdf), and the Resolution No. 3, of August 27, 2018, of the Brazilian Forest Service (https://imprensanacional.gov.br/materia/-/asset_publisher/Kujrw0TZC2Mb/content/id/38537086/do1-2018-08-28-resolucao-n-3-de-27-de-agos-de-2018-38536774), being AT - Active; PE - Pending; SU - Suspended; and CA - Cancelled. |
| ind_tipo      | public | text   | Classification of the type of rural property or possession according to the registration in the Sicar. Being IRU - Rural Property; AST - Agrarian Reform Settlements; PCT - Traditional Peoples and Communities. |
| des_condic    | public | text   | Indicates the current condition of the rural property or possession registration analysis in the Sicar. Reflects the stage the registration is at in the validation process, according to the progress of the technical analysis by the competent body. |
| municipio     | public | text   | Indicates the municipal political-administrative unit to which the rural property or possession is territorially located. |
| cod_estado    | public | text   | Two-letter code (UF) that identifies the Federative Unit (state) of Brazil to which the rural property or possession is located. |
| dat_criaca    | public | text   | Date on which the rural property or possession was registered in the Sicar. |
| dat_atuali    | public | text   | Date of the last time the registration data of the rural property or possession was modified in the Sicar. |

## Acknowledgements

- [Sicar - Sistema Nacional de Cadastro Ambiental Rural](https://www.car.gov.br/)
- [Sicar - Base de Downloads](https://consultapublica.car.gov.br/publico/estados/downloads)

## Roadmap

- [ ] Upload to pypi registry

## Contributing

The development environment with all necessary packages is available using [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/remote/containers).

[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/urbanogilson/SICAR)

Contributions are always welcome!

## Feedback

If you have any feedback, please reach me at hello@gilsonurbano.com

## License

[MIT](LICENSE)
