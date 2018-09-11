import sqlite3
from sqlite3 import Error

"""""""""
database connection and SQL
"""""""""
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_host_by_host_ip(conn, host_ip):
    cur = conn.cursor()
    cur.execute("SELECT host_ip FROM hosts WHERE host_ip = ?", (host_ip,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aHost = rows[i][0]
        return aHost

def select_host_id_by_host_ip(conn, host_ip):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(id) FROM hosts WHERE host_ip = ?", (host_ip,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aHostID = rows[i]
        return (aHostID)

def select_host_id_by_server_url(conn, server_url):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(id) FROM hosts WHERE server_url = ?", (server_url,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aHostID = rows[i]
        return (aHostID)


def create_unique_host(conn, host):

    sql = ''' INSERT INTO hosts(host_ip, port, server_url)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host)
    return cur.lastrowid

def create_unique_service(conn, service):

    sql = ''' INSERT INTO services(service_type)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (service,))
    return cur.lastrowid


def select_service(conn, service):

    cur = conn.cursor()
    cur.execute("SELECT service_type FROM services WHERE service_type = ?", (service,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aService = rows[i][0]
        return aService

def select_service_id_by_name(conn, service):
    cur = conn.cursor()
    cur.execute("SELECT id FROM services WHERE service_type = ?", (service,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aServiceID = rows[i][0]
        return aServiceID


def create_unique_host_service(conn, host_service_by_id):
    sql = ''' INSERT INTO host_services(host_id, service_id )
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host_service_by_id)

def select_host_services_by_host_id_and_service_id(conn, pair_of_id):
    cur = conn.cursor()
    cur.execute("SELECT host_id, service_id FROM host_services WHERE host_id = ? AND service_id = ?", (pair_of_id))
    rows = cur.fetchall()
    for i in range(len(rows)):
        apairOfId = rows[i]
        return (apairOfId)