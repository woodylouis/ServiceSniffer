from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import requests
from itertools import takewhile
import store
import tds_host
from urllib.parse import urlsplit

hostFilesDict = {}

def find_files_from_home_page(urls):

    host = urls.strip('http://').strip('thredds/catalog.xml').split(':')
    #print(host)
    hostIP = host[0]
    port = host[1]
    r = requests.get(urls, timeout=0.5, allow_redirects=False)
    soup = BeautifulSoup(r.text, features="lxml")
    ncs = []
    a = []
    catalog = soup.find('catalog')
    serviceTemp = {}
    hostDatasetDict = {}


    for services in catalog.find_all('service'):
            for service in services.find_all('service'):
                name = service['name']
                serviceType = service['serviceType'.lower()]
                base = service['base']
                if name not in serviceTemp:
                    serviceTemp[base] = [name, serviceType]
    #print(serviceTemp)

    try:
        for header in catalog.find_all('dataset'):
            for serviceName in header.find('servicename'):
                description = header['id']
                ncName = header['name']
                ncURLPath = header['urlpath']
                for bases, names in serviceTemp.items():
                    if serviceName in names[0]:
                        path = f"http://{hostIP}:{port}{bases}{ncURLPath}"
                        # print(description, path, ncName)
                        if path not in hostDatasetDict:
                            hostDatasetDict[path] = [description, ncName]
    except:
        pass

    return (hostDatasetDict)


def catch_data_into_nc_files(hostDatasetDict):
    # for keys, items
    database = "C:\\Users\LI252\PycharmProjects\servicesniffer\database\database-test.sqlite"
    conn = store.create_connection(database)
    try:
        with conn:
            for keys, items in hostDatasetDict.items():
                urlSplite = keys.split('/')
                #print(urlSplite)
                serviceName = urlSplite[4]
                #print(serviceName)
                urlPortion = urlsplit(keys, allow_fragments=True)
                hostIp = urlPortion.hostname
                hostId = store.select_host_id_by_host_ip(conn, hostIp)
                #print(hostId)
                if serviceName == 'dodsC':
                    serviceType = 'opendap'.upper()
                    serviceId = store.select_service_id_by_name(conn, serviceType)
                    #print(serviceId)
                elif serviceName == 'ncss':
                    serviceType = 'NetcdfSubset'
                    #serviceId = store.select_service_id_by_name(conn, serviceType)
                elif serviceName == 'fileServer':
                    serviceType = 'HTTPServer'
                    serviceId = store.select_service_id_by_name(conn, serviceType)
                    #print(serviceId)
                else:
                    serviceId = store.select_service_id_by_name(conn, serviceName.upper())
                    #print(serviceId)
                description = items[0]
                ncName = items[1]
                ncRecord = (ncName, description, keys, serviceId, hostId)
                existing = store.select_nc_name_and_description_and_url_path_and_service_id_and_host_id(conn, ncRecord)
                #
                if ncRecord != existing:
                    store.create_nc_files_record(conn, ncRecord)

    except:
        pass


def getHomeLink(urls):
    listOfLinksInHomePage = []
    for url in urls:
        urlPortion = urlsplit(url, allow_fragments=True)
        #print(urlPortion)
        hostIpWithPort = urlPortion.netloc
        # print(hostIpWithPort)

        r = requests.get(url, timeout=0.5, allow_redirects=False)
        soup = BeautifulSoup(r.text, features="lxml")
        catalog = soup.find('catalog')


        """
        There are two situations: one is catalogRef directly shown in homepage xml, but another one is catalogRef is stored
        under dataset tag. We can get all directory links in the home catalog page here
        """
        try:

            try:
                for catalogRef in catalog.find_all('catalogref'):
                    #print(url, catalogRef['xlink:href'])
                    catalogRefUrl = catalogRef['xlink:href']
                    if "/thredds/" in catalogRefUrl:
                        completeURL = f"http://{hostIpWithPort}{catalogRefUrl}"
                        listOfLinksInHomePage.append(completeURL)
                    else:
                        completeURL = f"http://{hostIpWithPort}/thredds/{catalogRefUrl}"
                        listOfLinksInHomePage.append(completeURL)
            except:
                for dataset in catalog.find_all('dataset'):
                    for catalogRef in dataset.find_all('catalogref'):
                        catalogRefUrl = catalogRef['xlink:href']
                        if "/thredds/" in catalogRefUrl:
                            completeURL = f"http://{hostIpWithPort}{catalogRefUrl}"
                            listOfLinksInHomePage.append(completeURL)
                            #print(listOfLinksInHomePage)
                        else:
                            completeURL = f"http://{hostIpWithPort}/thredds/{catalogRefUrl}"
                            listOfLinksInHomePage.append(completeURL)
        except:
            print("Something Wrong")

    return listOfLinksInHomePage


