https://superuser.com/questions/162624/how-to-password-protect-gzip-files-on-the-command-line

# Jude Standings

Extrai rankings (standings) do sistema [JUDE](https://github.com/rsalesc/jude), usado em competições de programação. Os rankings são extraídos de forma simplificada, ignorando informações como tempo da submissão ou número de submissões.

## Instalação

Você precisará ter os seguintes programas instalados:

- Python 3
- pipenv
- Google Chrome (ou Chromium)
- ChromeDriver

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

## Workflow do GitHub (GitHub Actions)

Este repositório está configurado para extrair os rankings diariamente. A saída fica disponível como artefato juntamente com o log de execução do workflow.

Além disso, o workflow executa um script (`upload-standings.py`) para fazer o upload dos rankings para uma planilha do Google Drive.

Para executar o workflow, você precisa configurar os seguintes *secrets* no seu repositório:

- `JUDE_USER` e `JUDE_PASSWORD`: credenciais usadas para acessar todas as listas do JUDE
- `GOOGLE_SERVICE_ACCOUNT_JSON`: credenciais (arquivo JSON) usadas pela aplicação para acessar a planilha no Google Drive
- `SPREADSHEET_ID`: identificador alfanumérico da planilha; pode ser obtido de sua URL
- `SHEET_TITLE`: título da planilha (aba) onde os dados serão gravados; se houver algum texto na planilha (aba), ele será sobrescrito.
