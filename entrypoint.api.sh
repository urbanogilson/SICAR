#!/usr/bin/env bash
# entrypoint.api.sh
set -e

VENV=/opt/venv
PYTHON=python

${PYTHON} -m venv $VENV
source $VENV/bin/activate

pip install --upgrade pip
pip install fastapi uvicorn httpx Pillow tqdm

exec uvicorn app:app --host 0.0.0.0 --port 8000
