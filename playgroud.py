profDataCriteria = ["FN","LN","School","Department","City","State","OQ","WTA","LOD","gives good feedback","respected","lots of homework","accessible outside class","get ready to read","participation matters","skip class? you wont pass.","inspirational","graded by few things","test heavy","group projects","clear grading criteria","hilarious","beware of pop quizzes","amazing lectures","lecture heavy","caring","extra credit","so many papers","tough grader","number of comments","prof_id","num_female_words","num_male_words","percent_female","gender"]
commentDataCriteria = ["Date","FN","LN","School","OQ","LOD","WTA","Course","for credit"]
commentDataCriteria.extend(["textbook used","grade received","attendence","comment","num found this useful", "num did not find this useful"])
commentDataCriteria.extend(profDataCriteria[9:29])
commentDataCriteria.extend(["comment_id"])



(Date DATE, FN, LN, School, OQ, LOD, WTA, Course, for credit, textbook used, grade received, attendence, comment, num found this useful, num did not find this useful, gives good feedback, respected, lots of homework, accessible outside class, get ready to read, participation matters, "skip class? you wont pass.", inspirational, graded by few things, test heavy, group projects, clear grading criteria, hilarious, beware of pop quizzes, amazing lectures, lecture heavy, caring, extra credit, so many papers, tough grader, comment_id)