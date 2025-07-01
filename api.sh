#!/usr/bin/env bash
# api.sh

set -e

VENV=".venv-api"
PYTHON_VERSION="3.11.8"

if ! command -v pyenv &> /dev/null; then
  echo "❌ pyenv não encontrado. Instale antes de continuar."
  exit 1
fi

if [ ! -d "$VENV" ]; then
  echo "⚙️ Criando ambiente virtual $VENV"
  pyenv install -s $PYTHON_VERSION
  pyenv exec python -m venv $VENV
fi

source $VENV/bin/activate

pip install --upgrade pip
pip install fastapi uvicorn httpx Pillow tqdm

echo "🚀 Servidor FastAPI pronto em http://localhost:8000"
uvicorn app:app --reload --port 8000
