import requests
with open('C:/Users/LI252/Desktop/ScanResults/02082018_ScanningRawData.txt', 'r') as f:
    rows = f.read()
    text_lines = rows.split('#################')
    httpHostList = []
    for i, row in enumerate(text_lines):
        if 'http' in str(row):
            hosts = text_lines[i - 1].strip("Host: ")
            httpHostList.append(hosts)
    for httpHost in httpHostList:
        urls = 'http://' + httpHost + '/thredds/catalog.html'
        try:
            r = requests.get(urls, timeout=1)
            r.raise_for_status()
            print("Http Connected", httpHost, r)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Connection Error for ", httpHost)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)







