# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:23:01 2016

@author: Shoeb
"""

from py2neo import Graph,Node,Relationship,authenticate
import csv

authenticate("localhost:7474","neo4j","shoebr")
graph_db = Graph()

try: #create uniqueness constraints on these nodes
    graph_db.schema.create_uniqueness_constraint("user","userID")
    graph_db.schema.create_uniqueness_constraint("interest","interest")
    graph_db.schema.create_uniqueness_constraint("skill","skill")
    graph_db.schema.create_uniqueness_constraint("organization","organization")
    graph_db.schema.create_uniqueness_constraint("organizationType","organizationType")
    graph_db.schema.create_uniqueness_constraint("project","project")
except:#error ConstraintViolationException is thrown when already created. this ensures the DB has the constraints
    pass


def loadFromFiles(csvfiles):
    with open(csvfiles[0],'r') as n: #names.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n:user) WHERE n.userID = " + row[0] + " return n")) == 0):#if user doesn't exist, create user
                person = Node("user","userID", userID=int(row[0]))
                person.properties['lName'] = row[2]
                person.properties['fName'] = row[1]
                graph_db.create(person)
    
    with open(csvfiles[1],'r') as n: #organizations.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n:user) WHERE n.userID = " + row[0] + " return n")) != 0): #if user exists, add organization of user
                user = graph_db.merge_one("user","userID", int(row[0]))
                
                if(len(graph_db.cypher.execute("MATCH (n {organization:\"" + row[1] + "\"}) return n")) == 0): #if organization doesn't exist, create it
                    p_organization = Node("organization", "organization", organization=row[1])
                    worksAt = Relationship(user, "WORKS AT", p_organization)
                    graph_db.create(worksAt)
                    
                    if(len(graph_db.cypher.execute("MATCH (n {organizationType:\"" + row[2] + "\"}) return n")) == 0): #if organization type doesn't exist, create it
                        org_type = Node("organizationType","organizationType",organizationType=row[2])
                        partOf = Relationship(p_organization,"PART OF",org_type)
                        graph_db.create(partOf)
                    else: #if it does exist, merge
                        if(len(graph_db.cypher.execute("MATCH (a{organization:\""+row[1]+"\"})--(b{organizationType:\"" + row[2] + "\"}) return a")) == 0):
                            org_type = graph_db.merge_one("organizationType","organizationType",row[2])
                            partOf = Relationship(p_organization,"PART OF",org_type)
                            graph_db.create(partOf)
                    
                else:#if organization exists, merge with existing
                    if(len(graph_db.cypher.execute("MATCH (a{userID:"+row[0]+"})--(b{organization:\"" + row[1] + "\"}) return a")) == 0):#makes sure any duplicate relationships aren't created
                        p_organization = graph_db.merge_one("organization", "organization", row[1])
                        worksAt = Relationship(user, "WORKS AT", p_organization)
                        graph_db.create(worksAt)
                        
                    if(len(graph_db.cypher.execute("MATCH (a{organization:\""+row[1]+"\"})--(b{organizationType:\"" + row[2] + "\"}) return a")) == 0):#makes sure any duplicate relationships aren't created
                        org_type = graph_db.merge_one("organizationType","organizationType",row[2])
                        partOf = Relationship(p_organization,"PART OF",org_type)
                        graph_db.create(partOf)
    
    with open(csvfiles[2],'r') as n: #projects.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n:user) WHERE n.userID = " + row[0] + " return n")) != 0):
                user = graph_db.merge_one("user","userID", int(row[0]))
                if(row[1] == ""): #skips entry if user isn't working on project
                    continue
                if(len(graph_db.cypher.execute("MATCH (n {project:\"" + row[1] + "\"}) return n")) == 0): #if project doesn't exist, create it
                    p_project = Node("project", "project", project=row[1])
                    worksOn = Relationship(user, "WORKS ON", p_project)
                    graph_db.create(worksOn)
                else:#if project exists, add user to project
                    if(len(graph_db.cypher.execute("MATCH (a{userID:"+row[0]+"})--(b{project:\"" + row[1] + "\"}) return a")) == 0): 
                        p_project = graph_db.merge_one("project","project",row[1])
                        worksOn = Relationship(user, "WORKS ON", p_project)
                        graph_db.create(worksOn)
    
    with open(csvfiles[4],'r') as n: #skills.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n:user) WHERE n.userID = " + row[0] + " return n")) != 0):#only add skill to user if user exists
                user = graph_db.merge_one("user","userID", int(row[0]))
                if(len(graph_db.cypher.execute("MATCH (n {skill:\"" + row[1] + "\"}) return n")) == 0): #if skill doesn't exist ,create it
                    p_skill = Node("skill", "skill", skill=row[1])
                    hasSkill = Relationship(user, "HAS", p_skill)
                    hasSkill.properties['level'] = int(row[2])
                    graph_db.create(hasSkill)
                else:#add skill to user if skill exists
                    if(len(graph_db.cypher.execute("MATCH (a{userID:"+row[0]+"})--(b{skill:\"" + row[1] + "\"}) return a")) == 0): 
                        p_skill = graph_db.merge_one("skill","skill",row[1])
                        hasSkill = Relationship(user, "HAS", p_skill)
                        hasSkill.properties['level'] = int(row[2])
                        graph_db.create(hasSkill)
                    
    with open(csvfiles[3],'r') as n: #interests.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n:user) WHERE n.userID = " + row[0] + " return n")) != 0):
                user = graph_db.merge_one("user","userID", int(row[0]))
                
                if(len(graph_db.cypher.execute("MATCH (n {interest:\"" + row[1] + "\"}) return n")) == 0): #if interest doesn't exist, create it
                    p_interest = Node("interest", "interest", interest=row[1])
                    hasInterest = Relationship(user, "HAS", p_interest)
                    hasInterest.properties['level'] = int(row[2])
                    graph_db.create(hasInterest)
                else:#if interest exists, add interest to user
                    if(len(graph_db.cypher.execute("MATCH (a{userID:"+row[0]+"})--(b{interest:\"" + row[1] + "\"}) return a")) == 0): 
                        p_interest = graph_db.merge_one("interest","interest",row[1])
                        hasInterest = Relationship(user, "HAS", p_interest)
                        hasInterest.properties['level'] = int(row[2])
                        graph_db.create(hasInterest)
    with open(csvfiles[5],'r') as n:#distance.csv
        reader = csv.reader(n)
        reader.next()
        for row in reader:
            if(len(graph_db.cypher.execute("MATCH (n {organization:\"" + row[0] + "\"}) return n")) != 0 and 
            len(graph_db.cypher.execute("MATCH (n {organization:\"" + row[1] + "\"}) return n")) != 0): #if both organizations exist, add distance relationship between organizations
                if(len(graph_db.cypher.execute('''MATCH (a{organization:"%s"})--(b{organization:"%s"}) return a'''%(row[0],row[1]))) == 0):#if the relationship between the two organizations don't exist, make one
                    org1 = graph_db.merge_one("organization","organization", row[0])
                    org2 = graph_db.merge_one("organization","organization", row[1])
                    dist = Relationship(org1,"DISTANCE",org2)
                    dist.properties['distance'] = float(row[2])
                    graph_db.create(dist)



def findTrusted(userID):
    if(len(graph_db.cypher.execute("match (a:user) where a.userID = %d return a.userID"%(userID))) == 0):
        print "This user does not exist. Please try another userID."
    else:
        org = graph_db.cypher.execute("match (a:user)--(b:organization) where a.userID = %d return b.organization"%(userID))[0]
        query = '''match (a:user)--(b:organization) where a.userID = %d
        WITH b.organization as orgName
        match (c:user)--(d:organization) where d.organization = orgName and c.userID <> %d
        WITH c.userID as userIDs
        match (e:user)--(f:project) where e.userID = userIDs 
        WITH f.project as project,userIDs as users
        match (g:user)--(h:project) where h.project = project and g.userID <> users
        with g as trusted
        match (a:user)--(b:interest) where a.userID = %d
        with b as interests,trusted
        match (c:user)--(d:interest) where d=interests and c.userID <> %d and c=trusted
        with  DISTINCT c as trustedUsers,collect(d.interest) as interests
        match (a:user)--(b:organization) where a = trustedUsers
        with trustedUsers,b.organization as trustedOrgs,interests
        match (a:user)--(b:project) where a = trustedUsers
        return a as trustedUsers,trustedOrgs,b.project as projects,interests''' % (userID,userID,userID,userID)
        print "Organization of user entered is: %s" % (org[0])
        if(len(graph_db.cypher.execute(query)) == 0):
            print "There are no trusted colleagues of the user you chose"
        else:
            print "Trusted colleagues of colleagues of selected user is:"
            for record in graph_db.cypher.execute(query):
                print "\tName: "+record[0]['fName'],record[0]['lName']
                print "\tUser ID: "+str(record[0]['userID'])
                print "\tOrganization: "+record[1]
                print "\tProject: " + record[2]
                print "\tCommon Interests with User:",", ".join(record[3])
                print ""

def deleteAllNodes():
    query = "match n detach delete n"
    graph_db.cypher.execute(query)    

def findCommon(userID):
    if(len(graph_db.cypher.execute("match (a:user) where a.userID = %d return a.userID"%(userID))) == 0):
        print "This user does not exist. Please try another userID."
    else:
        query = '''match (a:user)-[`WORKS AT`]-(m:organization)--(n:organizationType) where a.userID = %d
        WITH m.organization as Org, n.organizationType as orgType
        match (n:organization)-[a:DISTANCE]-(m:organization)--(t:organizationType) where a.distance <= 10 and n.organization = Org and t.organizationType = orgType
        WITH m.organization as closeOrgs, Org
        match (a:organization)-[`WORKS AT`]-(c:user) 
        where a.organization = closeOrgs or a.organization = Org
        WITH DISTINCT c.userID as closeUsers, a.organization as org
        match (a:user)--(b:interest)-[r:HAS]-(c:user) where a.userID = %d and c.userID = closeUsers
        return c as users, sum(r.level) as userSum, org, collect(b.interest) as interests
        ORDER BY userSum DESC
        ''' % (userID,userID)
        if(len(graph_db.cypher.execute(query)) == 0):
            print "There are no users close to the one you chose who have similar interests"
            
        else:
            print "The following people are within 10 miles of the user entered and have similar interests, sorted by weight of interests: \n"
            for record in graph_db.cypher.execute(query):
                print record[0]['fName'],record[0]['lName'],":"
                print "\tOrganization of user: " + record[2]
                print "\tSum of Weights of Interests in common with user: " + str(record[1])
                print "\tInterests in common:",", ".join(record[3])
                print ""
        
        print "\n"
        query = '''match (a:user)-[`WORKS AT`]-(m:organization)--(n:organizationType) where a.userID = %d
        WITH m.organization as Org, n.organizationType as orgType
        match (n:organization)-[a:DISTANCE]-(m:organization)--(t:organizationType) where a.distance <= 10 and n.organization = Org and t.organizationType = orgType
        WITH m.organization as closeOrgs, Org
        match (a:organization)-[`WORKS AT`]-(c:user) 
        where a.organization = closeOrgs or a.organization = Org
        WITH DISTINCT c.userID as closeUsers, a.organization as org
        match (a:user)--(b:skill)-[r:HAS]-(c:user) where a.userID = %d and c.userID = closeUsers
        return c as users, sum(r.level) as userSum, org, collect(b.skill) as skills
        ORDER BY userSum DESC
        ''' % (userID,userID)
        if(len(graph_db.cypher.execute(query)) == 0):
            print "There are no users similar to the one you chose who have smiliar skills"
        else:
            print "The following people are within 10 miles of the user entered and have similar skills, sorted by weight of skill: \n"
            for record in graph_db.cypher.execute(query):
                print record[0]['fName'],record[0]['lName'],":"
                print "\tOrganization of user: " + record[2]
                print "\tSum of Weights of Skills in common with user: " + str(record[1])
                print "\tSkills in common: ",", ".join(record[3])
                print ""
