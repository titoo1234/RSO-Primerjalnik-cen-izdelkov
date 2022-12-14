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
import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter
import config

logger = logging.getLogger("logstash")
logger.setLevel(logging.INFO)

handler = AsynchronousLogstashHandler(
    host=config.logurl, 
    port=23757,  
    ssl_verify=False,
    database_path='')

formatter = LogstashFormatter()
handler.setFormatter(formatter)

logger.addHandler(handler)

requests_total = Counter('flask_http_requests_total', 'VSI KLICI NA /user/<id>', ['method', 'endpoint'])
requests_summary = Summary('flask_http_requests_per_second', 'ŠTO NEVEM VEČ KA POMENI', ['method', 'endpoint'])

class Kosarica(Resource):
    def get(self,ime):
        try:
            query = f"SELECT izdelek,kolicina,cena FROM kosarica INNER JOIN uporabniki ON kosarica.uporabnik = uporabniki.id WHERE uporabniki.ime = '{ime}'"
            #query = f"SELECT * FROM kosarica where id = '{id}';"#SELECT * FROM Uporabniki Where {id} = Id
            conn = start_connDB()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            conn.close()
            return result, 200
        except Exception as e:
            "Error: " + str(e), 500

    def post(self,ime):#async
        try:
            #print("tuki smo")
            
            podatki = request.json
            izdelek = podatki['izdelek']
            # trgovina = podatki['trgovina']
            # cena = podatki['cena']
            kolicina = podatki['kolicina']
            query0 = f"SELECT cena FROM izdelki WHERE ime = '{izdelek}'"
            conn = start_connDB()
            df = pd.read_sql_query(query0, conn)
            tab_cen = df.to_dict("records")
            cena1 = round(tab_cen[0]["cena"] * kolicina, 2)
            cena2 = round(tab_cen[1]["cena"] * kolicina, 2)
            cena3 = round(tab_cen[2]["cena"] * kolicina, 2)
            #print(tab_cen)
            df = pd.read_sql_query(f"SELECT id FROM uporabniki WHERE ime = '{ime}'", conn)
            id = df.to_dict("records")[0]["id"]
            logger.info(f'added izdelek {izdelek} for user {ime}')
            query1 = f"INSERT INTO kosarica values ({id},'{izdelek}','Mercator',{kolicina},{cena1});"#SELECT * FROM Uporabniki Where {id} = Id
            query2 = f"INSERT INTO kosarica values ({id},'{izdelek}','Spar',{kolicina},{cena2});"#SELECT * FROM Uporabniki Where {id} = Id
            query3 = f"INSERT INTO kosarica values ({id},'{izdelek}','Tuš',{kolicina},{cena3});"#SELECT * FROM Uporabniki Where {id} = Id
            # df = pd.read_sql_query(query, conn)
            # result = df.to_dict("records")

            #print(query1)
            cursor = conn.cursor()
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)
            cursor.close()
            conn.close()
            return [True], 200
        except Exception as e:
            "Error: " + str(e), 500

    def delete(self, ime):
        conn = start_connDB()
        df = pd.read_sql_query(f"SELECT id FROM uporabniki WHERE ime = '{ime}'", conn)
        id = df.to_dict("records")[0]["id"]
        cur = conn.cursor()
        cur.execute(f"DELETE FROM kosarica WHERE uporabnik={id}")
        logger.info(f'deleted kosarica for user {ime}')
        cur.close()
        conn.close()
        return [True], 200



    

        

