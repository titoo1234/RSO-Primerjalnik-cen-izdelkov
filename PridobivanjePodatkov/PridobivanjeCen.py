from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

izdelki = ["milo", "mleko", "kruh", "jabolka", "maslo"]

def slovar_v_sql(slovar, ime_tabele, datoteka):
    """
    Funkcija na podlagi slovarja slovarjev {"izdelek": [{"trgovina1": cena1, "trgovina2": cena2, ...}, slika], ...}
    zgenerira skripto s sql stavki: 
    INSERT INTO TABELA VALUES (izdelek, trgovina1_cena, trgovina2_cena, trgovina3_cena, ...)
    """
    with open(datoteka, 'w') as dat:
        for izdelek in slovar.keys():
            mercator_cena = slovar[izdelek][0]["MERCATOR"]
            spar_cena = slovar[izdelek][0]["SPAR"]
            tus_cena = slovar[izdelek][0]["TUS"]
            slika_src = slovar[izdelek][1]
            insert_niz = f"INSERT INTO {ime_tabele} VALUES (\'{izdelek}\', {mercator_cena}, {spar_cena}, {tus_cena}, \'{slika_src}\')"
            try:
                dat.write(insert_niz)
                dat.write("\n")
            except:
                raise Exception("Napaka pri zapisovanju na datoteko.")


def datoteka_v_tabelo(datoteka):
    """
    Funkcija iz datoteke prebere izdelke in jih vrne v obliki tabele
    """
    izdelki = []
    with open(datoteka, "r") as dat:
        vrsta = dat.readline().strip()
        while vrsta != "":
            izdelki.append(vrsta)
            vrsta = dat.readline().strip()
    return izdelki

def pridobivanje_cen_izdelkov(izdelki):
    """
    Funkcija iz seznama željenih izdelkov zgenerira
    slovar slovarjev, kjer so ključi podani izdelki, vrednosti pa zopet tabele [slovar, slika]
    kjer so ključi slovarja trgovine (mercator, spar, tus) vrednosti pa cena izdelka v posamezni 
    spletni trgovini. Če izdelka ne najdemo, ga izpustimo.
    """
    options = Options()
    options.add_argument("--headless")
    slovar_izdelkov = {}
    brskalnik = webdriver.Chrome(options=options)
    for izdelek in izdelki:
        # url-ji za posamezne spletne trgovine
        mercator_url = f"https://trgovina.mercator.si/market/brskaj#search={izdelek}"
        spar_url = f"https://www.spar.si/online/search/?q={izdelek}&query={izdelek}&hitsPerPage=72&substringFilter=pos-visible:81701&q1=&x1=product-lifestyleInf"
        tus_url = f"https://www.tus.si/?swoof=1&post_type=product&woof_text={izdelek}"
        # slovar {"trgovina": cena}
        slovar_cen = {}
        slika_src = ""
        try:
            # MERCATOR:
            wait = WebDriverWait(brskalnik, 5)
            brskalnik.get(mercator_url)
            # pobrisemo pojavna okenca (cookie, adds), da pridemo do dejanske spletne strani
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div/a[2]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div[1]/a'))).click()
            izdelek_mercator_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="grid"]/div[1]/div[1]/div[4]/div[2]/strong')))
            try:  
                slika = brskalnik.find_element(By.XPATH, '//*[@id="grid"]/div[1]/div[1]/a[2]/img')
                slika_src = slika.get_attribute("src")
            except:
                try:
                    slika = brskalnik.find_element(By.XPATH, '//*[@id="grid"]/div[1]/div[1]/a/img')
                    slika_src = slika.get_attribute("src")
                except:
                    pass
            izdelek_mercator = izdelek_mercator_tab[0].text
            cena_mercator = float(izdelek_mercator.replace(",", "."))
            slovar_cen["MERCATOR"] = cena_mercator
            print(cena_mercator)
        except:
            print("NAPAKA: mercator")
            continue
        try:
            # ŠPAR:
            brskalnik = webdriver.Chrome(options=options)
            wait = WebDriverWait(brskalnik, 5)
            brskalnik.get(spar_url)
            try:
                izdelek_spar_cela_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div/div[1]/div[5]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div[1]')))
                izdelek_spar_dec_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div/div[1]/div[5]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[1]')))
            except: # Če ima izdelek akcijo, je potrebno zamenjati xpath
                izdelek_spar_cela_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div/div[1]/div[5]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[1]')))
                izdelek_spar_dec_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div/div[1]/div[5]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[1]')))
            izdelek_spar = izdelek_spar_cela_tab[0].text + "." + izdelek_spar_dec_tab[0].text
            cena_spar = float(izdelek_spar)
            slovar_cen["SPAR"] = cena_spar
            print(cena_spar)
        except:
            print("NAPAKA: spar")
            continue
        try:
            # TUŠ:
            brskalnik = webdriver.Chrome(options=options)
            wait = WebDriverWait(brskalnik, 5)
            brskalnik.get(tus_url)
            izdelek_tus_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/section[1]/div/div/div/div/div[2]/ul/li[1]/div/span[1]')))
            izdelek_tus = izdelek_tus_tab[0].text
            cena_tus = float(izdelek_tus.replace(",", ".")[:-2])
            slovar_cen["TUS"] = cena_tus
            print(cena_tus)
        except:
            print("NAPAKA: tus")
            continue
        slovar_izdelkov[izdelek] = [slovar_cen, slika_src]
    return slovar_izdelkov

tab = datoteka_v_tabelo("/Users/damijanrandl/Downloads/izdelki.txt")
slovar = pridobivanje_cen_izdelkov(tab)
slovar_v_sql(slovar, "cene", "/Users/damijanrandl/Downloads/insert_stavki.txt")
