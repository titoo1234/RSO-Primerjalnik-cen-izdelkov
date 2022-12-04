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


class Catalog(Resource):
    def get(self):
        
        # driver = "{ODBC Driver 17 for SQL Server}"
        # #server_name = "tcp:primerjava-cen.database.windows.net,1433"
        # server_name = "Database"
        # #če maš samo bazo na dockerju dap localhost
        # #db_name = "Primerjava_cen"
        # db_name = "base123"
        # #username = "baza"
        # username = "SA"
        # #password = "AdminAdmin1!"
        # password = "yourStrong(!)Password"
        # port = "1433"

        # conn_str = dedent('''
        #     Driver={driver};
        #     Server={server_name};
        #     Database={db_name};
        #     Uid={username};
        #     Pwd={password};
        #     Port={port};
        # '''.format(driver=driver, server_name=server_name, db_name=db_name, username=username, password=password, port=port))
        #            Encrypt=yes;
        #    TrustServerCertificate=no;
        #Connection Timeout=30;
        #conn_str = r"sqlite:///DRIVER={ODBC Driver 17 for SQL Server}C:/Users/Lenovo/Desktop/1faks/isrm1/racunalniske_storitve_v_oblaku/RSO-Primerjalnik-cen-izdelkov/testna_baza.db"
        #'mssql+pyodbc:///?odbc_connect=' + quote_plus("DRIVER={ODBC Driver 17 for SQL Server};Server=db;port=1433;DataBase=base1;UID=SA;PWD=yourStrong(!)Password;")
        #conn_str = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=tcp:primerjava-cen.database.windows.net,1433;Database=Primerjava_cen;Uid=baza;Pwd=AdminAdmin1!;Encrypt=yes;TrustServerCertificate=no;"
        #conn_str = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=tcp:primerjava-cen.database.windows.net,1433;Database=Primerjava_cen;Uid=baza;Pwd=AdminAdmin1!;"
        #conn_str = "mssql+pyodbc:///?odbc_connect=" + quote_plus(conn_str)
        #query = "SELECT * from Trgovina"
        
        
        # server ="Database"
        # port = "1433"
        # uid= "SA"
        # pwd= "yourStrong(!)Password"
        # db_name = "base123"
        # conn_str = "DRIVER={ODBC Driver 17 for SQL Server};Server="+str(server)+";port="+str(port)+";Database="+str(db_name)+";UID="+ str(uid) +";PWD=" + str(pwd)+";"
        # query = "SELECT * FROM Trgovine"

        

        try:
            up.uses_netloc.append("postgres")
            url = up.urlparse("postgres://fzhvzwic:hjYYIyExOk4_UXtKv9BoWkqeso0gVhlB@peanut.db.elephantsql.com/fzhvzwic")
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
            conn.set_session(autocommit=True)
            cur = conn.cursor()

            cur.execute('Select * from Trgovine')

            # eng = SQLRepository(conn_str)
            # eng.start_conn()
            # print("conn started success")
            result = cur.fetchall()
            # result = eng.execute_query(query)
            # print("execute query succ")
            # eng.close_conn()
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
        #id = request.json["id"]
        #trgovina = request.json["trgovina"]
        #query = "INSERT INTO Trgovina VALUES (?, ?);"
        eng = SQLRepository(conn_str)
        eng.start_conn()
        result = eng.add_row(request.json)
        eng.close_conn()
        if result:
            return AppResult(True, "", None).toJSON()
        return AppResult.create_error_result("negre").toJSON()

