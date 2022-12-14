"""Code for the flask app."""

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
import connections
broken = False
from izdelek import Izdelek
# def create_app():
#     app = Flask(__name__)
#     api = Api(app, doc='/openapi')
#     api.add_resource(Uporabnik, '/user', '/user/<int:id>')#, '/user/<int:id>')
#     #api.add_resource(Uporabniki, '/users')
#     #api.add_resource(AddUser, '/add_user')
#     api.add_resource(AddUser, '/user/add')
#     return app

def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Izdelek, '/izdelek/<string:ime>')
    return app

app = create_app()
metrics = PrometheusMetrics(app, group_by="endpoint", path="/izdelek/metrics")

@app.route('/izdelek/health')
def health_user():
    global broken
    if not broken and connections.check_connDB():#dodaj da preveri povezavo na bazo
        return "Ok", 200
    else:
        return "Unhealthy", 500

@app.route("/izdelek/break")
def break_ms():
    global broken
    broken = True
    return "You broke the microservice primerjava cen"

@app.route("/izdelek/unbreak")
def unbreak_ms():
    global broken
    broken = False
    return "You revived the microservice primerjava cen"

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5005)