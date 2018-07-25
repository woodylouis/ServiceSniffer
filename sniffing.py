import nmap
import sys
import time


hostsList = []

class SniffingForServices:


    def __init__(self, networkPrefix):
        self.networkPrefix = networkPrefix

    def nmapPingScan(self):

        nm = nmap.PortScanner()
        pingScanRawResult = nm.scan(hosts=self.networkPrefix, arguments='-v -n -sn')
        #print(pingScanRawResult)
        activeHosts = []
        for result in pingScanRawResult['scan'].values():
            print(result)
            for host in result['status'].values():
                if "":
                    print(result['addresses']['ipv4'])






        # for host in hostList:
        #     print(host)


test1 = SniffingForServices("140.253.178.1-254")
test1.nmapPingScan()






