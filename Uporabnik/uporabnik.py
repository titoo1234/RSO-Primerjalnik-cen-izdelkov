# import sys
# sys.path.append('../')
from flask import request, jsonify
#from flask_restful import Resource
from flask_restx import Resource
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from textwrap import dedent
import pyodbc
from flask_sqlalchemy import SQLAlchemy
import urllib.parse as up
import psycopg2
import pandas as pd
import connections
#from threading import Lock
#lock = Lock()

from prometheus_client import Counter, Summary, Gauge
requests_total = Counter('flask_http_requests_total', 'VSI KLICI NA /user/<id>', ['method', 'endpoint'])
requests_summary = Summary('flask_http_requests_per_second', 'VSI KLICI NA SEKUNDO NA /user/<id>', ['method', 'endpoint'])
#requests_gauge = Gauge('flask_http_request_latency_mean_seconds', 'POVPREČJE', ['method', 'endpoint'])

class Uporabnik(Resource):
    def get(self, id=None):

        requests_total.labels(method='GET', endpoint='/user').inc()
        with requests_summary.labels(method="GET", endpoint="/user").time():
        
            if id is None:
                try:
                    query = f"SELECT Id,Ime FROM Uporabniki;"
                    conn = connections.start_connDB()
                    df = pd.read_sql_query(query, conn)
                    result = df.to_dict("records")
                    conn.close()
                    return result, 200
                except Exception as e:
                    "Error: " + str(e), 500 #mogoče redirect na /break????

            else:
                try:
                    query = f"SELECT * FROM Uporabniki Where {id} = Id;"
                    conn = connections.start_connDB()
                    # cur = conn.cursor()
                    df = pd.read_sql_query(query, conn)
                    result = df.to_dict("records")
                    conn.close()
                    return result, 200
                except Exception as e:
                    "Error: " + str(e), 500

    def delete(self, id):
        try:
            conn = connections.start_connDB()
            cur = conn.cursor()
            cur.execute('DELETE FROM Uporabniki WHERE "id" = %s;', (id,))
            cur.close()
            conn.close()
            #če ni prišlo do napake je vse ok
            # df = pd.read_sql_query(query, conn)
            # print(df)
            # result = df.to_dict("records")
            # print(result)
            #result = AppResult.create_true_result()
            #return result.toJSON(), 200
            return "User deleted", 200
        except Exception as e:
            return "Error: " + str(e), 500
