# Jude Standings

Extrai rankings (standings) do sistema [JUDE](https://github.com/rsalesc/jude), usado em competições de programação. Os rankings são extraídos de forma simplificada, ignorando informações como tempo da submissão ou número de submissões.

## Instalação

Você precisará ter o Python 3 e o pipenv instalados.

Para baixar as dependências:

```sh
pipenv install
```

## Configuração

Você precisará editar o arquivo `listas.yml` para informar os dados das listas (contests) do JUDE cujos standings deseja baixar.

## Execução

Rode com o seguinte comando:

```sh
JUDE_USER=nnn JUDE_PASSWORD=nnn pipenv run python extract-standings.py
```

Troque `nnn` pelos valores adequados.

## Saída

A saída é gravada no arquivo `saida.csv`.
