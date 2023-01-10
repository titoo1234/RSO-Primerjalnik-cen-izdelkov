"""Code for the flask app."""
import requests
from flask import Flask,render_template,request,redirect,make_response
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from bs4 import BeautifulSoup
import hashlib
from funkcije_SV import *
broken = False
secret = 'skrivnost'


def create_app():
    app = Flask(__name__)
    #api = Api(app)
   # api.add_resource(Catalog, '/katalog')
    return app

app = create_app()
# metrics = PrometheusMetrics(app, group_by="endpoint", path="/user/metrics")

@app.route("/SV/")
def naslovna():
    # api_url = "http://127.0.0.1:5003/katalog" # TO DELA
    # response = requests.get(api_url)
    # vsi_izdelki = json_to_table(response.json())
    # vsi_izdelki = list(set(vsi_izdelki[0]))

    vsi_izdelki = ['Mleko','Kruh','Špageti']

    return render_template('zacetna_stran.html',izdelki=vsi_izdelki, uporabniskoIme=get_user())#'osnova_spletnega_vmesnika.html'


@app.route('/SV/izdelek/<izdelek>')
def izdelek(izdelek):
    # api_url = f"http://127.0.0.1:5005/izdelek/{izdelek}" #DELA
    # response = requests.get(api_url)
    # vsi_izdelki = json_to_table(response.json())
    # trgovine = list(set(vsi_izdelki[1]))
    # cene = list(set(vsi_izdelki[2]))

    slika_url = poisci_url(izdelek)
    trgovine=['Tuš','Mercator','Spar']
    cene = [1.21,1.52,1.54]
    zip1 = zip(trgovine,cene)
    return render_template('izdelek.html', zip = zip1,slika = slika_url,izdelek = izdelek,uporabniskoIme=get_user())#'osnova_spletnega_vmesnika.html'


@app.route('/SV/button')
def dodaj_v_kosarico():
    print('asdasd')
    api_url = f"http://127.0.0.1:5006/kosarica/1"
    kolicina = int(request.args.get("kolicina"))
    ime = request.args.get("ime_izdelka")
    data = {'kolicina':kolicina,'izdelek':'Mleko','trgovina':'Tuš','cena':7.45}
    response = requests.post(api_url,json=data)
    print(response.json)
    print(ime)
    #kolicina.
    #print(kolicina)

    # TODO dodaj izdelek v košarico...
    return redirect('/SV/')#'osnova_spletnega_vmesnika.html'

@app.route('/SV/kosarica/<uporabnik>')
def kosarica(uporabnik):

    # TODO preveri ali je pravi uporabnik... 
    api_url = f"http://127.0.0.1:5006/kosarica/{uporabnik}"
    
    response = requests.get(api_url)
    response = response.json()
    slika_url = poisci_url(izdelek)
    vse_tabele = json_to_table(response)
    Izdelki = vse_tabele[0]
    Kolicine = vse_tabele[1]
    Cene = vse_tabele[2]
    #Izdelek = ['Mleko','Mleko','Mleko']
    #Kolicina = [1,1,1]
    #Cena = [1.12,1.13,2.14]
    rez = []
    for i in range(0, len(Izdelki), 3):
        rez.append((Izdelki[i], Kolicine[i], Cene[i], Cene[i + 1],Cene[i + 2]))

    #zip1 = zip(Izdelek,Kolicina,Cena)
    uporabniskoIme = get_user()
    return render_template('kosarica.html', zip = rez, uporabniskoIme = uporabniskoIme)#'osnova_spletnega_vmesnika.html'

@app.route('/SV/buttonZbrisiKosarico')
def zbrisiKosarico():
    # api_url = f"http://127.0.0.1:5005/katalog/{izdelek}"


    # TODO rabimo podatek o ID uporabnika; zbrišemo stvari iz kosarice
    return redirect('/')#'osnova_spletnega_vmesnika.html'


@app.route('/SV/login')
def login():
    return render_template('login.html',napaka = None,uporabniskoIme=None)


@app.route('/SV/login',methods = ['Post'])
def login_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    uporabniskoIme = request.form['uporabniskoIme']
    geslo = password_md5(request.form['geslo']) #zakodiramo

    api_url = f"http://127.0.0.1:5002/user/login"
    data = {'username': uporabniskoIme, 'password':geslo}
    response = requests.get(api_url,json=data)
    #response = response.json
    response = response.json()
    # response = [True]
    if not response[0]:
        # Uporabnisko ime in geslo se ne ujemata
        return render_template('login.html',napaka = 'Uporabnik ne obstaja.',uporabniskoIme=None)

    else:
        resp = make_response(redirect('/SV/'))
        resp.set_cookie('uporabniskoIme', uporabniskoIme)
        #print(Flask.session_cookie_name)
        #print(request.cookies.get('uporabniskoIme'))
        #response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
        
        #return redirect('/SV/')
        return resp

@app.route('/SV/logout')
def logout():
    '''
    Pobrisi piškotke
    '''
    resp = make_response(redirect("/SV/"))
    resp.delete_cookie('uporabniskoIme')
    return resp

@app.route('/SV/register')
def register():
    return render_template('register.html', uporabniskoIme=None, napaka=None)

@app.route('/SV/register',methods = ['Post'])
def register_post():
    '''Registrira novega uporabnika.'''
    uporabniskoIme = request.form['uporabniskoIme']
    print("ASSDSADDSDASDFSF")
    geslo1 = request.form['geslo1']
    geslo2 = request.form['geslo2']
    if not geslo1 == geslo2:
        return render_template('register.html', uporabniskoIme=uporabniskoIme, napaka='Gesli se ne ujemata.')
    else:
        
        geslo = password_md5(geslo1)
        api_url = f"http://127.0.0.1:5002/user/add"
        data = {'username': uporabniskoIme, 'password':geslo}
        response = requests.post(api_url,json=data)
        response = response.json()
        print(response)
        #response = [True] #apiklic
        if response[0]:
            resp = make_response(redirect('/SV/'))
            resp.set_cookie('uporabniskoIme', uporabniskoIme)
            return resp
        else:
            return render_template('register.html', uporabniskoIme=uporabniskoIme, napaka='To uporabnisko ime ze obstaja.')

   





























if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
