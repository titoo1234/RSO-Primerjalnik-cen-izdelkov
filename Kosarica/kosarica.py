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

class Kosarica(Resource):
    def get(self,id):
        try:
            query = f"SELECT * FROM kosarica where id = '{id}';"#SELECT * FROM Uporabniki Where {id} = Id
            conn = start_connDB()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            conn.close()
            return result, 200
        except Exception as e:
            "Error: " + str(e), 500

    def post(self,id,izdelek,trgovina,kolicina,cena):
        try:
            query = f"INSERT INTO kosarica values({id},{izdelek},{trgovina},{kolicina},{cena});"#SELECT * FROM Uporabniki Where {id} = Id
            conn = start_connDB()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            conn.close()
            return result, 200
        except Exception as e:
            "Error: " + str(e), 500



    

        

