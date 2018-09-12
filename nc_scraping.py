from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import requests
from itertools import takewhile
import store
import tds_host
from urllib.parse import urlsplit

url = "http://152.83.247.62:80/thredds/catalog.xml"
hostFilesDict = {}

def find_files(urls):

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

# {'http://152.83.247.62:80/thredds/wcs/SMIPS/SMIPSv0.5.nc': ['SMIPSv0.5', 'SMIPSv0.5 Total Outputs'], 'http://152.83.247.62:80/thredds/dodsC/SMIPS/SMIPSv0.5.nc': ['SMIPSv0.5', 'SMIPSv0.5 Total Outputs'], 'http://152.83.247.62:80/thredds/dap4/SMIPS/SMIPSv0.5.nc': ['SMIPSv0.5', 'SMIPSv0.5 Total Outputs'], 'http://152.83.247.62:80/thredds/wms/SMIPS/SMIPSv0.5.nc': ['SMIPSv0.5', 'SMIPSv0.5 Total Outputs']}

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


    for link in listOfLinks:

        urlPortion = urlsplit(link, allow_fragments=True)
        # print(urlPortion)
        hostIpWithPort = urlPortion.netloc
        r = requests.get(link, timeout=0.5, allow_redirects=False)
        #print(r.status_code)
        soup = BeautifulSoup(r.text, features="lxml")
        catalog = soup.find('catalog')
        for dataset in catalog.find_all('dataset'):
            for subDataset in dataset.find_all('dataset'):
                print(urlPortion.hostname, subDataset['name'])



if __name__ == '__main__':
    listOfFile = find_files(url)
    catch_data_into_nc_files(listOfFile)
    listOfUrl = tds_host.getCandiateUrl()
    listOfLinks = getHomeLink(listOfUrl)
    getLinksOrFilesFromHomeDirectories(listOfLinks)




def catalog_ref_in_home():
    hrefs = []
    # for a in soup.find_all('catalogRef'.lower()):
    #     hrefs.append(a['xlink:href'])
    # return hrefs
# show what you've found:
# links = []
# for link in list_of_links:
#     urlPortion = url.split('/')
#     hostOnly = f"{urlPortion[0]}//{urlPortion[2]}"
#     hosthostWithThredds = f"{hostOnly}/{urlPortion[3]}/"
#
#     #['http:', '', '152.83.247.62:80', 'thredds', 'catalog.xml']
#     if "/thredds/catalog/" in link:
#         alink = (hostOnly + link)
#         links.append(alink)
#     else:
#         alink = hosthostWithThredds + link
#         links.append(alink)
# print(links)
#
# subDirectory = []
# validUrlInHome = []
# for link in links:
#
#
#     r = requests.get(link, timeout=0.5, allow_redirects=False)
#     """
#     We can get valid xlink in the home thredds catalog page in here
#     """
#     if r.status_code == 200:
#         validUrlInHome.append(r.url)

#print(validUrlInHome)
# def getValid():
#     for url in validUrlInHome:
#
#         subCatalogRef = find_files(url)
#         #print(len(subCatalogRef) == 0)
#         if len(subCatalogRef) != 0:
#             subDirectory.append(subCatalogRef)
#         else:
#             #print(len(subDirectory) == 0)
#             soup = BeautifulSoup(requests.get(url).text, features="lxml")
#             #print(soup)
#             ncs = []
#             dataset = soup.find_all('urlpath')
#             print(dataset)
#
# test = getValid()



