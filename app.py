"""Code for the flask app."""
# import sys
# sys.path.append("../")
from flask import Flask
from flask_restful import Api#, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy


#import logging
from Services.test import Test

#resources
from Services.uporabnik import Uporabnik
from Services.kosarica import Kosarica
from Services.trgovine import Trgovine



def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Uporabnik, '/users', '/users/<int:id>')
    api.add_resource(Kosarica, '/kosarica')
    api.add_resource(Trgovine, '/trgovine')

    api.add_resource(Test, '/test')
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()

@app.route('/trgovine/health')
def health_trgovine():
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