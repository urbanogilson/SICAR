# SICAR

[English](README.md) | [Português (BR)](README.pt-br.md)

Esta ferramenta foi desenvolvida para estudantes, pesquisadores, cientistas de dados ou qualquer pessoa que queira ter acesso aos arquivos do [SICAR](https://car.gov.br/publico/imoveis/index).

## Badges

[![Open In Collab](.github/colab-badge.svg)](https://colab.research.google.com/github/urbanogilson/SICAR/blob/main/examples/colab.ipynb)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
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
car.download_state(State.SP, Polygon.LEGAL_RESERVE, folder="SICAR/SP")
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
car.download_state(State.AM, Polygon.CONSOLIDATED_AREA, folder="SICAR/AM")
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

> Baseado no [Dicionário de Dados do SICAR](docs/Dicionario_de_Dados_SICAR.pdf) oficial.

| **Nome Atributo** | **Tipificação** | **Tipo de Dado** | **Descrição** |
|-------------------|-----------------|------------------|---------------|
| cod_tema      | publico | texto  | Indica o código do tema de uso do solo que compõe o cadastro da propriedade ou posse rural no Sistema Nacional de Cadastro Ambiental Rural (Sicar). Este dado classifica as diferentes áreas da propriedade conforme suas características e regulamentações. |
| nom_tema      | publico | texto  | Indica o nome do tema ou categoria ambiental de uso do solo que compõe o cadastro da propriedade ou posse rural no Sistema Nacional de Cadastro Ambiental Rural (Sicar). Este dado classifica as diferentes áreas da propriedade conforme suas características e regulamentações, incluindo, por exemplo: Área de Preservação Permanente (APP), Remanescente de Vegetação Nativa, Reserva Legal, Área de Uso Restrito, Área Rural Consolidada, Servidão Administrativa, Vereda, Hidrografia, Banhado, Áreas com Altitude Superior a 1800 metros, Áreas com Declividades Superiores a 45 graus, Topos de Morro, Bordas de Chapada, Área de Pousio, Manguezal e Restinga. |
| cod_imovel    | publico | texto  | Número de inscrição único atribuído a cada propriedade ou posse rural no Sistema Nacional de Cadastro Ambiental Rural (Sicar) no momento de sua inscrição. |
| mod_fiscal    | publico | numero | Unidade de medida agrária que varia por município e é utilizada para classificar o tamanho de uma propriedade ou posse rural (pequena, média, grande) no Sistema Nacional de Cadastro Ambiental Rural (Sicar), conforme a legislação vigente. |
| num_area      | publico | numero | Área bruta total do imóvel rural informada pelo proprietário ou possuidor no momento da inscrição no Sistema Nacional de Cadastro Ambiental Rural (Sicar). |
| ind_status    | publico | texto  | Situação do cadastro no CAR, segundo a Instrução Normativa nº 2, de 06 de maio de 2014, do Ministério do Meio Ambiente (https://www.car.gov.br/leis/IN_CAR.pdf), e a Resolução nº 3, de 27 de agosto de 2018, do Serviço Florestal Brasileiro (https://imprensanacional.gov.br/materia/-/asset_publisher/Kujrw0TZC2Mb/content/id/38537086/do1-2018-08-28-resolucao-n-3-de-27-de-agosto-de-2018-38536774), sendo AT - Ativo; PE - Pendente; SU - Suspenso; e CA - Cancelado. |
| ind_tipo      | publico | texto  | Classificação do tipo de propriedade ou posse rural conforme o registro no Sistema Nacional de Cadastro Ambiental Rural (Sicar). Sendo IRU - Imóvel Rural; AST - Assentamentos de Reforma Agrária; PCT - Povos e Comunidades Tradicionais. |
| des_condic    | publico | texto  | Indica a condição atual da análise do registro da propriedade ou posse rural no Sistema Nacional de Cadastro Ambiental Rural (Sicar). Reflete a etapa em que o cadastro se encontra no processo de validação, conforme o andamento da análise técnica pelo órgão competente. |
| municipio     | publico | texto  | Indica a unidade político-administrativa municipal à qual a propriedade ou posse rural está territorialmente localizada. |
| cod_estado    | publico | texto  | Código de duas letras (UF) que identifica a Unidade Federativa (estado) do Brasil à qual a propriedade ou posse rural está localizada. |
| dat_criaca    | publico | texto  | Data em que a propriedade ou posse rural foi inscrita no Sistema Nacional de Cadastro Ambiental Rural (Sicar). |
| dat_atuali    | publico | texto  | Data da última vez em que os dados de inscrição da propriedade ou posse rural foram modificados no Sistema Nacional de Cadastro Ambiental Rural (Sicar). |

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
