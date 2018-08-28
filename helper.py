import requests
import re

xmls = []
threddsInfoDict = {}
for candidate in threddsCandidateHostList:
    if 'html' in candidate:
        links = candidate.replace("html", "xml")
        xmls.append(links)
    # print(type(links))


#print(xmls)
services = ['OPENDAP', 'DAP4', 'HTTPServer', 'WCS', 'WMS', 'NetcdfSubset']
hostServicesDict = {}
hostServiceList = []
urls = ''
content = ''
for xml in xmls:

    #hosts = re.findall( r'[0-9]+(?:\.[0-9]+){3}', xml)
    try:
        r = requests.get(xml, timeout=0.5, allow_redirects=False)
        content = str(r.content).lower()
        urls = r.url
    except:
        pass

for service in services:
    if service.lower() in content:
        # print(r.url, service)
        hostServiceList.append(service)
print(hostServiceList)

if service not in hostServicesDict:
    hostServicesDict[urls] = hostServiceList




print(hostServicesDict)

