from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import requests
from itertools import takewhile


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
    print(hostDatasetDict)





