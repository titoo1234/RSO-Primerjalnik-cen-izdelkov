# import sys
# sys.path.append('../')
from flask import request
from flask_restful import Resource
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from Models.AppResult import AppResult
from Models.SQLRepository import SQLRepository
from textwrap import dedent
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from Models.Exceptions import *
import urllib.parse as up
import psycopg2
import pandas as pd




class Uporabnik(Resource):
    def get(self, id=None):

        

        try:
            query = f"SELECT Id,Ime,Admin FROM Uporabniki Where {id} = Id;"
            if id == None:
                query = f"SELECT Id,Ime,Admin FROM Uporabniki"
            up.uses_netloc.append("postgres")
            url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            conn.set_session(autocommit=True)
            # cur = conn.cursor()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            # cur.execute(query)
            # result = cur.fetchall()
            # eng = SQLRepository(conn_str)
            # eng.start_conn()
            # print("conn started success")
            
            # result = eng.execute_query(query)
            # print("execute query succ")
            # eng.close_conn()
            result = AppResult(True, "", result)
            return result.toJSON()
        except Exception as e:
            return AppResult.create_error_result(str(e)).toJSON()