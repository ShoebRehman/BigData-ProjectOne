# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:56:20 2016

@author: Shoeb
"""
from py2neo import Graph,Node,Relationship,authenticate
authenticate("localhost:7474","neo4j","shoebr")
graph_db = Graph()

query = '''match (a:user)-[`WORKS AT`]-(m:organization) where a.userID = %d 
WITH m.organization as Org
match (n:organization)-[a:DISTANCE]-(m:organization) where a.distance < 10 and n.organization = Org
WITH m.organization as closeOrgs, Org
match (a:organization)-[`WORKS AT`]-(c:user) 
where a.organization = closeOrgs or a.organization = Org
WITH DISTINCT c.userID as closeUsers
match (a:user)--(b:interest)--(c:user) where a.userID = %d and c.userID = closeUsers
return DISTINCT c'''%(3,3)

for record in graph_db.cypher.execute(query):
    print record[0]['fName']