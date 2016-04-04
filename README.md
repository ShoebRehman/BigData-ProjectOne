# BigData-ProjectOne
Build a database to model collaborator.net using Neo4J and MongoDB

To Run:
Launch main.py and run

Options explained:

1) Load data from CSV files into Neo4J Database and MongoDB Database. The script requires each file to be named as the following:

'names.csv' for First and Last Names for each coresponding userID
'organizations.csv' for the organization userID belongs in and type of organization
'projects.csv' for each userID's project that they are working on
'interests.csv' for each userID's interests with level
'skills.csv' for each userID's interests with level
'distance.csv' for each combination of organizations and their distances

2) Find Individuals with Similar Interests
Find all other individuals who share the same interests or skills as the user, and work in the same or different organization within 10 miles from the organization that the user works. 
The individuals should be ranked by the total weight of shared interests (or skills) with the user. In addition, the output should include the organization name, and the list of common interests (or skills).

3) Find Trusted Colleagues of Colleagues
Find all trusted colleagues-of-colleagues who have one or more particular interests. The “trusted colleague” is defined as two persons have worked on the same project.

4) Query a User via userID
For a specific userID, retrieve information of that user

5) Clear Databases
Deletes all data in both databases

6) Exit
