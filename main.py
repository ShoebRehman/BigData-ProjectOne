# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:39:59 2016

@author: Shoeb
"""

from NeoSandbox import loadFromFiles,findTrusted,deleteAll,findCommon

choice = raw_input('''1. Load From Files\n2. Find Individuals with Similar Interests\n3. Find Trusted Colleagues of Colleagues\n4. Query a User via userID
5. Clear Database\nChoice: ''')
if(choice == '1'):
    csvFiles = ['names.csv','organizations.csv','projects.csv','interests.csv','skills.csv','distance.csv']
    loadFromFiles(csvFiles)
if(choice == '2'):
    userID = int(raw_input('Enter userID you wish you query for: '))
    findCommon(userID)
if(choice == '3'):
    userID = int(raw_input('Enter userID you wish you query for: '))
    findTrusted(userID)
if(choice == '5'):
    choice = raw_input('Are you sure? y/n ')
    if(choice == 'y'):
        deleteAll() 