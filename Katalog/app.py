"""Code for the flask app."""
# import sys
# sys.path.append("../")
from flask import Flask
from flask_restful import Api#, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

#import logging

#resources
from catalog import Catalog
from test import Test


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Catalog, '/trgovine')
    api.add_resource(Test, "/test")
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=tcp:primerjava-cen.database.windows.net,1433;Database=Primerjava_cen;Uid=baza;Pwd=AdminAdmin1!;Encrypt=yes;TrustServerCertificate=no;"
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()
#db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)