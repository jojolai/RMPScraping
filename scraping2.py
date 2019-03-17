from urllib.request import urlopen as uReq
import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


executable_path = "/usr/local/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('/Users/JosephLai/Desktop/scraping/cjpalhdlnbpafiamejdnhcphjbkeiagm-1.18.4-www.Crx4Chrome.com.crx')

driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

t = time.time()
url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=601493&showMyProfs=true" #"https://www.ratemyprofessors.com/ShowRatings.jsp?tid=953067"
driver.get(url)
print('Time consuming:', time.time() - t)
print("done opening")

print("refreshing")
driver.refresh()
print("done refreshing")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'reveal-modal-bg')))

js = "var aa=document.getElementsByClassName('reveal-modal-bg')[0]; aa.parentNode.removeChild(aa)"
driver.execute_script(js)

try:
	driver.find_element_by_class_name("tbl-read-more-btn").click()
except NoSuchElementException:
	print("tbl-read-more-btn not found, trying loadMore Button")

for i in [1,2]:
	WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'loadMore')))
	try:
		driver.find_element_by_id("loadMore").click()
	except ElementNotVisibleException:
		print("loadMore button not found")
		break;

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

#comment parsing begins here
comment_table = page_soup.find('table', {'class': 'tftable'}) #finds table with comments
#cleanses comment table to create list of unique comments
comment_list = [] #list of unique comments 
comment_set = set() 
for comment in comment_table.find_all("tr", {"class": ["","even"]}):
	c_id = comment['id']
	if(c_id in comment_set): 
		continue #prevents duplicate comments from being added
	else:
		comment_set.add(comment)
		comment_list.append(comment)


