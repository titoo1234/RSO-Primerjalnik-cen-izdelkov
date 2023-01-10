"""Code for the flask app."""
import requests
from flask import Flask,render_template,request,redirect,make_response
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from bs4 import BeautifulSoup
import hashlib
broken = False
secret = 'skrivnost'

def json_to_table(tabJson):
    kluci = list(tabJson[0].keys())
    vrni = [[] for i in range(len(kluci))]
    for sl in tabJson:
        i = 0
        for kl in kluci:
            vrni[i].append(sl[kl])
            i += 1
    return vrni
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

def password_md5(s):
    '''
    Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
    kodirana s to funkcijo.
    '''
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

def get_user():
    '''
    Pogleda, kdo je uporabnik
    '''
    
    uporabniskoIme = request.cookies.get('uporabniskoIme')
    print(uporabniskoIme)
    if uporabniskoIme is not None:
        # preverimo če obstaja
        
        r = 'veljaven uporabnik'#model.Uporabnik(uporabniskoIme).jeUporabnik(conn)
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return uporabniskoIme
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    else:
        return None


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
    return render_template('izdelek.html', zip = zip1,slika = slika_url,izdelek = izdelek,user=get_user())#'osnova_spletnega_vmesnika.html'


@app.route('/SV/button')
def dodaj_v_kosarico():
    # api_url = f"http://127.0.0.1:5005/kosarica/{izdelek}"
    kolicina = int(request.args.get("kolicina"))
    ime = request.args.get("ime_izdelka")
    print(ime)
    #kolicina.
    #print(kolicina)

    # TODO dodaj izdelek v košarico...
    return redirect('/SV/')#'osnova_spletnega_vmesnika.html'

@app.route('/SV/kosarica/<uporabnik>')
def kosarica(uporabnik):

    # TODO preveri ali je pravi uporabnik... 
    # api_url = f"http://127.0.0.1:5005/kosarica/{uporabnik}"
    
    # response = requests.get(api_url)
    # response.json()
    slika_url = poisci_url(izdelek)
    Izdelek = ['Mleko','Mleko','Mleko']
    Kolicina = [1,1,1]
    Cena = [1.12,1.13,2.14]
    zip1 = zip(Izdelek,Kolicina,Cena)
    uporabniskoIme = 1
    return render_template('kosarica.html', zip = zip1, uporabniskoIme = uporabniskoIme)#'osnova_spletnega_vmesnika.html'

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
    api_url = f"http://127.0.0.1:5002/user/login/{uporabniskoIme}/{geslo}"
    # response = requests.get(api_url)
    # response.json()

    poizvedba = True
    if poizvedba is None:
        # Uporabnisko ime in geslo se ne ujemata
        return render_template('login.html',napaka = 'Uporabnik ne obstaja.',uporabniskoIme=None)

    else:
        resp = make_response('/SV/')
       
        resp.set_cookie('uporabniskoIme', uporabniskoIme)
        print(Flask.session_cookie_name)
        print(request.cookies.get(uporabniskoIme))
        #response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
        
        return redirect('/SV/')

@app.route('/SV/logout')
def logout():
    '''
    Pobrisi piškotke
    '''
    resp = make_response()
    resp.delete_cookie('uporabniskoIme')
    redirect('/SV/')

@app.route('/SV/register')
def register():
    return render_template('register.html', uporabniskoIme=None, napaka=None)

@app.route('/SV/register',methods = ['Post'])
def register_post():
    '''Registrira novega uporabnika.'''
    uporabniskoIme = request.form['uporabniskoIme']
    geslo1 = request.form['geslo1']
    geslo2 = request.form['geslo2']
    if not geslo1 == geslo2:
        return render_template('register.html', uporabniskoIme=uporabniskoIme, napaka='Gesli se ne ujemata.')
    else:
        geslo = password_md5(geslo1)
        poizvedba = True #apiklic
        if poizvedba:
            resp = make_response('(/SV/')
            resp.set_cookie('uporabniskoIme', uporabniskoIme, path='/')
            return redirect('/SV/')
        else:
            return render_template('register.html', uporabniskoIme=uporabniskoIme, napaka='To uporabnisko ime ze obstaja.')

   





























if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5004)
