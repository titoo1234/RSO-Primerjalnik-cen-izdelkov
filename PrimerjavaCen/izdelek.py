from flask import request, jsonify
from flask_restx import Resource
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
from connections import start_connDB
from prometheus_client import Counter, Summary, Gauge
requests_total = Counter('flask_http_requests_total', 'VSI KLICI NA /user/<id>', ['method', 'endpoint'])
requests_summary = Summary('flask_http_requests_per_second', 'ŠTO NEVEM VEČ KA POMENI', ['method', 'endpoint'])

class Izdelek(Resource):
    def get(self,ime):
        try:
            query = f"SELECT * FROM izdelki where ime = '{ime}';"#SELECT * FROM Uporabniki Where {id} = Id
            conn = start_connDB()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            print(result)
            conn.close()
            return result, 200
        except Exception as e:
            "Error: " + str(e), 500



    def delete(self, id):
        try:
            query = f"DELETE FROM Uporabniki WHERE id = {id};"#SELECT * FROM Uporabniki Where {id} = Id
            conn = start_connDB()
            cur = conn.cursor()
            cur.execute(query)
            cur.close()
            conn.close()
            conn.close()
            return "User deleted", 200
        except Exception as e:
            return "Error: " + str(e), 500

    

        

