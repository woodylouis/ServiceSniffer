from netCDF4 import Dataset
import requests
import os
import re

# dataset = Dataset("C:/Users/LI252/Desktop/SMIPSv0.5.nc")
# print(dataset.variables)



def getInto(url):
    r = requests.get(url)
    f = open("temp.txt", "w")
    f.write(r.text)

def removeTempFile():
    os.remove("temp.txt")

def getURLsFromPage():
    host = "152.83.247.74"
    aList = []
    file = open("temp.txt", "r").readlines()
    for line in file:
        if ".html" in line:
            aList.append(str(line))
    urls = set()
    for link in aList:
        urls.update(re.findall(r'href=[\'"]?([^\'" >]+)', link))
        """
        getting valid address
        """
    #print(urls)
    addr = []
    for url in urls:
        if url[0] != '/':
            test = 'http://' + host + '/thredds/' + url
            addr.append(test)
        else:
            test = 'http://' + host + url
            addr.append(test)
    print(addr)





getInto("http://152.83.247.74/thredds/catalog.html")
getURLsFromPage()
