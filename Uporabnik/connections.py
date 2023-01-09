import psycopg2
import urllib.parse as up
import config


def start_connDB():
    up.uses_netloc.append("postgres")
    url = up.urlparse(config.dburl)
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
    conn.set_session(autocommit=True)
    return conn


def check_connDB():
    try:
        up.uses_netloc.append("postgres")
        url = up.urlparse(config.dburl)
        conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host='peanut.db.elephantsql.com', port=url.port )
        conn.set_session(autocommit=True)
        return True
    except:
        return False