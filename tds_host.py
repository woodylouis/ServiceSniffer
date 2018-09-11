import requests
import sqlite3
from sqlite3 import Error
import re
import store

hostServiceDict = {}
def get_services(candidate_list):
    #print(len(candidate_list))
    ###
    # Candiadte_list = ['http://host_ip_1:port/thredds/catalog.html', 'http://host_ip_2:port/thredds/catalog.html', 'http://host_ip_3:port/thredds/catalog.html'] #
    ###

    xmls = []
    """
    # Perform xml analysis below and start getting thredds service type here, replace html with xml
    """
    for candidate in candidate_list:
        if 'html' in candidate:
            links = candidate.replace("html", "xml")
            xmls.append(links)
    s = 'serviceType='
    services = ['"OPENDAP"', '"DAP4"', '"HTTPServer"', '"WCS"', '"WMS"', '"NetcdfSubset"', '"HTTP"', '"NCSS"', '"NCML"', '"UDDC"', '"ISO"']
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
            r = requests.get(xml, timeout=3, allow_redirects=False)
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
    #return hostServiceDict

    """""""""
    Remove duplicated hosts with different port e.g. 80/8080 but they have same service types
    """""""""
    result = {}
    seen_ips = set()
    for url, services in hostServiceDict.items():
        ip = url.strip('http://').strip('thredds/catalog.xml').split(':')[0]
        if ip not in seen_ips:
            seen_ips.add(ip)
            result[url] = services
    return result

"""""""""
capture data to database here
"""""""""
def capture_host_in_db(result):
    #
    #print(hostServiceDict)
    database = "C:\\Users\LI252\PycharmProjects\servicesniffer\database\database.sqlite"
    conn = store.create_connection(database)
    with conn:

        hostTemp = []
        existingHostIps = []
        existingHostId = []

        for urls, services in result.items():
            host_port = urls.strip('http://').strip('thredds/catalog.xml').split(':')
            #print(host_port)
            hostTemp.append(host_port[0])
            for host in hostTemp:
                """
                Check if the hosts that already in the database. If not in the database, add the hosts.
                """
                try:
                    if host != store.select_host_by_host_ip(conn, host):
                        thredds = (host_port[0], host_port[1], urls)
                        store.create_unique_host(conn, thredds)
                except:
                    print("Failed to store host services into host_services table. Please check if the hosts have ports after IP addresses e.g. 192.168.1.1/80 in the threddsCandidates.txt file")

            for service in services:

                """
                Create unique service
                """
                theService = store.select_service(conn, service)
                if service != theService:
                    store.create_unique_service(conn, service)

        for urls, services in result.items():
            host = urls.strip('http://').strip('thredds/catalog.xml').split(':')
            hostId = store.select_host_id_by_host_ip(conn, host[0])
            # print(hostId)
            for service in services:
                # print(service)
                theService = store.select_service(conn, service)
                if service == theService:
                    serviceId = store.select_service_id_by_name(conn, service)
                    hs = hostId[0], serviceId
                    """
                    compare existing hosts and services in host_services_table, if not exist, add to the table
                    """
                    existingPair = store.select_host_services_by_host_id_and_service_id(conn, hs)
                    #print(existingPair)
                    if hs != existingPair:
                        store.create_unique_host_service(conn, hs)

def getCandiateUrl():
    candidateList = []
    try:
        with open(f"C:/Users/LI252/Desktop/threddsCandiates.txt", "r") as tdsFile:
            for url in tdsFile.read().splitlines():
                candidateList.append(url)
            return candidateList

    except:
        print("Invalid file to interrogate valid thredds")


if __name__ == '__main__':
    hosts = getCandiateUrl()
    hosts_services = get_services(hosts)
    capture_host_in_db(hosts_services)