"""Code for the flask app."""
# import sys
# sys.path.append("../")
from flask import Flask
from flask_restful import Api#, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy


#import logging

#resources
from uporabnik import Uporabnik
from uporabniki import Uporabniki
from dodajUporabnika import AddUser


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Uporabnik, '/user/<int:id>')#, '/user/<int:id>')
    api.add_resource(Uporabniki, '/users')
    api.add_resource(AddUser, '/add_user')
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()
#db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5002)