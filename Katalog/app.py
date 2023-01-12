"""Code for the flask app."""

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
import connections
broken = False
from catalog import Catalog


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Catalog, '/katalog')
    return app

app = create_app()
metrics = PrometheusMetrics(app, group_by="endpoint", path="/katalog/metrics")

@app.route('/katalog/health')
def health_user():
    global broken
    if not broken and connections.check_connDB():#dodaj da preveri povezavo na bazo
        return "Ok", 200
    else:
        return "Unhealthy", 500

@app.route("/katalog/break")
def break_ms():
    global broken
    broken = True
    return "You broke the microservice katalog"

@app.route("/katalog/unbreak")
def unbreak_ms():
    global broken
    broken = False
    return "You revived the microservice katalog"

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5003)