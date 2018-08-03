import nmap
import sys
import time
import os

class PingHosts:
    ## network initialisation
    def __init__(self, networkPrefix):
        self.networkPrefix = networkPrefix
    ## Perform simple ping and create a list of online hosts

    def nmapPingScan(self):
        t1 = time.time()
        nm = nmap.PortScanner()
        activeHosts = []

        #This is acceptable scanning speed and realiability for bunch of /16 network
        pingScanRawResult = nm.scan(hosts=self.networkPrefix, arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -sP')
        print(pingScanRawResult)
        for result in pingScanRawResult['scan'].values():
            print(result)
            if result['status']['state'] == 'up':
                activeHosts.append(result['addresses']['ipv4'])
        print("There are " + str(len(activeHosts)) + " active hosts online. The hosts are: \n" + '\n'.join('{}: {}'.format(*k) for k in enumerate(activeHosts, start=1)) + "\n")
        ## 1-1024 popular port
        ## 1194 openVPN
        ## 1433 Microsoft SQL Server
        ## 1434 Microsoft SQL Monitor
        ## 2483-2484 Oracle database
        ## 3306 MySQL database service
        ## 4333 mSQL
        ## 5432 PostgreSQL database
        ## 8080 HTTP Proxy such as Apache
        ## 27017 Mongo database
        for host in activeHosts:
            fullScanRawResults = nm.scan(hosts=host, arguments='--min-hostgroup=5000 --max-hostgroup=100000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -v', ports="1-1024, 1433-1434, 2483-2484, 800, 3306, 4333, 5432, 5000, 8080, 9000, 8433, 27017, 50000")
            #print(fullScanRawResults)
            for host, result in fullScanRawResults['scan'].items():
                if result['status']['state'] == 'up':
                    print('#' * 17 + 'Host: ' + host + '#' * 17)
                    idno = 1
                    try:
                        for port in result['tcp']:
                            try:
                                print('-' * 17 + 'TCP Service Detail' + '[' + str(idno) + ']' + '-' * 17)
                                idno = idno + 1
                                print('TCP Port Number: ' + str(port))
                                try:
                                    print('Status:' + result['tcp'][port]['state'])
                                except:
                                    pass
                                try:
                                    print('reason:' + result['tcp'][port]['reason'])
                                except:
                                    pass
                                try:
                                    print('Additional Info' + result['tcp'][port]['extrainfo'])
                                except:
                                    pass
                                try:
                                    print('Service: ' + result['tcp'][port]['name'])
                                except:
                                    pass
                                try:
                                    print('version: ' + result['tcp']['version'])
                                except:
                                    pass
                                try:
                                    print('product: ' + result['tcp'][port]['product'])
                                except:
                                    pass
                                try:
                                    print('Script: ' + result['tcp'][port]['script'])
                                except:
                                    pass
                            except:
                                pass
                    except:
                        pass

                    idno = 1
                    try:
                        for port in result['udp']:
                            try:
                                print('-' * 17 + 'UDP Service Detail' + '[' + str(idno) + ']' + '-' * 17)
                                idno = idno + 1
                                print('UDP Port Number:' + str(port))
                                try:
                                    print('Status: ' + result['udp'][port]['state'])
                                except:
                                    pass
                                try:
                                    print('Reason:' + result['udp'][port]['reason'])
                                except:
                                    pass
                                try:
                                    print('Additional Info' + result['udp'][port]['extrainfo'])
                                except:
                                    pass
                                try:
                                    print('Service: ' + result['udp'][port]['name'])
                                except:
                                    pass
                                try:
                                    print('Version: ' + result['udp']['version'])
                                except:
                                    pass
                                try:
                                    print('product: ' + result['udp'][port]['product'])
                                except:
                                    pass
                                try:
                                    print('Script: ' + result['udp'][port]['script'])
                                except:
                                    pass
                            except:
                                pass
                    except:
                        pass
                    print('-' * 20 + 'IP address detail' + '-' * 20)
                    try:
                        print('IP Address: ' + result['addresses']['ipv4'])
                        print('MAC Address: ' + result['addresses']['mac'])
                    except:
                        pass
        t2 = time.time()
        print("-" * 17 + "Time Used" + '-' * 17 + "\n" + str("Used %.2f"%(t2 - t1) + " seconds"))







