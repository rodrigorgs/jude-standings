#!/usr/bin/env python3

import gspread
import os

GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_TITLE = os.getenv('SHEET_TITLE', 'JUDE-Standings')

def read_csv():
  with open('saida.csv', 'r') as f:
    lines = f.readlines()
    csv = [line.rstrip().split('\t') for line in lines]
    for line in csv[1:]:
      line[4] = int(line[4])
    return csv

# Lê CSV
data = read_csv()
rows = len(data)
cols = len(data[0])
interval = 'A1:' + chr(ord('A') + cols - 1) + str(rows)
print('Intervalo a atualizar: ' + interval)

# Cria arquivo JSON para autenticar no Google Drive
google_json_path = 'google-service-account.json'
if not os.path.exists(google_json_path):
  with open(google_json_path, 'w') as f:
    f.write(GOOGLE_SERVICE_ACCOUNT_JSON)

gc = gspread.service_account(filename = google_json_path)
spreadsheet = gc.open_by_key(SPREADSHEET_ID)
sheet_id = [i for i,v in enumerate(spreadsheet.worksheets()) if v.title == SHEET_TITLE][0]
sheet = spreadsheet.get_worksheet(sheet_id)
print('Atualizando planilha...')
sheet.update(interval, data)
print('Feito')

# print(sheet.row_count)
# print(index)



