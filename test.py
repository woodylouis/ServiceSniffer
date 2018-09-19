from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
import helper
import store
links = ['http://130.116.24.23:80/thredds/catalog/catch_all/catalog.xml',
'http://130.116.24.23:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.96.92:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.96.92:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.96.100:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.96.100:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.96.101:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.96.101:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/imos-srs/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/imos-srs-prep/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/imos-srs-oc-prod/catalog.xml',
'http://138.194.104.48:80/thredds/catalog.oc1dts.xml',
'http://138.194.104.48:80/thredds/catalog.oc1mts.xml',
'http://138.194.104.48:80/thredds/catalog.sstL3Syts.xml',
'http://138.194.104.48:80/thredds/catalog.sstL3Sts.xml',
'http://138.194.104.48:80/thredds/catalog.misctest.xml',
'http://138.194.104.48:80/thredds/catalog.cars2009.xml',
'http://138.194.104.48:80/thredds/catalog/bawap/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/aodaac-test/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/web-maps/catalog.xml',
'http://138.194.104.48:80/thredds/catalog/ereefs-mwq/catalog.xml',
'http://138.194.106.73:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.106.73:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.106.79:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.106.79:80/thredds/catalog/testdata/catalog.xml',
'http://138.194.106.90:80/thredds/catalog/catch_all/catalog.xml',
'http://138.194.106.90:80/thredds/catalog/testdata/catalog.xml',
'http://140.79.3.22:80/thredds/catalog/catch_all/catalog.xml',
'http://140.79.3.22:80/thredds/catalog/testdata/catalog.xml',
'http://140.79.3.31:80/thredds/catalog/catch_all/catalog.xml',
'http://140.79.3.31:80/thredds/catalog/testdata/catalog.xml',
'http://140.79.3.32:80/thredds/catalog/catch_all/catalog.xml',
'http://140.79.3.32:80/thredds/catalog/testdata/catalog.xml',
'http://140.79.3.33:80/thredds/catalog/catch_all/catalog.xml',
'http://140.79.3.33:80/thredds/catalog/testdata/catalog.xml',
'http://152.83.2.92:80/thredds/catalog/catch_all/catalog.xml',
'http://152.83.2.92:80/thredds/catalog/testdata/catalog.xml',
'http://152.83.2.100:80/thredds/catalog/catch_all/catalog.xml',
'http://152.83.2.100:80/thredds/catalog/testdata/catalog.xml',
'http://152.83.2.101:80/thredds/catalog/catch_all/catalog.xml',
'http://152.83.2.101:80/thredds/catalog/testdata/catalog.xml',
'http://152.83.240.36:8080/thredds/catalog/auscover/modis-fc/catalog.xml',
'http://152.83.240.36:8080/thredds/catalog/auscover/modis-gpp/catalog.xml',
'http://152.83.240.36:8080/thredds/auscover/lpdaac-aggregates/catalog.xml',
'http://152.83.240.36:8080/thredds/catalog/auscover/lpdaac-csiro/catalog.xml',
'http://152.83.246.86:80/thredds/catalog/catch_all/catalog.xml',
'http://152.83.246.86:80/thredds/catalog/testdata/catalog.xml',
'http://152.83.247.62:80/thredds/catalog/testAll/catalog.xml',
'http://152.83.247.62:80/thredds/enhancedCatalog.xml',
'http://152.83.247.74:80/thredds/catalog/tasc/fcst/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/external/whit/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/external/mb/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/compas/setas/hydro/nrt/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/compas/arena/v3/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/setas/hydro/nrt/catalog.xml',
'http://152.83.247.74:80/thredds/catalog/storm/hydro/nrt/catalog.xml',
'http://150.229.2.77:8080/thredds/catalog/data/dynamic/catalog.xml',
'http://150.229.2.77:8080/thredds/catalog/data/nrm_ts/catalog.xml',
'http://150.229.2.77:8080/thredds/aggregation/timeseries_model_aggregation.xml',
'http://150.229.2.77:8080/thredds/catalog/data/thresholds/catalog.xml',
'http://150.229.2.77:8080/thredds/catalog/data/authoritative/CMIP5/catalog.xml',
'http://150.229.2.77:8080/thredds/catalog/data/authoritative/OBS/catalog.xml',
'http://150.229.2.77:8080/thredds/aggregation/scaled_seasonal_timeseries.xml',
'http://150.229.2.77:8080/thredds/aggregation/scaled_monthly_merged.xml',
'http://150.229.21.36:80/thredds/catalog/tasc/fcst/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/external/whit/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/external/mb/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/compas/setas/hydro/nrt/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/compas/arena/v3/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/setas/hydro/nrt/catalog.xml',
'http://150.229.21.36:80/thredds/catalog/storm/hydro/nrt/catalog.xml',
'http://150.229.194.19:80/thredds/catalog/dem/catalog.xml']

