import requests

with open('C:/Users/LI252/Desktop/ScanResults/02082018_ScanningRawData-dummy.txt', 'r') as f:
    rows = f.read()
    text_lines = rows.split('#################')
    httpHostList = []
    threddsCandidateHostList = []
    hostStatusDict = {}
    noThreddsInstalledHostList = []
    redirectToOtherURL = []
    unknownError = []
    for i, row in enumerate(text_lines):
        if 'http' in str(row):
            hosts = text_lines[i - 1].strip("Host: ")
            httpHostList.append(hosts)

    for httpHost in httpHostList:
        urls = 'http://' + httpHost + '/thredds/catalog.html'

        try:
            r = requests.get(urls, timeout=0.5, allow_redirects=False)
        # print(httpHost, r.status_code)
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
        else:
            if httpHost not in hostStatusDict:
                hostStatusDict[httpHost] = str(r.status_code)
    print(hostStatusDict, "all hosts status Dict is above ###\n\n")

    for host, status in hostStatusDict.items():
        if status == '404':
            noThreddsInstalledHostList.append(host)
            #print("no thredds installed in these hosts\n\n", noThreddsInstalledHostList)
        elif status == '302':
            # redirect to CISCO gateway login page or link has been moved permanently
            redirectToOtherURL.append(host)
            #print("These host redirect to other page or require to login\n\n", redirectToOtherURL)
        elif status == '200':
            threddsCandidateHostList.append(host)
            #print("These host may have thredd installed\n\n", threddsCandidateHostList)
        else:
            unknownError.append(host)

    # for theHost in noThreddsInstalledHostList:

    print("These host redirect to firewall login page\n", redirectToOtherURL)
    print("These host may have thredd installed\n", threddsCandidateHostList, '\n')
    print("no thredds installed in these hosts\n", noThreddsInstalledHostList, '\n')
    print("unknow\n", unknownError)



