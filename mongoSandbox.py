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
    
        interests_collection = ""
        
        for i in interests_results:
            interests_collection += str(i['interest']) + "(" +str(i['Interest level']) + "),"
        print("\tInterests: %s" % interests_collection)
    
        skill_collection = ""
        
        for sk in skill_results:
             skill_collection += str(sk['skill']) + "(" +str(sk['skill_level']) + "),"
        print("\tSkill : %s" %skill_collection)    
    
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
    for data in entries:
        collection_name.insert_one(data)
        
def loadFiles(csvfiles):    
    insertData(users,readFile(csvfiles[0]))
    insertData(organizations,readFile(csvfiles[1]))
    insertData(projects,readFile(csvfiles[2]))
    insertData(interests,readFile(csvfiles[3]))
    insertData(skills,readFile(csvfiles[4]))
    
def dropDB():
    client.drop_database("projectOne") 
