import nmap
import sys
import time
import os
import datetime

date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
reportName = str(date) + "_rawData" + ".txt"
scanReport = open(reportName, "a")

class PingHosts:

    """
    network initialisation
    """
    def __init__(self, networkPrefix):
        self.networkPrefix = networkPrefix
    ##

    def nmapPingScan(self):
        t1 = time.time()
        nm = nmap.PortScanner()
        activeHosts = []
        """
        Perform simple ping and create a list of online hosts
        This is acceptable scanning speed and realiability for bunch of /16 network
        """

        raw_result = nm.scan(hosts=self.networkPrefix, arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -sP')
        #print(pingScanRawResult)
        for result in raw_result['scan'].values():
            #print(result)
            if result['status']['state'] == 'up':
                activeHosts.append(result['addresses']['ipv4'])
        totalActiveHosts = ("There are " + str(len(activeHosts)) + " active hosts online. The hosts are: \n" + '\n'.join('{}: {}'.format(*k) for k in enumerate(activeHosts, start=1)) + "\n")
        scanReport.write(totalActiveHosts)
        """
        1-1024 popular port
        1194 openVPN
        1433 Microsoft SQL Server
        1434 Microsoft SQL Monitor
        2483-2484 Oracle database
        3306 MySQL database service
        4333 mSQL
        5432 PostgreSQL database
        8080 HTTP Proxy such as Apache
        27017 Mongo database
        """
        for host in activeHosts:
            fullScanRawResults = nm.scan(hosts=host, arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -v', ports="1-1024, 1433-1434, 2483-2484, 800, 3306, 4333, 5432, 5000, 8080, 9000, 8433, 27017, 50000")
            #print(fullScanRawResults)
            for host, result in fullScanRawResults['scan'].items():
                if result['status']['state'] == 'up':
                    hostDecoration = ('#' * 17 + 'Host: ' + host + '#' * 17 + "\n")
                    scanReport.write(hostDecoration)
                    idno = 1
                    try:
                        for port in result['tcp']:
                            try:
                                id = ('-' * 17 + 'TCP Service Detail' + '[' + str(idno) + ']' + '-' * 17  + "\n")
                                scanReport.write(id)
                                idno = idno + 1
                                portNum = ('TCP Port Number: ' + str(port)  + "\n")
                                scanReport.write(portNum)
                                try:
                                    portStatus = ('Status:' + result['tcp'][port]['state'] + "\n")
                                    scanReport.write(portStatus)
                                except:
                                    pass
                                try:
                                    reason = ('reason:' + result['tcp'][port]['reason'] + "\n")
                                    scanReport.write(reason)
                                except:
                                    pass
                                try:
                                    info = ('Additional Info' + result['tcp'][port]['extrainfo'] + "\n")
                                    scanReport.write(info)
                                except:
                                    pass
                                try:
                                    service = ('Service: ' + result['tcp'][port]['name'] + "\n")
                                    scanReport.write(service)
                                except:
                                    pass
                                try:
                                    version = ('version: ' + result['tcp']['version'] + "\n")
                                    scanReport.write(version)
                                except:
                                    pass
                                try:
                                    product = ('product: ' + result['tcp'][port]['product'] + "\n")
                                    scanReport.write(product)
                                except:
                                    pass
                                try:
                                    script = ('Script: ' + result['tcp'][port]['script'] + "\n")
                                    scanReport.write(script)
                                except:
                                    pass
                            except:
                                pass
                    except:
                        pass

                    try:
                        ipAddr = ('IP Address: ' + result['addresses']['ipv4'] + "\n")
                        macAddr = ('MAC Address: ' + result['addresses']['mac'] + "\n")
                        scanReport.write(ipAddr)
                        scanReport.write(macAddr)
                    except:
                        pass
        t2 = time.time()
        timeUsed = ("-" * 17 + "Time Used" + '-' * 17 + "\n" + str("Used %.2f"%(t2 - t1) + " seconds") + "\n")
        scanReport.write(timeUsed)
        print("\n" + "#" * 25 + "\n" + "##Scan Report Created!!##" + "\n" + "#" * 25 + "\n")

try:
    f = open(input("Please enter the path for the files that contains address: "), "r")
    network = f.read()
except:
    print("Please enter a valid file path")

    #This is acceptable scanning speed and realiability for bunch of /16 network

test1 = PingHosts(network)
test1.nmapPingScan()