# SICAR

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

# Create Sicar instance
car = Sicar()

# Download APPS polygon for the PA state
car.download_state(State.PA, Polygon.APPS)

# Get release date for all states as a dict
release_dates = car.get_release_dates()
print(release_dates.get(State.PA))
# '03/08/2024'
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

| **Attribute** | **Description**                                              |
|---------------|--------------------------------------------------------------|
| cod_estado    | Unit of the Federation in which the registration is located. |
| municipio     | Municipality in which the registration is located. |
| num_area      | Gross area of the rural property or the subject that makes up the registry, in hectare. |
| cod_imovel    | Registration number in the Rural Environmental Registry (CAR). |
| ind_status    | Status of registration in CAR, according to Normative Instruction no. 2, of May 6, 2014, of the Ministry of the Environment (https://www.car.gov.br/leis/IN_CAR.pdf), and the Resolution No. 3, of August 27, 2018, of the Brazilian Forest Service (https://imprensanacional.gov.br/materia/-/asset_publisher/Kujrw0TZC2Mb/content/id/38537086/do1-2018-08-28-resolucao-n-3-de-27-de-agos-de-2018-38536774), being AT - Active; PE - Pending; SU - Suspended; and CA - Cancelled. |
| des_condic    | Condition in which the registration is in the analysis flow by the competent body. |
| ind_tipo      | Type of Rural Property, being IRU - Rural Property; AST - Agrarian Reform Settlements; PCT - Traditional Territory of Traditional Peoples and Communities. |
| mod_fiscal    | Number of rural property tax modules. |
| nom_tema      | Name of the theme that makes up the registration (Permanent Preservation Area, Path, Remnant of Native Vegetation, Restricted Use Area, Administrative Easement, Legal Reserve, Hydrography, Wetlands, Consolidated Rural Area, Areas with Altitude Higher than 1800 meters, Areas with Slopes Higher than 45 degrees, Hilltops, Plateau Edges, Fallow Areas, Mangroves and Restinga). |

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
