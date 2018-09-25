import scan

# def getCandiateUrl():
#     candidateList = []
#     try:
#         with open(f"C:\\Users\LI252\Desktop\ScanResults\ScanReport Request.txt", "r") as reportFile:
#             for line in reportFile.read().splitlines():
#                 if 'may have Thredds installed' in line:
#                     print('T')
#
#
#     except:
#         print("Invalid file to interrogate valid thredds")
#
# getCandiateUrl()
"""

Local config file. 
In the file,
IP network address should be like:

192.168.1.0/24
192.168.2.0/24
192.168.3.0/24

"""
try:
    f = open(input("Please enter the path for the files that contains address: "), "r")
    network = f.read()
except:
    print("Please enter a valid file path")




scan.get_thredds_hosts(network)