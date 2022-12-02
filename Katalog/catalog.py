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


class Catalog(Resource):
    def get(self):
        
        driver = "{ODBC Driver 17 for SQL Server}"
        server_name = "tcp:primerjava-cen.database.windows.net,1433"
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
        '''.format(driver=driver, server_name=server_name, db_name=db_name, username=username, password=password))
        #Connection Timeout=30;
        #conn_str = r"sqlite:///DRIVER={ODBC Driver 17 for SQL Server}C:/Users/Lenovo/Desktop/1faks/isrm1/racunalniske_storitve_v_oblaku/RSO-Primerjalnik-cen-izdelkov/testna_baza.db"
        #'mssql+pyodbc:///?odbc_connect=' + quote_plus("DRIVER={ODBC Driver 17 for SQL Server};Server=db;port=1433;DataBase=base1;UID=SA;PWD=yourStrong(!)Password;")
        #conn_str = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=tcp:primerjava-cen.database.windows.net,1433;Database=Primerjava_cen;Uid=baza;Pwd=AdminAdmin1!;Encrypt=yes;TrustServerCertificate=no;"
        #conn_str = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=tcp:primerjava-cen.database.windows.net,1433;Database=Primerjava_cen;Uid=baza;Pwd=AdminAdmin1!;"
        #conn_str = "mssql+pyodbc:///?odbc_connect=" + quote_plus(conn_str)
        #query = "SELECT * from Trgovina"
        query = "SELECT * FROM Trgovina"
        try:
            eng = SQLRepository(conn_str)
            eng.start_conn()
            result = eng.execute_query(query)
            eng.close_conn()
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

