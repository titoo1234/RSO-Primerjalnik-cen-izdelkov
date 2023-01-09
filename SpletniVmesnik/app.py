"""Code for the flask app."""
import requests
from flask import Flask,render_template
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
broken = False



def create_app():
    app = Flask(__name__)
    #api = Api(app)
   # api.add_resource(Catalog, '/katalog')
    return app

app = create_app()
# metrics = PrometheusMetrics(app, group_by="endpoint", path="/user/metrics")

@app.route("/a")
def naslovna():
    # api_url = "http://127.0.0.1:5003/katalog"
    # response = requests.get(api_url)
    # response.json()#response.json()
    return render_template('zacetna_stran.html')#'osnova_spletnega_vmesnika.html'


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5004)