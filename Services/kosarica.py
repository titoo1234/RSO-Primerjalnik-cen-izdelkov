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
import urllib.parse as up
import psycopg2
import pandas as pd

class Kosarica(Resource):
    def get(self):
        try:
            query = f"SELECT * FROM Kosarica;"
            up.uses_netloc.append("postgres")
            url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            conn.set_session(autocommit=True)
            # cur = conn.cursor()
            df = pd.read_sql_query(query, conn)
            result = df.to_dict("records")
            result = AppResult(True, "", result)
            return result.toJSON()
        except Exception as e:
            return AppResult.create_error_result(str(e)).toJSON()



    def post(self):
        driver = "{ODBC Driver 17 for SQL Server}"

        server_name = "primerjava-cen.database.windows.net,1433"
        db_name = "Primerjava_cen"

        username = "baza"
        password = "AdminAdmin1!"

        conn_str = dedent('''
            Driver={driver};
            Server={server_name};
            Database={db_name};
            Uid={username};
            Pwd={password};
            Encrypt=yes;
            TrustServerCertificate=no;
            Connection Timeout=30;
        '''.format(driver=driver, server_name=server_name, db_name=db_name, username=username, password=password))
        # conn_str = "C:/Users/Lenovo/Desktop/1faks/isrm1/racunalniske_storitve_v_oblaku/RSO-Primerjalnik-cen-izdelkov/prva_baza.db"
        eng = SQLRepository(conn_str)
        eng.start_conn()
        result = eng.add_row(request.json)
        eng.close_conn()
        if result:
            return AppResult(True, "", None).toJSON()
        return AppResult.create_error_result("negre").toJSON()

