import requests
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter
import re
import os
import urllib.request
from bs4 import BeautifulSoup

# xmls = []
# threddsInfoDict = {}
# for candidate in threddsCandidateHostList:
#     if 'html' in candidate:
#         links = candidate.replace("html", "xml")
#         xmls.append(links)
#     # print(type(links))
#
#
# #print(xmls)
# s = 'serviceType='
# services = ['"OPENDAP"', '"DAP4"', '"HTTPServer"', '"WCS"', '"WMS"', '"NetcdfSubset"', '"HTTP"', '"NCSS"', '"NCML"', '"UDDC"', '"ISO"']
# content = ''
# serviceTypes = []
# urlList = []
# hostDict = {}
# for service in services:
#     # print(type(service))
#     t = s + service
#     serviceTypes.append(t)
# #print(serviceTypes)
#
# for xml in xmls:
#     try:
#         r = requests.get(xml, timeout=0.5, allow_redirects=False)
#         content = str(r.content).lower()
#         urls = r.url
#         urlList.append(urls)
#         if urls not in hostDict:
#             hostDict[urls] = content
#     except:
#         pass
#
# #print(urlList)
#
# s = []
#
# threddsInfoDict = {}
# for urls, urlInfo in hostDict.items():
#     #print(urlInfo)
#     for serviceType in serviceTypes:
#         if serviceType.lower() in urlInfo.lower():
#             pass
#             s = [urls, serviceType]
#             threddsInfoDict.setdefault(urls, []).append(serviceType.strip("serviceType=").replace('"', ''))
# print(threddsInfoDict)
linkList = []
def RecurseLinks(url):
    try:
        web = urllib.request.urlopen(url)
        soup = BeautifulSoup(web.read(), features="xml")
    except:
        pass

    host = url.strip('http://').strip('/thredds/catalog.xml')
    #print(host)
    hostServiceDict = {}
    """""
    Get services types
    """""
    for service in soup.find_all("service"):
        name = service.get("name")
        base = service.get("base")
        if name not in hostServiceDict:
            hostServiceDict[name] = base


    # get absolute directory path in the dict
    newHostServiceDict = {k: hostServiceDict[k] for k in hostServiceDict if hostServiceDict[k]}
    # print(newHostServiceDict) #{'odap': '/thredds/dodsC/', 'dap4': '/thredds/dap4/', 'http': '/thredds/fileServer/', 'wcs': '/thredds/wcs/', 'wms': '/thredds/wms/'}

    """""
    This dataset tag contains .nc files and in the thredds home catelog
    """""

    try:
        ncFileList = []
        for dataset in soup.find_all("dataset"):
            dataset = dataset.get("urlPath")
            for url in newHostServiceDict.values():
                ncFilePath = f"http://{host}{url}{dataset}"
                ncFileList.append(ncFilePath)
        print(ncFileList)
    except:
        pass

    """""
    This catalogrRef tag contains links
    """""
    try :
        for catalogrRef in soup.find_all("catalogRef"):
            xlink = catalogrRef.get("xlink:href")
            #print(xlink)
            if xlink.startswith("/"):
                xlinks = f"http://{host}{xlink}"
                linkList.append(xlinks)

            else:
                xlinks = f"http://{host}/thredds/{xlink}"
                #print(xlinks)
                linkList.append(xlinks)
        print(linkList)

    except:
        pass

    for link in linkList:
        RecurseLinks(link)






   #  for ncFilePath in newNcFileList:
   #      r = requests.get(ncFilePath, allow_redirects=False)
   #      print(r, r.url)

                # r = requests.get(ncFilePath, timeout=0.5, allow_redirects=False)
                # aList = [f"{r.status_code}", r.url]
                # if aList[0] == "200":
                #     ncFileList.append(aList[1])
                #     print(ncFileList)



    #
    # for dataset in soup.find_all("dataset"):
    #     xlink = dataset.get("urlPath")
    #     #print(xlink)
    #
    # subUrlList = []
    # aList = []
    # subUrl = []
    # for link in linkList:
    #     web = urllib.request.urlopen(link)
    #     soup = BeautifulSoup(web.read(), features="xml")
    #
    #
    #
    #     for catalogrRef in soup.find_all("catalogRef"):
    #         xlink = catalogrRef.get("xlink:href")
    #         #print(xlink)
    #         link = link.rstrip('catalog.xml') + xlink
    #         subUrlList.append(link)
    #         for aLink in subUrlList:
    #             r = requests.get(aLink, timeout=0.5, allow_redirects=False)
    #             aList = [f"{r.status_code}", r.url]
    #             if aList[0] == "200":
    #                 subUrl.append(aList[1])
    # #print(subUrl)





#
# for link in linkList:
#     try:
#         RecurseLinks(link)
#     except:
#         pass


#
# r = requests.get(urls, timeout=0.5, allow_redirects=False)
# print(r)
# print(r.content)