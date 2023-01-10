'''test'''
print(1)
import requests
from bs4 import BeautifulSoup
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


a = [{'ime': 'Mleko', 'trgovina': 'Hofer', 'cena': 1.22}, {'ime': 'Mleko', 'trgovina': 'Mercator', 'cena': 1.37}, {'ime': 'Mleko', 'trgovina': 'Tuš', 'cena': 1.42}]
b = a[0]['cena']
print(b)

def json_to_table(tabJson):
    kluci = list(tabJson[0].keys())
    vrni = [[] for i in range(len(kluci))]
    for sl in tabJson:
        i = 0
        for kl in kluci:
            vrni[i].append(sl[kl])
            i += 1
    return vrni
t = {'ime': 'Mleko', 'trgovina': 'Hofer', 'cena': 1.22}

print(json_to_table(a))
