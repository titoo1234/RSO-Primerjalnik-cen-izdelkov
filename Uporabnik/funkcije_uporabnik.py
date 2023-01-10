import hashlib
import connections
import pandas as pd

def password_md5(s):
    '''
    Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
    kodirana s to funkcijo.
    '''
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def preveri_ime_geslo(ime, geslo):
    '''
    Preveri, če je ime in geslo pravilno
    '''
    query = "SELECT * FROM uporabniki WHERE ime=%s and geslo = %s;"
    conn = connections.start_connDB()
    cur = conn.cursor()
    cur.execute(query, (ime, geslo))
    rez = cur.fetchall()
    if len(rez) == 1:
        conn.close()
        return True
    conn.close()
    return False

def obstaja_uporabnik(ime):
    '''
    Preveri, če je obstaja uporabnik z imenom ime
    '''
    query = "SELECT * FROM uporabniki WHERE ime=%s;"
    conn = connections.start_connDB()
    cur = conn.cursor()
    cur.execute(query, (ime,))
    rez = cur.fetchall()
    if len(rez) == 1:
        conn.close()
        return True
    conn.close()
    return False