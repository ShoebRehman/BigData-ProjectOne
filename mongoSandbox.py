import pymongo, csv

client = pymongo.MongoClient()
db = client["projectOne"]
users= db["Users"]
organizations= db["Organizations"]
interests= db["Interests"]
projects= db["Projects"]
skills= db["Skill"]

def main():
    client = pymongo.MongoClient()
    db = client["projectOne"]

    #reads data from file as input from the user provided
    user= db["Users"]
    organizations= db["Organizations"]
    interests= db["Interests"]
    projects= db["Projects"]
    skill= db["Skill"]
    while True:
        val = raw_input("\nWould you like to search for a user (y/n):  ")
        if val == 'y':
            lookUpUser(user, organizations, interests, skill, projects)
        else:
            break


def lookUpUser(userID):
    if((users.find({"User_id": str(userID)})).count() == 0):
        print "This user does not exist. Please try another userID."

    else:
        user_results = users.find({"User_id": str(userID)})   
        organization_result = organizations.find({"User_id": str(userID)})
        interests_results = interests.find({"User_id": str(userID)})
        skill_results = skills.find({"User_id": str(userID)})
        projects_results = projects.find({"User_id": str(userID)})
        
        for u in user_results:
            print("\tName: %s %s" %(u['First name'], u['First name']))
    
        for o in organization_result:
            print("\tWorks at: %s" %o["organization"])
    
        interest_collection=  ""
	for i in interests_results:
		if isinstance(i["Interest"], list):
			for items in range(len(i["Interest"])):
				interest_collection+= i["Interest"][items] + "(" + i["Interest level"][items] + "),"
		else:
			interest_collection = i["Interest"] + "(" + i["Interest level"] + ")"
			
	print("\tInterest: %s" %interest_collection)

	skill_collection = ""
	for sk in skill_results:
		if isinstance(sk["Skill"], list):
		 	for items in range(len(sk["Skill"])):
		 		skill_collection += sk["Skill"][items] + "(" + sk["Skill level"][items] + "), "
		else:
			skill_collection = sk["Skill"] + "(" + sk["Skill level"] + ")"
	print("\tSkill: %s" %skill_collection)
	

	for p in projects_results:
		print("\tWorks on: %s" %p["Project"])


def readFile(file_name):
    r_file = open(file_name)
    csv_file = csv.reader(r_file)
    
    headers = next(csv_file)


    keys = []
    data_entry = {}
    size = 0
    data_collection = []

    for key in headers:
        keys.append(key)

    size = len(keys)
    for rows in csv_file:
        for i in range(size):
            data_entry[keys[i]] = rows[i]
        data_collection.append(data_entry)
        data_entry = {}

    r_file.close()
    return data_collection


def insertData(collection_name, entries):
    print entries
    collection_name.create_index("User_id", unique= True)
    for data in entries:
        collection_name.insert_one(data)
        
def loadFiles(csvfiles):    
    insertData(users,readFile(csvfiles[0]))
    insertData(organizations,readFile(csvfiles[1]))
    insertData(projects,readFile(csvfiles[2]))
    insertData(interests,readIntOrSkill(csvfiles[3],"interest"))
    insertData(skills,readIntOrSkill(csvfiles[4],"skill"))

def readIntOrSkill(file_name, tag):
	r_file = open(file_name, "r")
	csv_file = csv.reader(r_file)
	headers = next(csv_file)
	
	keys = headers
	
	
	data_collection = []
	interests.create_index([("User_id", pymongo.ASCENDING), ("interest", pymongo.DESCENDING)], unique=True)
	skills.create_index([("User_id", pymongo.ASCENDING), ("skill", pymongo.DESCENDING)], unique=True)
	for rows in csv_file:
		data = {}
		for column in range(len(rows)):
			data[keys[column]] = rows[column]
		if findMatchingId(data, data_collection, tag):
			data_collection.append(data)

	r_file.close()
	return data_collection


#checks if there is a matching user id and then creates a list for skill/interest along with level
def findMatchingId(info, arr, tag):
	if tag == "interest":
		for elements in arr:
			if elements["User_id"] == info["User_id"]:
				if not isinstance(elements["Interest"], list):
					elements["Interest"] = [elements["Interest"], info["Interest"]]
					elements["Interest level"] = [elements["Interest level"], info["Interest level"]]
				else:
					if info["Interest"] not in elements["Interest"]:
						elements["Interest"].append(info["Interest"])
						elements["Interest level"].append(info["Interest level"])
				return False
		return True

	elif tag == "skill":
		for elements in arr:
			if elements["User_id"] == info["User_id"]:
				if not isinstance(elements["Skill"], list):
					elements["Skill"] = [elements["Skill"], info["Skill"]]
					elements["Skill level"] = [elements["Skill level"], info["Skill level"]]
				else:
					if info["Skill"] not in elements['Skill']:
						elements["Skill"].append(info["Skill"])
						elements["Skill level"].append(info["Skill level"])
				return False
		return True

def insertData(collection_name, entries):
	if collection_name != skills or collection_name != interests:
		collection_name.create_index("User_id", unique= True)

	for data in entries:
		try:
			collection_name.insert_one(data)
		except:
                    print data
                    pass
def dropDB():
    client.drop_database("projectOne")
