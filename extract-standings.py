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

driver = None

def init_webdriver():
	if driver is None:
		chrome_options = Options()  
		# chrome_options.add_argument('--headless')  
		chrome_options.add_argument('--window-size=1280,800')
		driver = webdriver.Chrome(options = chrome_options)

# 'http://200.128.51.30/#/login?id=603bcc937293660011629359'
def get_standings_html(driver, url):
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


if __name__ == "__main__":
	with open('exemplo.html', 'r') as f:
		html = f.read()
		data = extract_data(html)
		# save_data_as_csv(data, 'teste.csv')
		for aluno in data:
		print("\t".join(aluno))
