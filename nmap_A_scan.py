import nmap
import sys
import time

# fileName = time.strftime("%Y%m%d-%H%M%S")
# f = open(fileName + ".txt", 'w')
def nmap_A_scan(network_prefix):
    nm = nmap.PortScanner()
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A')

    for host, result in scan_raw_result['scan'].items():

        if result['status']['state'] == 'up':
            print('#' * 17 + 'Host: ' + host + '#' * 17)


            print('-' * 20 + 'OS' + '-' * 20)

            for os in result['osmatch']:
                print('Operating System is: ' + os['name'] + ' Accuracy is: ' + os['accuracy'])
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
                            print('name: ' + result['tcp'][port]['name'])
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
                            print('CPE: ' + result['tcp'][port]['cpe'])
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
                        print('UDP Port:' + str(port))
                        try:
                            print('Status: ' + result['udp'][port]['state'])
                        except:
                            pass
                        try:
                            print('reason:' + result['udp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('Additional Info' + result['udp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('name: ' + result['udp'][port]['name'])
                        except:
                            pass
                        try:
                            print('version: ' + result['udp']['version'])
                        except:
                            pass
                        try:
                            print('product: ' + result['udp'][port]['product'])
                        except:
                            pass
                        try:
                            print('CPE: ' + result['udp'][port]['cpe'])
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


if __name__ == '__main__':
    nmap_A_scan(sys.argv[1])




