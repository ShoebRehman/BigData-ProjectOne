# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:39:59 2016

@author: Shoeb
"""

from databaseSandbox import loadFiles,findTrusted,deleteAll,findCommon
from mongoSandbox import lookUpUser

def menu():
    while(True):
        choice = raw_input('''1. Load From Files\n2. Find Individuals with Similar Interests\n3. Find Trusted Colleagues of Colleagues\n4. Query a User via userID\n5. Clear Databases\n6. Exit\nChoice: ''')
        if(choice == '1'):
            csvFiles = ['names.csv','organizations.csv','projects.csv','interests.csv','skills.csv','distance.csv']
            loadFiles(csvFiles)
        if(choice == '2'):
            userID = int(raw_input('Enter userID you wish you query for: '))
            findCommon(userID)
        if(choice == '3'):
            userID = int(raw_input('Enter userID you wish you query for: '))
            findTrusted(userID)
        if(choice == '4'):
            userID = raw_input('Enter userID you wish you query for: ')
            lookUpUser(userID)
        if(choice == '5'):
            choice = raw_input('Are you sure? y/n ')
            if(choice == 'y'):
                deleteAll()
        if(choice == '6'):
            return False

menu()