ls = []
urls = []
temp = []

def getLinks(links):
    database = "C:\\Users\LI252\PycharmProjects\servicesniffer\database\database.sqlite"
    conn = store.create_connection(database)
    subURLs = []
    subCatalogRefHrefList = []
    with conn:
        for link in links:
            postfix = 'catalog.xml'
            host = urlsplit(link, allow_fragments=True)
            #print(host)
            hostIP = host.netloc
            if postfix in link:
                urlPrefix = link.strip(postfix)
                #print(urlPrefix)
            else:
                urlPrefix = f"http://{hostIP}"


            r = requests.get(link, timeout=0.5, allow_redirects=False)
            soup = BeautifulSoup(r.text, features="lxml")
            catalog = soup.find('catalog')
            #print(catalog)
            for catalogRef in catalog.find_all('catalogref'):
                # print(catalogRef)
                catalogRefHref = catalogRef['xlink:href']
                # print(catalogRefHref)
                # ls.append(catalogRefHref)
                # print(urlPrefix, catalogRefHref)
                completeURL = urlPrefix + catalogRefHref
                subURLs.append(completeURL)

        for subURL in subURLs:
            host = urlsplit(subURL, allow_fragments=True)
            hostIpWithPort = host.netloc
            hostIp = host.hostname
            hostId = store.select_host_id_by_host_ip(conn, hostIp)
            try:
                r = requests.get(subURL, timeout=0.5, allow_redirects=False)
                soup = BeautifulSoup(r.text, features="lxml")
                # print(r.url, r.status_code)
                subCatalog = soup.find('catalog')
                for subCatalogRef in subCatalog.find_all('catalogref'):
                    subCatalogRefHref = subCatalogRef['xlink:href']
                    ### We can get a larget list of sub URL here
                    subCatalogRefHrefList.append(subCatalogRefHref)

                for dataset in subCatalog.find_all('dataset'):
                    if '.nc' in dataset['name']:
                        datasetName = dataset['name']
                        description = dataset['id']
                        ncUrlPath = dataset['urlpath']
                        for services in subCatalog.find_all('service'):
                            for service in services.find_all('service'):
                                serviceName = service['name']
                                # print(serviceName)
                                serviceType = service['serviceType'.lower()]
                                base = service['base']
                                # print(base)
                                completeURL = f"http://{hostIpWithPort}{base}{ncUrlPath}"
                                serviceId = helper.compare(conn, serviceName)

                        datasetRecord = (datasetName, description, completeURL, serviceId, hostId)
                    # print(datasetRecord)

                        existing = store.select_nc_name_and_description_and_url_path_and_service_id_and_host_id(conn, datasetRecord)
                        if datasetRecord != existing:
                            # print(ncRecord)
                            store.create_nc_files_record(conn, datasetRecord)
            except AttributeError:
                pass

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







setOfLink = getLinks(links)


# if "/thredds/" in catalogRefUrl:
#     completeURL = f"http://{hostIpWithPort}{catalogRefUrl}"
#     listOfLinksInHomePage.append(completeURL)
#     # print(listOfLinksInHomePage)
# else:
#     completeURL = f"http://{hostIpWithPort}/thredds/{catalogRefUrl}"
#     listOfLinksInHomePage.append(completeURL)