from netCDF4 import Dataset
import requests
import os
import re

dataset = Dataset("C:/Users/LI252/Desktop/SMIPSv0.5.nc")
print(dataset.variables)

# def getHost():
#
#
# def getInto(hosts):
#     r = requests.get(hosts, timeout=0.5, allow_redirects=False)
#     f = open("temp.txt", "w")
#     f.write(r.text)
#
# def removeTempFile():
#     os.remove("temp.txt")
#
# def getURLsFromPage():
#     host = "152.83.247.7"
#     aList = []
#     file = open("temp.txt", "r").readlines()
#     for line in file:
#         if ".html" in line:
#             aList.append(str(line))
#     urls = set()
#     for link in aList:
#         urls.update(re.findall(r'href=[\'"]?([^\'" >]+)', link))
#         """
#         getting valid address
#         """
#     #print(urls)
#     addrs = []
#     for url in urls:
#         if url[0] != '/':
#             test = 'http://' + host + '/thredds/' + url
#             addrs.append(test)
#         else:
#             test = 'http://' + host + url
#             addrs.append(test)
#     print(addrs)
#
#     addressDict = {}
#     for addr in addrs:
#         try:
#             r = requests.get(addr, timeout=0.5, allow_redirects=False)
#         # print(httpHost, r.status_code)
#         except requests.exceptions.HTTPError:
#             """An HTTP error occurred."""
#             pass
#         except requests.exceptions.ConnectionError:
#             """A Connection error occurred."""
#             pass
#         except requests.exceptions.Timeout:
#             """
#             The request timed out while trying to connect to the remote server.
#
#             Requests that produced this error are safe to retry.
#             """
#             pass
#         except requests.exceptions.RequestException:
#             """
#             There was an ambiguous exception that occurred while handling your request.
#             """
#             pass
#         else:
#             if addr not in addressDict:
#                 addressDict[addr] = str(r.status_code)
#     print("###There are", len(addressDict), "host\n", addressDict, "all hosts status Dict is above ###\n\n")
#
#     accessibleLink = []
#     for host, status in addressDict.items():
#         if status == '200':
#             accessibleLink.append(host)
#             print(accessibleLink)
#
#
#
#
#
# getInto("http://152.83.247.74/thredds/catalog.html")
#
# getURLsFromPage()
