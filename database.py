# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 13:30:13 2016

@author: Shoeb
"""
from mongoSandbox import loadFiles,dropDB
from Neo4JSandbox import loadFromFiles,deleteAllNodes

def loadData(csvfiles):
    loadFromFiles(csvfiles)
    loadFiles(csvfiles)

def deleteAll():
    dropDB()
    deleteAllNodes()
    



