#!/bin/bash
# download_state.sh

set -e

# \U1F9E0 Uso:
# ./download_state.sh --state DF --polygon APPS --folder data/DF --debug True

# \U1F9EA Verifica pyenv
if ! command -v pyenv &> /dev/null; then
  echo -e "\u274c pyenv não encontrado. Instale com:\n  brew install pyenv  # macOS\n  sudo apt install pyenv -y  # Ubuntu/Debian"
  exit 2
fi

# \U1F40D Define Python version
PYTHON_VERSION="3.10.12"
if ! pyenv versions --bare | grep -q "^$PYTHON_VERSION$"; then
  echo -e "\u23f3 Instalando Python $PYTHON_VERSION via pyenv..."
  pyenv install $PYTHON_VERSION
fi

# \U1F4E6 Cria venv se não existir
VENV_DIR=".venv-download"
if [[ ! -d "$VENV_DIR" ]]; then
  echo -e "\u23f3 Criando venv Python em $VENV_DIR..."
  PYENV_VERSION=$PYTHON_VERSION pyenv exec python -m venv $VENV_DIR
fi

# \u26A1 Ativa venv
source $VENV_DIR/bin/activate

# \u1F680 Instala dependências
pip install --upgrade pip
pip install 'git+https://github.com/Malnati/download-car#egg=SICAR[paddle]'

# \u1F6E0 Define variáveis de ambiente para passar os parâmetros para o script Python
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --state)
      STATE="$2"
      shift 2
      ;;
    --polygon)
      POLYGON="$2"
      shift 2
      ;;
    --folder)
      FOLDER="$2"
      shift 2
      ;;
    --debug)
      DEBUG="$2"
      shift 2
      ;;
    *)
      echo "Erro: Parâmetro desconhecido $1"
      echo "Uso: ./download_state.sh --state <state> --polygon <polygon> --folder <folder> --debug <debug>"
      exit 1
      ;;
  esac
done

# Verifica se os parâmetros obrigatórios foram passados
if [ -z "$STATE" ] || [ -z "$POLYGON" ] || [ -z "$FOLDER" ]; then
  echo "Erro: Parâmetros obrigatórios faltando."
  echo "Uso: ./download_state.sh --state <state> --polygon <polygon> --folder <folder> --debug <debug>"
  exit 1
fi

# \U1F4D1 Exemplo de parâmetros passados para o script
echo "Executando download para o estado $STATE, polígono $POLYGON, na pasta $FOLDER com debug=$DEBUG..."

# \u25B6️ Executa o script download_state.py com os parâmetros fornecidos
python examples/download_state.py --state "$STATE" --polygon "$POLYGON" --folder "$FOLDER" --debug "$DEBUG"

