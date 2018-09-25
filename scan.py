##########################################################################################
#######It is needed to be careful to run this program. It is involved NMAP package.#######
##################Running this might arise attention from IM&T############################

import nmap
import datetime
import requests

##########################################################################################
#########A raw data for scanning will be generated once the scanning has started##########
###########The report will be keep updating until scanning process has stopped############
##########################################################################################
date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")



def get_thredds_hosts(network_prefix):
    reportName = str(date) + "_ScanReport" + ".txt"
    scanReport = open(reportName, "a")
    nm = nmap.PortScanner()
    activeHosts = []
    portDict = {}
    hostInfoDict = {}
    """
    Perform simple ping and create a list of online hosts
    The parameters below might be aggressive.
    However, this is acceptable scanning speed and accuracy for bunch of /16 network after perform few tests.
    The parameters below might be aggressive can be modified.
    """
    pingResult = nm.scan(hosts=network_prefix,
                         arguments='--min-hostgroup=5000 --max-hostgroup=10000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T4 -n -sP')

    """
    Get active hosts only from raw scanning report
    """
    for pResult in pingResult['scan'].values():
        hostStatus = pResult['status']['state']
        host = pResult['addresses']['ipv4']
        if hostStatus == 'up':
            activeHosts.append(host)
    totalActiveHosts = ("There are " + str(len(activeHosts)) + " active hosts online. The hosts are: \n" + '\n'.join(
        '{}: {}'.format(*k) for k in enumerate(activeHosts, start=1)) + "\n")


    """
    Get the hosts with open ports and is HTTP protocol from active hosts above
    # 1-1024 popular port
    # 1194 openVPN
    # 1433 Microsoft SQL Server
    # 1434 Microsoft SQL Monitor
    # 2483-2484 Oracle database
    # 3306 MySQL database service
    # 4333 mSQL
    # 5432 PostgreSQL database
    # 8080 HTTP Proxy such as Apache
    # 27017 Mongo database
    """

    for host in activeHosts:
        aDict = nm.scan(hosts=host,
                        arguments='--min-hostgroup=5000 --max-hostgroup=10000 --min-parallelism=100 --max-parallelism=200 --host-timeout=2s -T5 -n -v',
                        ports="80, 1433-1434, 2483-2484, 800, 3306, 4333, 5432, 5000, 8080, 9000, 8433, 27017, 50000")
        scanReport.write(str(aDict))

        for serviceScan in aDict['scan'].values():
            host = serviceScan['addresses']['ipv4']
            try:
                portInfo = serviceScan['tcp']
            except:
                pass
            for port, info in portInfo.items():
                hostServices = info['name']
                portState = info['state']
                """
                Get all hosts' HTTP service and port in a dictionary
                """
                if portState == 'open' and 'http' in hostServices:
                    if port not in portDict:
                        portDict[port] = hostServices
                    if host not in hostInfoDict:
                        hostInfoDict[host] = portDict
    # print(hostInfoDict)
    """
    In here, it will create a host status dictionary for all host using HTTP protocol.
    Constructing URLs with host IP, ports, main thredds catalog path.
    After that, it will generate a potential dictionary for potential TDS candidate by using REQUEST.
    If the status is '404', these hosts will be ignore. 
    If the status is '302', it means the page redirect to login page. These host may have TDS installed and are store in database
    If the status is '200', it means these hosts are TDS servers and can be access.
    """
    httpHostStatusDict = {}
    hostInfoDict = {'152.83.247.62': {80: 'http', 8080: 'http-proxy'}, '152.83.247.74': {80: 'http', 8080: 'http-proxy'}}
    for host, hostInfo in hostInfoDict.items():
        for port in hostInfo.keys():
            urls = f'http://{host}:{port}/thredds/catalog.html'
            try:
                r = requests.get(urls, timeout=0.5, allow_redirects=False)
                if str(r.url) not in httpHostStatusDict:
                    httpHostStatusDict[str(r.url)] = str(r.status_code)
            except requests.exceptions.HTTPError:
                """An HTTP error occurred."""
                pass
            except requests.exceptions.ConnectionError:
                """A Connection error occurred."""
                pass
            except requests.exceptions.Timeout:
                """
                The request timed out while trying to connect to the remote server.
                Requests that produced this error are safe to retry.
                """
                pass
            except requests.exceptions.RequestException:
                """
                There was an ambiguous exception that occurred while handling your request.
                """
                pass
    # print(httpHostStatusDict)
    threddsCandidateHostList = []
    noThreddsInstalledHostList = []
    redirectToOtherURL = []
    unknownError = []
    for urls, status in httpHostStatusDict.items():
        if status == '404':
            noThreddsInstalledHostList.append(urls)
        elif status == '302':
            redirectToOtherURL.append(urls)
        elif status == '200':
            threddsCandidateHostList.append(urls)
        else:
            unknownError.append(urls)

    return threddsCandidateHostList
    # print(threddsCandidateHostList)

