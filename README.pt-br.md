# SICAR

[English](README.md) | [Português (BR)](README.pt-br.md)

Esta ferramenta foi desenvolvida para estudantes, pesquisadores, cientistas de dados ou qualquer pessoa que queira ter acesso aos arquivos do [SICAR](https://car.gov.br/publico/imoveis/index).

## Badges

[![Open In Collab](.github/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/examples/colab.ipynb)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker Pulls](https://img.shields.io/docker/pulls/urbanogilson/sicar)](https://hub.docker.com/r/urbanogilson/sicar)
[![Coverage Status](https://coveralls.io/repos/github/urbanogilson/SICAR/badge.svg?branch=main)](https://coveralls.io/github/urbanogilson/SICAR?branch=main)
[![interrogate](.github/interrogate_badge.svg)](https://interrogate.readthedocs.io/)

## Funcionalidades

- Download de polígono
- Download de estado
- Download do país inteiro
- Drivers Tesseract e PaddleOCR (opcional) para detectar o captcha automaticamente

## Instalação

Instale o SICAR com pip

```bash
pip install git+https://github.com/urbanogilson/SICAR
```

Pré-requisito:

[Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (informações adicionais sobre como instalar o motor no Linux, Mac OSX e Windows).

Opcional: [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (informações adicionais sobre como instalar o motor no Linux, Mac OSX e Windows).

Se você não quiser instalar as dependências no seu computador ou não souber como instalá-las, recomendamos fortemente o [Google Colab](#executar-com-google-colab).

## Documentação

- [Pacote SICAR - API](https://gilsonurbano.com/sicar-api/)
- [Pacote SICAR - O que é? Por quê?](https://gilsonurbano.com/posts/sicar/)
- [Dicionário de dados](#dicionário-de-dados)

## Uso/Exemplos

```python
from SICAR import Sicar, State, Polygon
import pprint

# Cria a instância do Sicar
car = Sicar()

# Obtém as datas de disponibilização dos dados
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

# Faz o download do polígono APPS para o estado do PA
car.download_state(State.PA, Polygon.APPS)
```

### Drivers de OCR

Os drivers de [reconhecimento óptico de caracteres (OCR)](https://pt.wikipedia.org/wiki/Reconhecimento_%C3%B3ptico_de_caracteres) são usados para reconhecer caracteres em um captcha.

Atualmente temos duas opções para automatizar o processo de download.

#### [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Padrão)

```python
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Tesseract

# Cria a instância do Sicar usando o Tesseract OCR
car = Sicar(driver=Tesseract)

# Faz o download de um estado
car.download_state(State.SP, Polygon.LEGAL_RESERVE, folder='SICAR/SP')
```

#### [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

Instale o SICAR com pip incluindo as dependências do Paddle

```bash
pip install 'SICAR[paddle] @  git+https://github.com/urbanogilson/SICAR'
```

```python
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Paddle

# Cria a instância do Sicar usando o PaddleOCR
car = Sicar(driver=Paddle)

# Faz o download de um estado
car.download_state(State.AM, Polygon.CONSOLIDATED_AREA, folder='SICAR/AM')
```

### Executar com Google Colab

Usando o Google Colab, você não precisa instalar as dependências no seu computador e pode salvar os arquivos diretamente no seu Google Drive.

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/examples/colab.ipynb)

### Executar com Docker

Baixe a imagem do Docker Hub [urbanogilson/sicar](https://hub.docker.com/r/urbanogilson/sicar)

```sh
docker pull urbanogilson/sicar:latest
```

Execute a imagem Docker baixada usando um ponto de entrada (arquivo) da sua máquina (host)

```sh
docker run -i -v $(pwd):/sicar urbanogilson/sicar:latest -<./examples/docker.py
```

Nota: Atualize o arquivo de ponto de entrada [./examples/docker.py](./examples/docker.py) ou crie um novo para fazer o download dos dados conforme suas necessidades.

ou passe um script através do `STDIN`

```sh
docker run -i -v $(pwd):/sicar urbanogilson/sicar:latest -<<EOF
from SICAR import Sicar, State, Polygon
from SICAR.drivers import Paddle

car = Sicar(driver=Paddle)

car.download_state(state='MG', polygon=Polygon.CONSOLIDATED_AREA, folder='MG')
EOF
```

Nota: Usando `$(pwd)` o contêiner salvará os dados baixados na pasta atual.

Opcional: Crie um diretório externo para armazenar os dados baixados e use o parâmetro de volume no comando run para apontar para ele.

## Dicionário de dados

| **Atributo**  | **Descrição**                                                |
|---------------|--------------------------------------------------------------|
| cod_estado    | Unidade da Federação em que o cadastro está localizado. |
| municipio     | Município em que o cadastro está localizado. |
| num_area      | Área bruta do imóvel rural ou do objeto que compõe o cadastro, em hectares. |
| cod_imovel    | Número de registro no Cadastro Ambiental Rural (CAR). |
| ind_status    | Situação do cadastro no CAR, conforme a Instrução Normativa nº 2, de 6 de maio de 2014, do Ministério do Meio Ambiente (https://www.car.gov.br/leis/IN_CAR.pdf), e a Resolução nº 3, de 27 de agosto de 2018, do Serviço Florestal Brasileiro (https://imprensanacional.gov.br/materia/-/asset_publisher/Kujrw0TZC2Mb/content/id/38537086/do1-2018-08-28-resolucao-n-3-de-27-de-agos-de-2018-38536774), sendo AT - Ativo; PE - Pendente; SU - Suspenso; e CA - Cancelado. |
| des_condic    | Condição em que o cadastro se encontra no fluxo de análise pelo órgão competente. |
| ind_tipo      | Tipo de Imóvel Rural, sendo IRU - Imóvel Rural; AST - Assentamentos de Reforma Agrária; PCT - Território Tradicional de Povos e Comunidades Tradicionais. |
| mod_fiscal    | Número de módulos fiscais do imóvel rural. |
| nom_tema      | Nome do tema que compõe o cadastro (Área de Preservação Permanente, Servidão de Passagem, Remanescente de Vegetação Nativa, Área de Uso Restrito, Servidão Administrativa, Reserva Legal, Hidrografia, Áreas Úmidas, Área Rural Consolidada, Áreas com Altitude Superior a 1800 metros, Áreas com Declividade Superior a 45 graus, Topos de Morro, Bordas de Chapada, Áreas de Pousio, Manguezais e Restinga). |

## Agradecimentos

- [Sicar - Sistema Nacional de Cadastro Ambiental Rural](https://www.car.gov.br/)
- [Sicar - Base de Downloads](https://consultapublica.car.gov.br/publico/estados/downloads)

## Roadmap

- [ ] Publicar no registro pypi

## Contribuindo

O ambiente de desenvolvimento com todos os pacotes necessários está disponível usando [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/remote/containers).

[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/urbanogilson/SICAR)

Contribuições são sempre bem-vindas!

## Feedback

Se você tiver algum feedback, entre em contato comigo pelo e-mail hello@gilsonurbano.com

## Licença

[MIT](LICENSE)
