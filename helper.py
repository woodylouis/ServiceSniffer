import requests
from collections import defaultdict
from operator import itemgetter
import re
xmls = []
threddsInfoDict = {}
threddsCandidateHostList = []
for candidate in threddsCandidateHostList:
    if 'html' in candidate:
        links = candidate.replace("html", "xml")
        xmls.append(links)
    # print(type(links))


#print(xmls)
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
#print(serviceTypes)

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

#print(urlList)

s = []

threddsInfoDict = {}
for urls, urlInfo in hostDict.items():
    #print(urlInfo)
    for serviceType in serviceTypes:
        if serviceType.lower() in urlInfo.lower():
            pass
            s = [urls, serviceType]
            threddsInfoDict.setdefault(urls, []).append(serviceType.strip("serviceType=").replace('"', ''))

print(threddsInfoDict)
