#-*- coding: utf-8 -*-
import os

SERVER_AUTO = True

if SERVER_AUTO:
    SERVER_TYPE = os.environ.get('S_TYPE')
    
if SERVER_TYPE == None or SERVER_AUTO ==False:
    SERVER_TYPE = "LOCAL"   ## AUTO, LOCAL,  STAGING,  REAL,  UNITTEST

  
if SERVER_TYPE == "LOCAL" :
    DB_NAME = "todo"
    DB_USER = "todouser"
    DB_PASSWORD = "Todo-0316_18"
    DB_HOST = "localhost"
    DB_PORT = 3306

elif SERVER_TYPE == "UNITTEST" :
    DB_NAME = "todo_unittest"
    DB_USER = "todouser"
    DB_PASSWORD = "Todo-0316_18"
    DB_HOST = "localhost"
    DB_PORT = 3306
    
elif SERVER_TYPE == "REAL":
    DB_NAME = "todo"
    DB_USER = "todouser"
    DB_PASSWORD = "Todo-0316_18"
    DB_HOST = "localhost"
    DB_PORT = 3306

