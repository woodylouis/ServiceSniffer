import nmap
import sys
import time
from nmap_ping_scan import nmap_ping_scan
from nmap_A_scan import nmap_A_scan



def nmap_ping_A_scan(network_prefix):
    hosts = nmap_ping_scan(network_prefix)
    for host in hosts:
        nmap_A_scan(host)
        print(host)



if __name__ == '__main__':
    nmap_ping_A_scan(sys.argv[1])
