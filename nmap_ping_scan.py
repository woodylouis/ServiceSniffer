import nmap
import sys
import socket


def nmap_ping_scan(network_prefix):
    nm = nmap.PortScanner()
    pingScanRawResult = nm.scan(hosts=network_prefix, arguments='-v -n -sn')
    hostList = []
    print(pingScanRawResult)
    for Result in pingScanRawResult['scan'].values():
        if Result['status']['state'] == 'up':
            hostList.append(Result['addresses']['ipv4'])
    return hostList

if __name__ == '__main__':
    import time
    t1 = time.time()
    for host in nmap_ping_scan(sys.argv[1]):
        print( '%-20s %5s' % (host, 'is up'))

    t2 = time.time()
    print("Used" + str(t2 - t1) + " seconds")