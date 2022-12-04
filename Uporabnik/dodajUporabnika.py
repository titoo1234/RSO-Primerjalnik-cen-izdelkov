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
import hashlib
import pandas as pd
import psycopg2
import urllib.parse as up
    
    
class AddUser(Resource):
    def post(self):
        return
        #try:
            # query = "SELECT Id,Ime FROM Uporabniki;"
            # up.uses_netloc.append("postgres")
            # url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            # conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            # conn.set_session(autocommit=True)
            
            # #df = pd.read_sql_query(query, conn)
            # #result = df.to_dict("records")
            # cursor = conn.cursor()
            # cursor.execute("INSERT INTO Uporabniki VALUES (?, ?, ?)", [req["username"], req["password"], 0])
            
            # execute_query()
            # cur.execute(query)
            # result = cur.fetchall()


            # eng = SQLRepository(conn_str)
            # eng.start_conn()
            # print("conn started success")
            
            # result = eng.execute_query(query)
            # print("execute query succ")
            # eng.close_conn()
        #     result = AppResult(True, "", result)
        #     return result.toJSON()
        # except Exception as e:
        #     return AppResult.create_error_result(str(e)).toJSON()
        # driver = "{ODBC Driver 17 for SQL Server}"

        # server_name = "primerjava-cen.database.windows.net,1433"
        # db_name = "Primerjava_cen"

        # username = "baza"
        # password = "AdminAdmin1!"

        # conn_str = dedent('''
        #     Driver={driver};
        #     Server={server_name};
        #     Database={db_name};
        #     Uid={username};
        #     Pwd={password};
        #     Encrypt=yes;
        #     TrustServerCertificate=no;
        #     Connection Timeout=30;
        # '''.format(driver=driver, server_name=server_name, db_name=db_name, username=username, password=password))
        # podatki = request.json
        # if "username" not in podatki: raise DataException("username not in body")
        # if "password" not in podatki: raise DataException("password not in body")
        # #podatki["password"] = hash(podatki["password"])############################UPORABI DRUGAČNO FUNKCIJO
        # podatki["password"] = hashlib.md5(podatki["password"].encode()).hexdigest()
        # ime = podatki["username"]
        # #conn_str = "C:/Users/Lenovo/Desktop/1faks/isrm1/racunalniske_storitve_v_oblaku/RSO-Primerjalnik-cen-izdelkov/prva_baza.db"
        # eng = SQLRepository(conn_str)
        # eng.start_conn()
        # try:
        #     result = eng.add_row(podatki)
        # except Exception as e:
        #     print(str(e))
        #     return AppResult.create_error_result("neki negre, vrjetno že obstaja s takim imenom").toJSON()
        # eng.close_conn()
        # if result:
        #     return AppResult(True, f"added user {ime}", None).toJSON()
        # return AppResult.create_error_result("negre").toJSON()