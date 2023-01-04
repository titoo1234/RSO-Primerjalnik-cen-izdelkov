"""Code for the flask app."""
# import sys
# sys.path.append("../")
from flask import Flask
from flask_restful import Api#, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

from prometheus_flask_exporter import PrometheusMetrics

#import logging

#resources
from uporabnik import Uporabnik
#from uporabniki import Uporabniki
from dodajUporabnika import AddUser


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Uporabnik, '/user', '/user/<int:id>')#, '/user/<int:id>')
    #api.add_resource(Uporabniki, '/users')
    #api.add_resource(AddUser, '/add_user')
    api.add_resource(AddUser, '/user/add')
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()
metrics = PrometheusMetrics(app, group_by="endpoint", path="/user/metrics")
@app.route('/user/health')
def health_uporabnik():
    # tule bi načeloma mogli preverjat neki --_o_--
    # na navodilih piše da moremo simulirat bolno storitev, to bi naredli mogoče tako,
    # da bi meli neko globalno spremenljivo, ki bi se pri nekem določenem klicu spremenila,
    # in botem bi tule prišlo do falsa
    # neki simetričnega bi naredili za readiness pa še na eni mikrostoritvi
    if 1 + 1 == 2:
        return "Ok", 200
    else:
        return "Unhealthy", 500

#db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5002)