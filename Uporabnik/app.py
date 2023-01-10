"""Code for the flask app."""
# import sys
# sys.path.append("../")
from flask import Flask, request
#from flask_restful import Api#, Resource, reqparse
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import flask

from prometheus_flask_exporter import PrometheusMetrics
import connections
import hashlib
import config
from funkcije_uporabnik import *


#import logging

#resources
from uporabnik import Uporabnik
#from uporabniki import Uporabniki
from dodajUporabnika import AddUser

broken = False

def create_app():
    app = Flask(__name__)
    api = Api(app, doc='/openapi')
    api.add_resource(Uporabnik, '/user', '/user/<int:id>')#, '/user/<int:id>')
    #api.add_resource(Uporabniki, '/users')
    #api.add_resource(AddUser, '/add_user')
    api.add_resource(AddUser, '/user/add')
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()
metrics = PrometheusMetrics(app, group_by="endpoint", path="/user/metrics")


@app.route('/user/health')
#@app.header("ABC", "WTF")
def health_user():
    # tule bi načeloma mogli preverjat neki --_o_--
    # na navodilih piše da moremo simulirat bolno storitev, to bi naredli mogoče tako,
    # da bi meli neko globalno spremenljivo, ki bi se pri nekem določenem klicu spremenila,
    # in botem bi tule prišlo do falsa
    # neki simetričnega bi naredili za readiness pa še na eni mikrostoritvi
    #if not broken and dela_pozevaz
    global broken
    if not broken and connections.check_connDB():#dodaj da preveri povezavo na bazo
        return "Ok", 200
    else:
        return "Unhealthy", 500

@app.route("/user/break")
def break_ms():
    global broken
    broken = True
    return "You broke the microservice user"

@app.route("/user/unbreak")
def unbreak_ms():
    global broken
    broken = False
    return "You revived the microservice user"

@app.route("/user/login", methods=["GET"])
def check_login():
    ime = request.json["username"]
    geslo = request.json["password"]
    return [preveri_ime_geslo(ime, geslo)]

@app.route("/user/check/<string:ime>", methods=["GET"])
def check_user(ime):
    return [obstaja_uporabnik(ime)]



if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5002)