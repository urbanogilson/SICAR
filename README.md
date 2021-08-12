# SICAR

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/urbanogilson/SICAR)](https://github.com/urbanogilson/SICAR/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/urbanogilson/SICAR?style=social)](https://github.com/urbanogilson/SICAR/stargazers/)
[![GitHub issues](https://img.shields.io/github/issues/urbanogilson/SICAR)](https://github.com/urbanogilson/SICAR/issues/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/urbanogilson/SICAR.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/urbanogilson/SICAR/context:python)

## What is SICAR?

This tool is designed for students, researchers, data scientists or anyone who would like to have access to [SICAR](https://car.gov.br/publico/imoveis/index) files.

## How to use SICAR?

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/src/example.ipynb)


## How to run with Docker?

To generate docker image
```sh
# using the docker build script
./docker-build.sh
```

To view or change the list of states, go to the sicar.py file and search for "__states"

Run to download all data from a hardcoded state list to a external directory.
Make an external directory to store the downloaded data, /my/local/data/dir, and use a volume parameter in the run command to point to it.
```sh
# run the docker image in detached mode
docker run -d --rm -v /my/local/data/dir:/data softwarevale/download-sicar:v0.1
```

### To-Do

- [ ] Download CSV files
- [ ] Add tests
  
