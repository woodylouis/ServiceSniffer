import nmap
import time
import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import database

date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
reportName = str(date) + "_ScanReport" + ".txt"
scanReport = open(reportName, "a")

def get_thredds_hosts(network_prefix):
    t1 = time.time()
    nm = nmap.PortScanner()
    activeHosts = []
    portDict = {}
    hostInfoDict = {}
    """
    Perform simple ping and create a list of online hosts
    This is acceptable scanning speed and realiability for bunch of /16 network
    """
    pingResult = nm.scan(hosts=network_prefix,
                         arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -sP')

    for pResult in pingResult['scan'].values():
        hostStatus = pResult['status']['state']
        host = pResult['addresses']['ipv4']
        if hostStatus == 'up':
            activeHosts.append(host)
    totalActiveHosts = ("There are " + str(len(activeHosts)) + " active hosts online. The hosts are: \n" + '\n'.join(
        '{}: {}'.format(*k) for k in enumerate(activeHosts, start=1)) + "\n")
    # scanReport.write(str(totalActiveHosts))
    # scanReport.write(totalActiveHosts)
    # """
    # 1-1024 popular port
    # 1194 openVPN
    # 1433 Microsoft SQL Server
    # 1434 Microsoft SQL Monitor
    # 2483-2484 Oracle database
    # 3306 MySQL database service
    # 4333 mSQL
    # 5432 PostgreSQL database
    # 8080 HTTP Proxy such as Apache
    # 27017 Mongo database
    # """
    for host in activeHosts:
        aDict = nm.scan(hosts=host,
                        arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -v',
                        ports="80, 1433-1434, 2483-2484, 800, 3306, 4333, 5432, 5000, 8080, 9000, 8433, 27017, 50000")
        scanReport.write(str(aDict))
        for serviceScan in aDict['scan'].values():
            host = serviceScan['addresses']['ipv4']
            try:
                portInfo = serviceScan['tcp']
            except:
                pass
            for port, info in portInfo.items():
                hostServices = info['name']
                portState = info['state']
                """
                Get all hosts' HTTP service and port in a dictionary
                """
                if portState == 'open' and 'http' in hostServices:
                    if port not in portDict:
                        portDict[port] = hostServices
                    if host not in hostInfoDict:
                        hostInfoDict[host] = portDict
    # print(hostInfoDict)

    httpHostStatusDict = {}
    for host, hostInfo in hostInfoDict.items():
        for port in hostInfo.keys():
            urls = f'http://{host}:{port}/thredds/catalog.html'
            # print(urls)
            try:
                r = requests.get(urls, timeout=0.5, allow_redirects=False)
                # print(r.url)
                if str(r.url) not in httpHostStatusDict:
                    httpHostStatusDict[str(r.url)] = str(r.status_code)
            except requests.exceptions.HTTPError:
                """An HTTP error occurred."""
                pass
            except requests.exceptions.ConnectionError:
                """A Connection error occurred."""
                pass
            except requests.exceptions.Timeout:
                """
                The request timed out while trying to connect to the remote server.

                Requests that produced this error are safe to retry.
                """
                pass
            except requests.exceptions.RequestException:
                """
                There was an ambiguous exception that occurred while handling your request.
                """
                pass
    # print(httpHostStatusDict)
    threddsCandidateHostList = []
    noThreddsInstalledHostList = []
    redirectToOtherURL = []
    unknownError = []
    for urls, status in httpHostStatusDict.items():
        if status == '404':
            noThreddsInstalledHostList.append(urls)
        elif status == '302':
            # redirect to CISCO gateway login page or link has been moved permanently
            redirectToOtherURL.append(urls)
        elif status == '200':
            threddsCandidateHostList.append(urls)
        else:
            unknownError.append(urls)
        # print("There are", len(redirectToOtherURL), "urls redirect to firewall login page\n", redirectToOtherURL, '\n')
        # print("There are", len(threddsCandidateHostList), "urls may have Thredds installed\n", threddsCandidateHostList, '\n')
        # print("There are", len(noThreddsInstalledHostList), "urls have no Thredds installed in these hosts\n", noThreddsInstalledHostList, '\n')
        # print("There are", len(unknownError), "unknown error urls\n", unknownError, '\n')
        # for candidate in threddsCandidateHostList:
        #     print(type(candidate))
    return threddsCandidateHostList
    # print(threddsCandidateHostList)
    # """
    # Perform xml analysis below and start getting thredds service type here
    # """

def get_services():



    xmls = []
    hostServiceDict = {}

    """
    # Perform xml analysis below and start getting thredds service type here
    """
    for candidate in candidate_list:
        if 'html' in candidate:
            links = candidate.replace("html", "xml")
            xmls.append(links)
    s = 'serviceType='
    services = ['"OPENDAP"', '"DAP4"', '"HTTPServer"', '"WCS"', '"WMS"', '"NetcdfSubset"', '"HTTP"', '"NCSS"', '"NCML"', '"UDDC"', '"ISO"']
    content = ''
    serviceTypes = []
    urlList = []
    hostDict = {}
    for service in services:
        # print(type(service))
        t = s + service
        serviceTypes.append(t)
    # print(serviceTypes)
    for xml in xmls:
        try:
            r = requests.get(xml, timeout=0.5, allow_redirects=False)
            content = str(r.content).lower()
            urls = r.url
            urlList.append(urls)
            if urls not in hostDict:
                hostDict[urls] = content
        except:
            pass

    # print(urlList)
    for urls, urlInfo in hostDict.items():
        # print(urlInfo)
        for serviceType in serviceTypes:
            if serviceType.lower() in urlInfo.lower():
                pass
                s = [urls, serviceType]
                hostServiceDict.setdefault(urls, []).append(serviceType.strip("serviceType=").replace('"', ''))
    #print(hostServiceDict)
    return hostServiceDict

"""""""""
capture data to database here
"""""""""
def capture_host_in_db(hostServiceDict):
    #print(hostServiceDict)
    database = "C:\\Users\LI252\PycharmProjects\servicesniffer\database\sniffing.database"
    conn = create_connection(database)
    with conn:

        hostTemp = []
        for urls, services in hostServiceDict.items():
            host_port = urls.strip('http://').strip('thredds/catalog.xml').split(':')
            hostTemp.append(host_port[0])


            for host in hostTemp:
                """
                Check if the hosts that already in the database. If not in the database, add the hosts.
                """
                if host != select_host_by_host_ip(conn, host):
                    thredds = (host_port[0], host_port[1], urls)
                    create_unique_host(conn, thredds)



        temp = []
        for service in hostServiceDict.values():
            for i in service:
                temp.append(i)

        """
        Check if the services that the hosts have. If not in the database, add the new service in the database.
        """
        # i > theService:
        # i means all the services that are hosted per servers. theService is a unique service in database.
        for i in temp:
            theService = select_service(conn, i)
            if i != theService:
                create_unique_service(conn, i)

        # for urls, services in hostServiceDict.items():
        #     host_port = urls.strip('http://').strip('thredds/catalog.xml').split(':')
        #     hostTemp.append(host_port[0])
        #     for host in hostTemp:
        #         if host == select_host_by_host_ip(conn, host):
        #             host_id = select_host_id_by_host_ip(conn, host)
        #             print(host_id)

                #create_unique_host_service(conn, hostAndService)



        #print(hostServiceDict)
        #theService = select_service(conn, 'DAP4')



    # t2 = time.time()
    # print("-" * 17 + "Time Used" + '-' * 17 + "\n" + str("Used %.2f" % (t2 - t1) + " seconds"))



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
    cur.execute("SELECT host_ip FROM host WHERE host_ip = ?", (host_ip,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aHost = rows[i][0]
        return aHost

def select_host_id_by_host_ip(conn, host_ip):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(id) FROM host WHERE host_ip = ?", (host_ip,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aHostID = rows[i]
        print(aHostID)

def create_unique_host(conn, host):

    sql = ''' INSERT INTO host(host_ip, port, server_url)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host)
    return cur.lastrowid

def create_unique_service(conn, service):

    sql = ''' INSERT INTO service(service_type)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (service,))
    return cur.lastrowid


def select_service(conn, service):

    cur = conn.cursor()
    cur.execute("SELECT service_type FROM service WHERE service_type = ?", (service,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aService = rows[i][0]
        return aService

def select_service_id_by_name(conn, service):
    cur = conn.cursor()
    cur.execute("SELECT id FROM service WHERE service_type = ?", (service,))
    rows = cur.fetchall()
    for i in range(len(rows)):
        aServiceID = rows[i][0]
        return aServiceID


def create_unique_host_service(conn, host_service_by_id):
    sql = ''' INSERT INTO host_service(host_id, service_id )
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host_service_by_id)


# try:
#     f = open(input("Please enter the path for the files that contains address: "), "r")
#     network = f.read()
# except:
#     print("Please enter a valid file path")


if __name__ == '__main__':
    #hosts = get_thredds_hosts(network)
    #hosts_services = get_services(hosts)
    hosts_services = get_services()
    capture_host_in_db(hosts_services)



