from urllib.request import urlopen as uReq
import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as numpy
import pandas as pd

executable_path = "/usr/local/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('/Users/JosephLai/Desktop/scraping/cjpalhdlnbpafiamejdnhcphjbkeiagm-1.18.4-www.Crx4Chrome.com.crx')

driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

t = time.time()  #"https://www.ratemyprofessors.com/ShowRatings.jsp?tid=953067"

driver.get("https://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolID=1&queryoption=TEACHER")


print("refreshing")
driver.refresh()
print("done refreshing")

try: 
	#TODO: I believe this only happens on the first url load the delay is not necessary, but not sure
	WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'reveal-modal-bg')))
	js = "var aa=document.getElementsByClassName('reveal-modal-bg')[0]; aa.parentNode.removeChild(aa)"
	driver.execute_script(js)
	print("modal removed")
except TimeoutException:
	print("modal not present")

profIDDataCriteria = ["Name", "ID"]
profIds = []

# for idNum in range(1,6050):

for idNum in range(124,125):
	driver.get("https://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolID=" + str(idNum) + "&queryoption=TEACHER")

	while(True):
		try:
			WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Load More"]')))
			time.sleep(0.1) #fixes bug where duplicate comments are loaded because button is pressed too fast
		except TimeoutException:
			print("loadMore button not found")
			break
		try:
			driver.find_element_by_xpath('//div[text()="Load More"]').click()
		except ElementNotVisibleException:
			print("loadMore button not found")
			break
		# except WebDriverException:
		# 	print("loadMore button has been hidden")
		# 	break
		# print("button clicked")
	#offload html into variable
	page_html = driver.page_source
	#html parsing
	page_soup = soup(page_html, "html.parser")

	profList = page_soup.find('div', {'class': 'side-panel'}).findChildren("div", {'class':'result-list'}, recursive=True)[0].contents[1].contents


	for prof in profList:
		if(prof == '\n'):
			continue
		else:
			profID = prof.get('id')
			profID = profID[13:]
			profName = prof.findChildren("span", {'class':'name'}, recursive=True)[0].text
			profName = profName.split("\n")[0]
			profData = [profName, profID]
			profIds.append(profData)
	


profIdMapDF = pd.DataFrame(profIds, columns=profIDDataCriteria)
profIdMapDF.to_csv(path_or_buf = "/Users/JosephLai/Desktop/scraping/profIdMap.csv")





