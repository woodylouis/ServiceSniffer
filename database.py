import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_host(conn, host):

    sql = ''' INSERT INTO host(host_ip, port, server_url)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host)
    return cur.lastrowid

def create_service(conn, service):

    sql = ''' INSERT INTO service(service_type)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, service)
    return cur.lastrowid