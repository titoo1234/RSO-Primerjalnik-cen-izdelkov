from logging import exception
import sqlite3 as dbapi
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pyodbc
from Models.Exceptions import DataException, QueryException, ConnectionException
from flask_sqlalchemy import SQLAlchemy
import sqlite3

class SQLRepository:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def start_conn(self):
        #odbc_str = 'DRIVER={ODBC Driver 17 for SQL Server};' + self.conn_str
        #you have to download odbc driver 17 https://www.microsoft.com/en-us/download/details.aspx?id=56567
        #full_conn_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(self.conn_str)
        try:
            #self.engine = pyodbc.connect(self.conn_str)
            #self.engine = create_engine(self.conn_str)
            self.engine = sqlite3.connect(self.conn_str)####################################################
        except Exception as e:
            raise ConnectionException(str(e))

    def close_conn(self):
        self.engine.close()
        #self.engine.dispose()

    def execute_query(self, query):
        df = pd.read_sql_query(query, self.engine)
        return df.to_dict("records")
        # try:
        #     df = pd.read_sql_query(query, self.engine)
        #     return df
        # except Exception as e:
        #     raise QueryException(str(e))

    def add_row(self, req): # data has to be dataframe
        #data = pd.DataFrame(data)
        cursor = self.engine.cursor()
        cursor.execute("INSERT INTO Uporabniki VALUES (?, ?, ?, ?)", [req["username"], req["password"], 0, None])
        self.engine.commit()
        #cursor.commit()
        #data.to_sql(str(table_name), self.engine, if_exists="replace", index=False)
        return True