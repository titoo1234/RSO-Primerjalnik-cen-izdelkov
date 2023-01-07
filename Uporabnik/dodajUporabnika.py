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
    
    
class AddUser(Resource):
    def post(self):
        try:
            name = request.json["username"]
            password = request.json["password"]
            h = hashlib.md5()
            h.update(password.encode('utf-8'))
            h = h.hexdigest()
            #query = f"SELECT Id,Ime FROM Uporabniki;"
            #query = "INSERT INTO Uporabniki (ime, geslo, admin) VALUES ('test3', '1234567', 0);"
            up.uses_netloc.append("postgres")
            url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            cur.execute("INSERT INTO Uporabniki (ime, geslo, admin) VALUES (%s, %s, %s);", (name, h, 0))
            cur.close()
            conn.close()
            #če ni prišlo do napake je vse ok
            # df = pd.read_sql_query(query, conn)
            # print(df)
            # result = df.to_dict("records")
            # print(result)
            result = AppResult.create_true_result()
            return result.toJSON(), 200
        except Exception as e:
            return AppResult.create_error_result(str(e)).toJSON(), 500


