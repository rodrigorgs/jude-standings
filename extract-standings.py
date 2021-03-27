#!/usr/bin/env python3

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time 


chrome_options = Options()  
# chrome_options.add_argument('--headless')  
chrome_options.add_argument('--window-size=1280,800')

driver = webdriver.Chrome(options = chrome_options)
driver.implicitly_wait(30)

driver.get('http://200.128.51.30/#/login?id=603bcc937293660011629359')

inputs = driver.find_elements_by_css_selector('input')
inputs[0].send_keys(os.getenv('JUDE_USER'))
inputs[1].send_keys(os.getenv('JUDE_PASSWORD'))

driver.find_element_by_link_text('Login').click()
time.sleep(2)
driver.get('http://200.128.51.30/#/contest/standings')

elems = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#floatTheadTable tbody tr")))

for elem in elems:
	children = elem.find_elements_by_css_selector('*')
	nome = children[2].get_attribute('innerText')
	score = children[3].get_attribute('innerText').split('\n')[0]
	details = []
	for question_elem in children[4:]:
		driver.implicitly_wait(0)
		p_elems = question_elem.find_elements_by_tag_name('p')
		
		correct = 0
		if len(p_elems) > 0:
			pts = p_elems[0].get_attribute('innerText').strip()
			if '+' in pts:
				correct = 1
		details.append(correct)

	print(f'nome: {nome}\tscore: {score}\tdetails: {" ".join([str(x) for x in details])}')

# x = driver.page_source
# print(x)


#####

# var x = Array.from(document.querySelectorAll('#floatTheadTable tbody tr'))
#   .map(e => ({
#     nome: e.children[1].innerText,
#     score: e.children[2].innerText.split('\n')[0],
#     detail: Array.from(e.children).slice(3).map(elem => elem.children.length == 0 ? '' : elem.children[0].children[0].innerText.trim().replace(/[+]$/, '0')),
#     time: Array.from(e.querySelectorAll('.ju-problem-cell:not(.ju-score-cell) .ju-score-info')).reduce((last, elem) => Math.max(last, parseInt(elem.innerText.split(':')[0])), 0)
# }));
# x.forEach(e => {
#   e.correct = e.detail.map(d => (parseInt(d) >= 0 ? 1 : 0))}
# );
# var y = x.map(e => `${e.nome}\t${e.score}\t${e.correct.join('\t')}`).sort().join('\n')
# console.log(y);