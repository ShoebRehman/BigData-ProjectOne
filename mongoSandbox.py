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
    if((users.find({"userID": str(userID)})).count() == 0):
        print "This user does not exist. Please try another userID."

    else:
        user_results = users.find({"userID": str(userID)})   
        organization_result = organizations.find({"userID": str(userID)})
        interests_results = interests.find({"userID": str(userID)})
        skill_results = skills.find({"userID": str(userID)})
        projects_results = projects.find({"userID": str(userID)})
        
        for u in user_results:
            print("\tName: %s %s" %(u['fName'], u['lName']))
    
        for o in organization_result:
            print("\tWorks at: %s" %o["organization"])
    
        interest_collection=  ""
	for i in interests_results:
		if isinstance(i["interest"], list):
			for items in range(len(i["interest"])):
				interest_collection+= i["interest"][items] + "(" + i["interest_level"][items] + "),"
		else:
			interest_collection = i["interest"] + "(" + i["interest_level"] + ")"
			
	print("\tInterest: %s" %interest_collection)

	skill_collection = ""
	for sk in skill_results:
		if isinstance(sk["skill"], list):
		 	for items in range(len(sk["skill"])):
		 		skill_collection += sk["skill"][items] + "(" + sk["skill_level"][items] + "), "
		else:
			skill_collection = sk["skill"] + "(" + sk["skill_level"] + ")"
	print("\tSkill: %s" %skill_collection)
	

	for p in projects_results:
		print("\tWorks on: %s" %p["project"])


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
    collection_name.create_index("userID", unique= True)
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
	interests.create_index([("userID", pymongo.ASCENDING), ("interest", pymongo.DESCENDING)], unique=True)
	skills.create_index([("userID", pymongo.ASCENDING), ("skill", pymongo.DESCENDING)], unique=True)
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
			if elements["userID"] == info["userID"]:
				if not isinstance(elements["interest"], list):
					elements["interest"] = [elements["interest"], info["interest"]]
					elements["interest_level"] = [elements["interest_level"], info["interest_level"]]
				else:
					if info["interest"] not in elements["interest"]:
						elements["interest"].append(info["interest"])
						elements["interest_level"].append(info["interest_level"])
				return False
		return True

	elif tag == "skill":
		for elements in arr:
			if elements["userID"] == info["userID"]:
				if not isinstance(elements["skill"], list):
					elements["skill"] = [elements["skill"], info["skill"]]
					elements["skill_level"] = [elements["skill_level"], info["skill_level"]]
				else:
					if info["skill"] not in elements['skill']:
						elements["skill"].append(info["skill"])
						elements["skill_level"].append(info["skill_level"])
				return False
		return True

def insertData(collection_name, entries):
	if collection_name != skills or collection_name != interests:
		collection_name.create_index("userID", unique= True)

	for data in entries:
		try:
			collection_name.insert_one(data)
		except:
                    pass
def dropDB():
    client.drop_database("projectOne")
