from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from flask import request, jsonify
from flask_restx import Resource
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from textwrap import dedent
import pyodbc
from flask_sqlalchemy import SQLAlchemy
import urllib.parse as up
import psycopg2
import pandas as pd
from connections import start_connDB
from prometheus_client import Counter, Summary, Gauge
import os

class PridobivanjePodatkov(Resource):
    def get(self):
        try:
            conn = start_connDB()
            cur = conn.cursor()
            dat_izdelkov = "PridobivanjePodatkov/datoteke/izdelki.txt"
            tab_izdelkov = self.datoteka_v_tabelo(dat_izdelkov) 
            slovar_izdelkov = self.pridobivanje_cen_izdelkov(tab_izdelkov)
            datoteka = self.slovar_v_sql(slovar_izdelkov, "Izdelki", "PridobivanjePodatkov/datoteke/insert_stavki.txt")
            self.izprazni_bazo(cur, "Izdelki")
            self.napolni_bazo(cur, datoteka)
            cur.close()
            conn.close()
            return "Data inserted", 200
        except Exception as e:
            return "Error: " + str(e), 500

    def slovar_v_sql(self, slovar, ime_tabele, datoteka):
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
                insert_niz_1 = f"INSERT INTO {ime_tabele} VALUES (\'{izdelek}\', \'Mercator\', {mercator_cena});"
                insert_niz_2 = f"INSERT INTO {ime_tabele} VALUES (\'{izdelek}\', \'Špar\', {spar_cena});"
                insert_niz_3 = f"INSERT INTO {ime_tabele} VALUES (\'{izdelek}\', \'Tuš\', {tus_cena});"
                try:
                    dat.write(insert_niz_1)
                    dat.write("\n")
                    dat.write(insert_niz_2)
                    dat.write("\n")
                    dat.write(insert_niz_3)
                    dat.write("\n")
                except:
                    raise Exception("Napaka pri zapisovanju na datoteko.")
        return datoteka


    def datoteka_v_tabelo(self, datoteka):
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

    def pridobivanje_cen_izdelkov(self, izdelki):
        """
        Funkcija iz seznama željenih izdelkov zgenerira
        slovar slovarjev, kjer so ključi podani izdelki, vrednosti pa zopet tabele [slovar, slika]
        kjer so ključi slovarja trgovine (mercator, spar, tus) vrednosti pa cena izdelka v posamezni 
        spletni trgovini. Če izdelka ne najdemo, ga izpustimo.
        """
        options = Options()
        options.add_argument("--headless")
        slovar_izdelkov = {}
        brskalnik = webdriver.Chrome(options=options, executable_path='/PridobivanjePodatkov/chrome/chromedriver.exe')
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
                wait = WebDriverWait(brskalnik, 20)
                brskalnik.get(mercator_url)
                # pobrisemo pojavna okenca (cookie, adds), da pridemo do dejanske spletne strani
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div/a[2]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div[1]/a'))).click()
                izdelek_mercator_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="grid"]/div[1]/div[1]/div[4]/div[2]/strong')))
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
                wait = WebDriverWait(brskalnik, 20)
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
                wait = WebDriverWait(brskalnik, 20)
                brskalnik.get(tus_url)
                izdelek_tus_tab = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/section[1]/div/div/div/div/div[2]/ul/li[1]/div/span[1]')))
                izdelek_tus = izdelek_tus_tab[0].text
                cena_tus = float(izdelek_tus.replace(",", ".")[:-2])
                slovar_cen["TUS"] = cena_tus
                print(cena_tus)
            except:
                print("NAPAKA: tus")
                continue
            print(slovar_cen)
            slovar_izdelkov[izdelek] = [slovar_cen, slika_src]
        return slovar_izdelkov

    def napolni_bazo(self, conn, datoteka):
        """
        Funkcija iz datoteke prebere INSERT stavke in jih
        zažene na podani povezavi
        """
        with open(datoteka) as dat:
            vrstica = dat.readline().strip()
            while vrstica != "":
                try:
                    conn.execute(vrstica)
                except:
                    print("Napaka pri vnašanju podatkov v bazo")
                vrstica = dat.readline().strip()
    
    def izprazni_bazo(self, conn, ime_tabele):
        """
        Funkcija izbriše vse podatke iz podane tabele v bazi
        """
        sql_niz = f"DELETE FROM {ime_tabele};"
        try:
            conn.execute(sql_niz)
        except:
            print(f"Napaka pri brisanju podatkov iz tabele {ime_tabele}")


# tab = datoteka_v_tabelo("/Users/damijanrandl/Downloads/izdelki.txt")
# slovar = pridobivanje_cen_izdelkov(tab)
# slovar_v_sql(slovar, "Izdelki", "/Users/damijanrandl/Downloads/insert_stavki.txt")
