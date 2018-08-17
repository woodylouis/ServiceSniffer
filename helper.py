import requests


def getValidReturn(httpHostList):

    hostStatusDict = {}
    noThreddsInstalledHostList = []
    redirectToOtherURLsList = []
    threddsCandidateHostList = []
    otherErrorHostList = []

    for httpHost in httpHostList:

        try:
            r = requests.get(httpHost, timeout=0.5, allow_redirects=False)
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
    #print("###There are", len(hostStatusDict), "host\n", hostStatusDict, "all hosts status Dict is above ###\n\n")

    for host, status in hostStatusDict.items():
        if status == '404':
            noThreddsInstalledHostList.append(host)
            #print("no thredds installed in these hosts\n\n", noThreddsInstalledHostList)
        elif status == '302':
            # redirect to CISCO gateway login page or link has been moved permanently
            redirectToOtherURLsList.append(host)
            #print("These host redirect to other page or require to login\n\n", redirectToOtherURL)
        elif status == '200':
            threddsCandidateHostList.append(host)
            #print("These host may have thredd installed\n\n", threddsCandidateHostList)
        else:
            otherErrorHostList.append(host)

#getValidReturn(list)