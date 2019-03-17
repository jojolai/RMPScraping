from urllib.request import urlopen as uReq
import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2272729"

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 20)

t = time.time()

print("begin loading page for first time")
driver.get(url)

wait.until(EC.presence_of_element_located((By.ID, 'cookie-notice')))

driver.execute_script("window.stop();")

print("done loading page")
print('Time consuming:', time.time() - t)

#https://www.ratemyprofessors.com/ShowRatings.jsp?tid=953067 dave sullivan

t = time.time()
print("begin reloading page")
driver.get(url)
print('Time consuming:', time.time() - t)
print("closed cookie modal successfully by refreshing")


try:
	driver.find_element_by_class_name("tbl-read-more-btn").click()
except NoSuchElementException:
	print("tbl-read-more-btn not found, trying loadMore Button")

try:
	driver.find_element_by_id("loadMore").click()
except NoSuchElementException:
	print("loadMore button not found")


# try:
# 	driver.find_element_by_class_name("tbl-read-more-btn").click()
# except ElementNotVisibleException:
# 	print("not tbl-read-more-btn... trying loadMore")

# try:
# 	driver.find_element_by_id("loadMore").click()
# except ElementNotVisibleException:
# 	print("not loadMore btn")



#offload html into variable
page_html = driver.page_source
#html parsing
page_soup = soup(page_html, "html.parser")

#find different parts of prof page

prof_name = page_soup.find('h1',{'class':'profname'})
prof_name_str = ''
for span in prof_name.contents:
	if(isinstance(span, bs4.element.Tag) and span.contents[0].strip() != ''):
		prof_name_str += span.contents[0].strip() + ' '
#finished parsing professor's name stored in prof_name_str	
print("done parsing professor's name: ", prof_name_str)


#0-5 overall quality score, 0-100% "would take again" score, and 0-5 "level of difficulty" score
#0-5 OQ score
overall_quality_score = page_soup.findAll('div', {'class': 'grade'})[0].contents[0]
#0-100% WTA score w/o percentage sign aftwards
would_take_again_score = page_soup.findAll('div', {'class': 'grade'})[1].contents[0].split()[0][:-1]
#0-5 LOD score
level_of_difficulty_score = page_soup.findAll('div', {'class': 'grade'})[2].contents[0].split()[0]
print("done parsing professor's scores: OQ = ", overall_quality_score, "; WTA = ", would_take_again_score, "; LOD = ", level_of_difficulty_score)


comment_table = page_soup.find('table', {'class': 'tftable'})

