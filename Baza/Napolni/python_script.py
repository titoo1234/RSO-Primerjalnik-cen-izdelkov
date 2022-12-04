import pyodbc
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import sys
import time
from textwrap import dedent


def create_db(server, port, uid, pwd, db_name):
    '''
        Creates new database on localhost, port 1433
    '''
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};Server=" + str(server) +";port=" + str(port)+";Database=master;UID="+str(uid)+";PWD="+str(pwd)+";"
        #odbc_str = 'DRIVER={ODBC Driver 17 for SQL Server};' + self.conn_str
        #you have to download odbc driver 17 https://www.microsoft.com/en-us/download/details.aspx?id=56567
    full_conn_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(conn_str)
    engine = create_engine(full_conn_str)
    engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    engine.execute(text(f"CREATE DATABASE {db_name}"))
    engine.dispose()

def fill_db(server, port, uid, pwd, db_name, sql_script):
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};Server="+str(server)+";port="+str(port)+";Database="+str(db_name)+";UID="+ str(uid) +";PWD=" + str(pwd)+";"
    # conn_str = dedent('''
    #         Driver={driver};
    #         Server=localhost;
    #         Port={port};
    #         Database={db_name};
    #         Uid={username};
    #         Pwd={password};
    #     '''.format(driver="{ODBC Driver 17 for SQL Server}", server_name=server, db_name=db_name, username=uid, password=pwd, port=port))
    # driver = "{ODBC Driver 17 for SQL Server}"
    #     #server_name = "tcp:primerjava-cen.database.windows.net,1433"
    # server_name = "localhost"
    #     #db_name = "Primerjava_cen"
    # db_name = "base123"
    #     #username = "baza"
    # username = "SA"
    #     #password = "AdminAdmin1!"
    # password = "yourStrong(!)Password"
    # port = "1433"

    # conn_str = dedent('''
    #         Driver={driver};
    #         Server={server_name};
    #         Database={db_name};
    #         Uid={username};
    #         Pwd={password};
    #         Port={port};
    #     '''.format(driver=driver, server_name=server_name, db_name=db_name, username=username, password=password, port=port))
    full_conn_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(conn_str)
    engine = create_engine(full_conn_str)
    #engine = create_engine(conn_str)
    #engine = pyodbc.connect(conn_str)
    with open(sql_script) as file:
        query = text(file.read())
    engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    engine.execute(query)
    # engine.dispose()


if __name__=='__main__':
    time.sleep(15)
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    d = sys.argv[4]
    e = sys.argv[5]
    f = sys.argv[6]
    try:
        create_db(a, b, c, d, e)
        fill_db(a, b, c, d , e , f)
    except Exception as e:
        print(str(e))
    # create_db("localhost", 1433, "SA", "yourStrong(!)Password", "base22")
    # fill_db("localhost", 1433, "SA", "yourStrong(!)Password" ,"base22", "setup.sql")