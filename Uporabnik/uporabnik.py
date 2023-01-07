# import sys
# sys.path.append('../')
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
import urllib.parse as up
import psycopg2
import pandas as pd
#from threading import Lock
#lock = Lock()

from prometheus_client import Counter, Summary, Gauge
requests_total = Counter('flask_http_requests_total', 'VSI KLICI NA /user/<id>', ['method', 'endpoint'])
requests_summary = Summary('flask_http_requests_per_second', 'ŠTO NEVEM VEČ KA POMENI', ['method', 'endpoint'])
#requests_gauge = Gauge('flask_http_request_latency_mean_seconds', 'POVPREČJE', ['method', 'endpoint'])

class Uporabnik(Resource):
    def get(self, id=None):
        requests_total.labels(method='GET', endpoint='/uporabnik').inc()
        with requests_summary.labels(method="GET", endpoint="/uporabnik").time():
        
            if id is None:
                try:
                    query = f"SELECT Id,Ime FROM Uporabniki;"
                    up.uses_netloc.append("postgres")
                    url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
                    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
                    conn.set_session(autocommit=True)
                    # cur = conn.cursor()
                    df = pd.read_sql_query(query, conn)
                    result = df.to_dict("records")
                    conn.close()
                    result = AppResult(True, "", result)

                    # with lock:
                    #     requests_summary._lock
                    #     count = requests_summary.labels(method='GET', endpoint='/uporabnik')._count
                    #     summ = requests_summary.labels(method='GET', endpoint='/uporabnik')._sum
                        
                    #     if count > 0:
                    #         requests_gauge.labels(method="GET", endpoint="/uporabnik").set(summ / count)
                    #         requests_summary._lock.release


                    return result.toJSON()
                except Exception as e:
                    return AppResult.create_error_result(str(e)).toJSON()

            else:
                try:
                    query = f"SELECT * FROM Uporabniki Where {id} = Id;"
                    up.uses_netloc.append("postgres")
                    url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
                    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
                    conn.set_session(autocommit=True)
                    # cur = conn.cursor()
                    df = pd.read_sql_query(query, conn)
                    result = df.to_dict("records")
                    conn.close()
                    result = AppResult(True, "", result)
                    return result.toJSON()
                except Exception as e:
                    return AppResult.create_error_result(str(e)).toJSON()

    def delete(self, id):
        try:
            #name = request.json["username"]
            #password = request.json["password"]
            #query = f"SELECT Id,Ime FROM Uporabniki;"
            #query = "INSERT INTO Uporabniki (ime, geslo, admin) VALUES ('test3', '1234567', 0);"
            up.uses_netloc.append("postgres")
            url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            cur.execute('DELETE FROM Uporabniki WHERE "id" = %s;', (id,))
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
