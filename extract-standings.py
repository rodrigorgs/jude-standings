#!/usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time 
import yaml

driver = None

def load_listas():
	with open('listas.yml', 'r') as f:
		return yaml.safe_load(f)

def init_webdriver():
	global driver
	if driver is None:
		chrome_options = Options()  
		chrome_options.add_argument('--headless')  
		chrome_options.add_argument('--window-size=1280,800')
		driver = webdriver.Chrome(options = chrome_options)

def quit_webdriver():
	global driver
	driver.quit()

def get_standings_html(url):
	global driver
	init_webdriver()
	driver.implicitly_wait(30)

	driver.get(url)

	inputs = driver.find_elements_by_css_selector('input')
	inputs[0].send_keys(os.getenv('JUDE_USER'))
	inputs[1].send_keys(os.getenv('JUDE_PASSWORD'))

	driver.find_element_by_link_text('Login').click()
	time.sleep(2)
	driver.get('http://200.128.51.30/#/contest/standings')

	elems = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#floatTheadTable tbody tr")))

	return driver.page_source

def extract_data(html):
	data = []
	soup = BeautifulSoup(html, 'html.parser')
	for elem in soup.select('#floatTheadTable tbody tr'):
		children = elem.select('td')
		nome = children[1].text.strip()
		score = children[2].select('p')[0].text.strip()
		details = []
		for question in children[3:]:
			correct = '0'
			p = question.select('p')
			if len(p) > 0 and '+' in p[0].text:
				correct = '1'
			details.append(correct)
		assert sum([int(x) for x in details]) == int(score)
		data.append([nome, score, *details])

	return sorted(data, key=lambda x: x[0])

def save_data_as_csv(data, filename):
	with open(filename, 'w') as f:
		for aluno in data:
			f.write("\t".join(aluno) + "\n")

# def get_example_standings():
# 	with open('exemplo.html', 'r') as f:
# 		html = f.read()	
# 	return html

def download_all_lists():
	registros = [['Nome', '#', 'Nome da Lista', 'Questão', 'Pontos']]
	listas = load_listas()
	for lista in listas:
		chave = lista['chave']
		nome_lista = lista['nome']
		print(nome_lista)
		html = get_standings_html(lista['url'])
		data = extract_data(html)
		for row in data:
			nome = row[0]
			score = row[1]
			details = row[2:]
			registros.append([nome, chave, nome_lista, 'score', score])
			for idx, question in enumerate(details):
				registros.append([nome, chave, nome_lista, f'Q{1+idx}', details[idx]])
	return registros


if __name__ == "__main__":
	data = download_all_lists()
	save_data_as_csv(data, 'saida.csv')
	quit_webdriver()
