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
import csv
import json
from sklearn.feature_extraction.text import CountVectorizer
import MySQLdb
import datetime

mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="joe1234lai",
  db = "mysql"
)
mycursor = mydb.cursor()

mycursor.execute("USE RMP")

urls = ["https://www.ratemyprofessors.com/ShowRatings.jsp?tid=601493&showMyProfs=true","https://www.ratemyprofessors.com/ShowRatings.jsp?tid=558674&showMyProfs=true","https://www.ratemyprofessors.com/ShowRatings.jsp?tid=64638&showMyProfs=true"]

profIds =[]


with open('profIdMap.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        profIds.append(row[2])
profIds = profIds[1:]

#boot chrome driver with adblock
executable_path = "/usr/local/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('/Users/JosephLai/Desktop/scraping/cjpalhdlnbpafiamejdnhcphjbkeiagm-1.18.4-www.Crx4Chrome.com.crx')

driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

t = time.time()
bootUrl = urls[0]  #"https://www.ratemyprofessors.com/ShowRatings.jsp?tid=953067"
driver.get(bootUrl)
print('Time consuming:', time.time() - t)
print("done opening")

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



#initialize data frame labels
profDataCriteria = ["FN","LN","School","Department","City","State","OQ","WTA","LOD","gives good feedback","respected","lots of homework","accessible outside class","get ready to read","participation matters","skip class? you won't pass.","inspirational","graded by few things","test heavy","group projects","clear grading criteria","hilarious","beware of pop quizzes","amazing lectures","lecture heavy","caring","extra credit","so many papers","tough grader","number of comments","prof_id","num_female_words","num_male_words","percent_female","gender"]
commentDataCriteria = ["Date","FN","LN","School","OQ","LOD","WTA","Course","for credit"]
commentDataCriteria.extend(["textbook used","grade received","attendence","comment","num found this useful", "num did not find this useful"])
commentDataCriteria.extend(profDataCriteria[9:29])
commentDataCriteria.extend(["comment_id"])

femaleIDWords = ["her", "hers", "she", "she'll", "she's"]
maleIDWords = ["he", "him", "his", "he'll", "he's"]
# #initialize allProfData and allCommentData
# allProfData = []
# allCommentData = []


# with open('commentData.csv', mode='a') as commentDataCSV:
# with open('testCommentData.csv', mode='a') as commentDataCSV:
# 	# with open ('profData.csv', mode='a') as profDataCSV:
# 	with open ('testProfData.csv', mode='a') as profDataCSV:
# comment_data_writer = csv.writer(commentDataCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# prof_data_writer = csv.writer(profDataCSV)
# write headers 
# comment_data_writer.writerow(commentDataCriteria)
# prof_data_writer.writerow(profDataCriteria)


for prof in [601493]: # profIds:
	driver.get("https://www.ratemyprofessors.com/paginate/professors/ratings?tid="+ str(prof) +"&filter=&courseCode=&page=1")
	data = json.loads(driver.page_source.split(">")[5][:-5])
	if(len(data["ratings"]) == 0):
		print("found prof with no ratings, done parsing")
		break
	url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid="+ str(prof) +"&showMyProfs=true"
	driver.get(url)

	#offload html into variable
	page_html = driver.page_source
	#html parsing
	page_soup = soup(page_html, "html.parser")

	#row in profDataDF
	profData = [0]*35 
	numComments =  page_soup.find('div', {'class': 'table-toggle rating-count active'}).text.split("\n")[1].strip().split(" ")[0]
	profData[29] = numComments
	profData[30] = prof #stores id
	#find different parts of prof page
	prof_name = page_soup.find('h1',{'class':'profname'})
	prof_name_str = ''
	for span in prof_name.contents:
		if(isinstance(span, bs4.element.Tag) and span.contents[0].strip() != ''):
			prof_name_str += span.contents[0].strip() + ' '
	#finished parsing professor's name stored in prof_name_str	
	prof_first_name = prof_name_str.split(' ')[0]
	prof_last_name = prof_name_str.split(' ')[1]
	print("parsing prof, first name: ", prof_first_name, "; last name: ", prof_last_name)
	profData[0] = prof_first_name
	profData[1] = prof_last_name

	#find prof's school, department, city, and state
	prof_school = page_soup.find('a', {'class': 'school'}).contents[0]
	profData[2] = prof_school

	prof_dep = page_soup.find('div', {'class': 'result-title'}).contents[0]
	prof_dep = prof_dep.split("the")[1].split("department")[0].strip()
	profData[3] = prof_dep

	prof_city = page_soup.find('h2', {'class': 'schoolname'}).contents[2].split(",")
	prof_state = prof_city[2].strip()
	prof_city = prof_city[1].strip()
	profData[4] = prof_city
	profData[5] = prof_state

	#0-5 overall quality score, 0-100% "would take again" score, and 0-5 "level of difficulty" score
	#0-5 OQ score
	overall_quality_score = page_soup.findAll('div', {'class': 'grade'})[0].contents[0]
	#0-100% WTA score w/o percentage sign aftwards
	would_take_again_score = page_soup.findAll('div', {'class': 'grade'})[1].contents[0].split()[0][:-1]
	#0-5 LOD score
	level_of_difficulty_score = page_soup.findAll('div', {'class': 'grade'})[2].contents[0].split()[0]
	print("done parsing professor's scores: OQ = ", overall_quality_score, "; WTA = ", would_take_again_score, "; LOD = ", level_of_difficulty_score)
	profData[6] = overall_quality_score
	profData[7] = would_take_again_score
	profData[8] = level_of_difficulty_score

	#create dictionary that maps tags to index
	tag_map = {}
	for num in range(9,29):
		tag_map[profDataCriteria[num]] = num
	#parse tag box to find tags and corresponding counts
	tag_box = page_soup.find('div', {'class': 'tag-box'}).contents
	for tag in tag_box:
		if(tag == '\n'):
			continue
		else:
			index = tag_map[tag.contents[0].strip().lower()]
			profData[index] = tag.contents[1].contents[0].split("(")[1].split(")")[0]

	# allProfData.append(profData)
	
	pageNum = 1
	numCommentsFound = 0
	maleWordCount = 0
	femaleWordCount = 0
	while(True):
		jsonUrl = "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="+ str(prof) +"&filter=&courseCode=&page=" + str(pageNum) 
		driver.get(jsonUrl)

		jsonData = json.loads(driver.page_source.split(">")[5][:-5])

		for comment in jsonData["ratings"]:
			numCommentsFound += 1
			commentData = [0]*len(commentDataCriteria)
			#each comment is a row in the commentData dataframe
			commentData[-1] = comment["id"]
			#convert date to mysql format, aka from mm/dd/yyyy to yyyy-mm-dd
			commentData[0] = datetime.datetime.strptime(comment["rDate"], '%m/%d/%Y').strftime('%Y-%m-%d')   
			#data that we already have
			commentData[1] = prof_first_name
			commentData[2] = prof_last_name
			commentData[3] = prof_school
			commentData[4] = comment["rOverall"] #overall quality
			# print(type(commentData[4]))
			commentData[5] = comment["rEasy"] #level of difficulty
			commentData[6] = comment["rWouldTakeAgain"]
			commentData[7] = comment["rClass"]
			commentData[8] = comment["takenForCredit"]
			commentData[9] = comment["rTextBookUse"]
			commentData[10] = comment["teacherGrade"]
			commentData[11] = comment["attendance"]
			commentData[12] = comment["rComments"]
			# removes "\r" from comments because it messes csv formatting up
			commentStr = ""
			for part in commentData[12].split("\r"):
				commentStr = commentStr + part
			commentData[12] = commentStr
			#count gender words
			#initialize word count dictionary for comment
			vectorizer = CountVectorizer()
			try:
				vectorizer.fit([commentStr])
				wordCountDict = vectorizer.vocabulary_
				for maleWord in maleIDWords:
					maleWordCount += wordCountDict.get(maleWord, 0)
				for femaleWord in femaleIDWords:
					femaleWordCount += wordCountDict.get(femaleWord, 0)
			except ValueError:
				pass
			commentData[13] = comment["helpCount"]
			commentData[14] = comment["notHelpCount"]
			tag_box = comment["teacherRatingTags"]
			for tag in tag_box:
				index = tag_map[tag.lower()] + 6
				commentData[index] = 1
			# allCommentData.append(commentData)
			# write to csv
			# print(tuple (commentData))
			# comment_data_writer.writerow(commentData) # for writing into csv
			# print((tuple (commentData)))
			mycursor.execute("INSERT INTO `commentData` VALUES {0};".format(tuple (commentData)))
			mydb.commit()
		if(jsonData["remaining"] == 0):
			print("done parsing comments: found ", numCommentsFound, " out of ", numComments, " comments")
			if(str(numCommentsFound) != numComments):
				raise Exception('Number of comments parsed does not match number of comments found')
			break
		else:
			pageNum += 1
	#determine gender mechanism
	gender = "unknown"
	percentFemale = 0.5
	totalGenderWordCount = femaleWordCount + maleWordCount
	if(totalGenderWordCount != 0):
		percentFemale = femaleWordCount/totalGenderWordCount
	if(percentFemale >= 0.7):
		gender = "female"
	elif (percentFemale <= 0.3):
		gender = "male"
	profData[31] = femaleWordCount
	profData[32] = maleWordCount
	profData[33] = percentFemale
	profData[34] = gender
	# print(tuple (profData))
	# prof_data_writer.writerow(profData) #for writing to csv
	# print((tuple (profData)))
	mycursor.execute("INSERT INTO `profData` VALUES {0};".format(tuple (profData)))
	mydb.commit()

#create pandas dataframe for professor data(FN,LN, School, OQ, WTA, LOD, Tags)
# profDataDF = pd.DataFrame(allProfData, columns=profDataCriteria)# profData = pd.DataFrame([range(1,27), range(28,54)], columns=profDataList)
# commentDataDF = pd.DataFrame(allCommentData, columns=commentDataCriteria)

# profDataDF.to_csv(path_or_buf = "/Users/JosephLai/Desktop/scraping/profData.csv")
# commentDataDF.to_csv(path_or_buf = "/Users/JosephLai/Desktop/scraping/commentData.csv")

#used to calculate performance
print('Time consumed:', time.time() - t)
mydb.commit()
mydb.close()
driver.close()

