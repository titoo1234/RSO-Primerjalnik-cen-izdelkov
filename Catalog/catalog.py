from flask import request
from flask_restful import Resource
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from Models import AppResult

class Catalog(Resource):
    def get(self):
        #data = self.calculation_service.do_work()
        #if not isinstance(data, pd.DataFrame): raise ScriptException("Script result is not Dataframe")
        #self.sql_repo_commit.start_conn()
        #self.sql_repo_commit.commit(data, self.table_name)
        #self.sql_repo_commit.close_conn()
        return AppResult.create_true_result()


    def start_conn(self):
        #odbc_str = 'DRIVER={ODBC Driver 17 for SQL Server};' + self.conn_str
        #you have to download odbc driver 17 https://www.microsoft.com/en-us/download/details.aspx?id=56567
        full_conn_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(self.conn_str)
        s = ""
        try:
            self.engine = create_engine(full_conn_str)
        except Exception as e:
            pass