def getLinksOrFilesFromHomeDirectories(listOfLinks):
    database = "C:\\Users\LI252\PycharmProjects\servicesniffer\database\database-test.sqlite"
    conn = store.create_connection(database)
    #
    # for link in listOfLinks:
    #     print(link)


    with conn:
        for link in listOfLinks:

            urlPortion = urlsplit(link, allow_fragments=True)
            hostIpWithPort = urlPortion.netloc
            hostIp = urlPortion.hostname
            hostId = store.select_host_id_by_host_ip(conn, hostIp)
            r = requests.get(link, timeout=0.5, allow_redirects=False)
            #print(r.status_code)
            soup = BeautifulSoup(r.text, features="lxml")
            catalog = soup.find('catalog')
            for dataset in catalog.find_all('dataset'):
                for subDataset in dataset.find_all('dataset'):
                    ncName = subDataset['name']
                    description = subDataset['id']
                    ncUrlPath = subDataset['urlpath']
                    #print('filename:',ncName, 'description:', description, 'path', ncUrlPath)
                    for services in catalog.find_all('service'):
                        for service in services.find_all('service'):
                            serviceName = service['name']
                            # print(serviceName)
                            serviceType = service['serviceType'.lower()]
                            base = service['base']
                            #print(base)
                            completeURL = f"http://{hostIpWithPort}{base}{ncUrlPath}"
                            if serviceName == 'odap':
                                serviceType = 'opendap'.upper()
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'dodsC':
                                serviceType = 'opendap'.upper()
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'ncss':
                                serviceType = 'NetcdfSubset'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'dap4':
                                serviceType = 'DAP4'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'subsetServer':
                                serviceType = 'NetcdfSubset'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'fileServer':
                                serviceType = 'HTTPServer'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'http':
                                serviceType = 'HTTPServer'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'wms':
                                serviceType = 'WMS'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                #print(serviceId, hostId)
                            elif serviceName == 'wcs':
                                serviceType = 'WCS'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'ncml':
                                serviceType = 'NCML'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)
                            elif serviceName == 'uddc':
                                serviceType = 'UDDC'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                #print(serviceId, hostId)
                            elif serviceName == 'iso':
                                serviceType = 'ISO'
                                serviceId = store.select_service_id_by_name(conn, serviceType)
                                # print(serviceId, hostId)

                    ncRecord = (ncName, description, completeURL, serviceId, hostId)
                    #print(ncRecord)

                    existing = store.select_nc_name_and_description_and_url_path_and_service_id_and_host_id(conn, ncRecord)
                    if ncRecord != existing:
                        #print(ncRecord)
                        store.create_nc_files_record(conn, ncRecord)

                    #print(urlPortion.hostname, subDataset['name'])
        #print(serviceTemp)

if __name__ == '__main__':
    listOfFile = find_files_from_home_page(url)
    catch_data_into_nc_files(listOfFile)
    listOfUrl = tds_host.getCandiateUrl()
    listOfLinks = getHomeLink(listOfUrl)
    getLinksOrFilesFromHomeDirectories(listOfLinks)






