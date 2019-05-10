import MySQLdb

mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="joe1234lai",
  db = "mysql"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE RMP;")

mycursor.execute("CREATE DATABASE RMP;")

print("finished")


mycursor.execute("USE RMP")
# mycursor.execute("DROP TABLE profData")
# mycursor.execute("DROP TABLE commentData")
mycursor.execute("CREATE TABLE profData (firstName VARCHAR(30), lastName VARCHAR(30), school VARCHAR(40), department VARCHAR(30), city VARCHAR(30), state VARCHAR(30), overallQuality FLOAT, wouldTakeAgain FLOAT, levelOfDifficulty FLOAT, gives_good_feedback INT, respected INT, lots_of_homework INT, accessible_outside_class INT, get_ready_to_read INT, participation_matters INT, skip_class_you_wont_pass INT, inspirational INT, graded_by_few_things INT, test_heavy INT, group_projects INT, clear_grading_criteria INT, hilarious INT, beware_of_pop_quizzes INT, amazing_lectures INT, lecture_heavy INT, caring INT, extra_credit INT, so_many_papers INT, tough_grader INT, num_of_comments INT, prof_id INT, num_female_words INT, num_male_words INT, percent_female FLOAT, gender VARCHAR(10));")
mycursor.execute("CREATE TABLE commentData (Date DATE, FN VARCHAR(30), LN VARCHAR(30), School VARCHAR(30), OQ FLOAT, LOD FLOAT, WTA VARCHAR(3), Course VARCHAR(10), for_credit VARCHAR(4), textbook_used VARCHAR(4), grade_received VARCHAR(14), attendence VARCHAR(13), comment VARCHAR(450), num_found_this_useful INT, num_did_not_find_this_useful INT, gives_good_feedback INT, respected INT, lots_of_homework INT, accessible_outside_class INT, get_ready_to_read INT, participation_matters INT, skip_class_you_wont_pass INT, inspirational INT, graded_by_few_things INT, test_heavy INT, group_projects INT, clear_grading_criteria INT, hilarious INT, beware_of_pop_quizzes INT, amazing_lectures INT, lecture_heavy INT, caring INT, extra_credit INT, so_many_papers INT, tough_grader INT, comment_id INT);")

# temp = "(firstName VARCHAR(30)", "lastName VARCHAR(30));"
# mycursor.execute("CREATE TABLE temp {0}".format(temp))

# mycursor.execute("INSERT INTO `profData` VALUES  ('Aaron', 'Stevens', 'Boston University', 'Computer Science', 'Boston', 'MA', '3.3', '44', '3.4', '3', '1', '18', '2', '2', '5', '7', 0, 0, '1', 0, '4', '2', '1', '1', '1', '1', '1', 0, '18', '134', 601493, 0, 2556, 0.0, 'male');")


# profDataCriteria = ["FN VARCHAR(30)","LN","School","Department","City","State","OQ","WTA","LOD","gives good feedback","respected","lots of homework","accessible outside class","get ready to read","participation matters","skip class? you won't pass.","inspirational","graded by few things","test heavy","group projects","clear grading criteria","hilarious","beware of pop quizzes","amazing lectures","lecture heavy","caring","extra credit","so many papers","tough grader","number of comments","prof_id","num_female_words","num_male_words","percent_female","gender"]
# commentDataCriteria = ["Date","FN","LN","School","OQ","LOD","WTA","Course","for credit"]
# commentDataCriteria.extend(["textbook used","grade received","attendence","comment","num found this useful", "num did not find this useful"])
# commentDataCriteria.extend(profDataCriteria[9:29])
# commentDataCriteria.extend(["comment_id"])


# value = None
# mycursor.execute("INSERT INTO table (`column1`) VALUES (%s)", (value,))

# thingList = ['Puffball','Diane','hamster','f','1999-03-30', None]



# mycursor.execute("INSERT INTO `pet` VALUES {0};".format(tuple (thingList)))
mydb.close()

