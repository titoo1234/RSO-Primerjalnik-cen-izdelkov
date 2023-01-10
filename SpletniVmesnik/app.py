"""Code for the flask app."""
import requests
from flask import Flask,render_template,request,redirect
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from bs4 import BeautifulSoup
broken = False

def poisci_url(niz):
    '''
    Poišče prvo sliko, ki jo najdemo v brskalniku
    '''
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(niz)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    vrni = str(images[1]).split('src="')[1].split(';')[0]
    return vrni
def create_app():
    app = Flask(__name__)
    #api = Api(app)
   # api.add_resource(Catalog, '/katalog')
    return app

app = create_app()
# metrics = PrometheusMetrics(app, group_by="endpoint", path="/user/metrics")

@app.route("/")
def naslovna():
    # api_url = "http://127.0.0.1:5003/katalog"
    # response = requests.get(api_url)
    # response.json()#response.json()
    return render_template('zacetna_stran.html',izdelki=['Mleko','Kruh','Spageti','Klobase'])#'osnova_spletnega_vmesnika.html'


@app.route('/izdelek/<izdelek>')
def izdelek(izdelek):
    api_url = f"http://127.0.0.1:5005/katalog/{izdelek}"
    
    # response = requests.get(api_url)
    # response.json()
    slika_url = poisci_url(izdelek)
    trgovine=['Tuš','Mercator','Spar']
    cene = [1.21,1.52,1.54]
    zip1 = zip(trgovine,cene)
    return render_template('izdelek.html', zip = zip1,slika = slika_url,izdelek = izdelek)#'osnova_spletnega_vmesnika.html'


@app.route('/button')
def dodaj_v_kosarico():
    # api_url = f"http://127.0.0.1:5005/katalog/{izdelek}"
    kolicina = int(request.args.get("kolicina"))
    ime = request.args.get("ime_izdelka")
    print(ime)
    #kolicina.
    #print(kolicina)

    # TODO dodaj izdelek v košarico...
    return redirect('/')#'osnova_spletnega_vmesnika.html'

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5004)