from flask import request
#from flask_restful import Resource
from flask_restx import Resource
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from Models.AppResult import AppResult
from Models.SQLRepository import SQLRepository
from textwrap import dedent
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from Models.Exceptions import *
import hashlib
import pandas as pd
import psycopg2
import urllib.parse as up
import requests
import connections
    
    
class AddUser(Resource):
    def post(self):
        try:
            name = request.json["username"]
            password = request.json["password"]
            #h = hashlib.md5()
            #h.update(password.encode('utf-8'))
            #h = h.hexdigest()

            conn = connections.start_connDB()
            cur = conn.cursor()
            cur.execute("INSERT INTO Uporabniki (ime, geslo, admin) VALUES (%s, %s, %s);", (name, password, 0))
            cur.close()
            conn.close()

            return [True], 200
        except:
            return [False], 500


