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

## Usage/Examples

```python
from SICAR import Sicar, State, Polygon

# Create Sicar instance
car = Sicar()

# Download APPS polygon for PA state
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
from SICAR import Sicar
from SICAR.drivers import Paddle

car = Sicar(email="name@domain.com", driver=Paddle)

car.download_state(state='MG', folder='MG')
EOF
```

Note: Using `$(pwd)` the container will save the download data into the current folder.

Optional: Make an external directory to store the downloaded data and use a volume parameter in the run command to point to it.

## Acknowledgements

- [Sicar - Sistema Nacional de Cadastro Ambiental Rural](https://www.car.gov.br/)
- [Sicar - Base de Downloads](https://www.car.gov.br/publico/municipios/downloads)

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
