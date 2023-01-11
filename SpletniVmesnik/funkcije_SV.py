from bs4 import BeautifulSoup
import requests
import hashlib
from flask import request
import requests

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
    return uporabniskoIme # OSTALO DELA AMPAK JE VRJETNO NEPOTREBNO
    # if uporabniskoIme is not None:
    #     api_url = f"http://127.0.0.1:5002/user/check/{uporabniskoIme}" # TO DELA
    #     response = requests.get(api_url)
    #     #r = 'veljaven uporabnik'#model.Uporabnik(uporabniskoIme).jeUporabnik(conn)
    #     response = response.json()
    #     if response[0]:
    #         # uporabnik obstaja, vrnemo njegove podatke
    #         return uporabniskoIme
    # # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    # else:
    #     return None
    ############################################################################## NEBRISAT
# ZUNANJI APIJI
def prevod(niz):
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": niz,
        "source": "en",
        "target": "sl"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "f152cd08b5msh52e4d2bcda3cbfap11d05ejsncaaad4e8d2df",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response = response.json()
    return response['data']['translations']['translatedText']

def lokacija():
    url = "https://ip-address-tracker-free.p.rapidapi.com/rapidapi/ip"
    headers = {
        "X-RapidAPI-Key": "f152cd08b5msh52e4d2bcda3cbfap11d05ejsncaaad4e8d2df",
        "X-RapidAPI-Host": "ip-address-tracker-free.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    return response['city']

def vreme_podatki():
    mesto = lokacija()
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":mesto}
    headers = {
        "X-RapidAPI-Key": "f152cd08b5msh52e4d2bcda3cbfap11d05ejsncaaad4e8d2df",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    #response['current']['condition']
    return response['current']['temp_c'],prevod(response['current']['condition']['text']),response['current']['condition']['icon']
