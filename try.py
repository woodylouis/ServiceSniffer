from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import urllib
import requests
import urllib.request
from urllib.parse import urlsplit
import tds_host

# base_url = "http://152.83.2.100/thredds/catalog/catch_all/testdata/nc/catalog.html"
# his = ["/thredds/dodsC/"]
#
# for i in range(20):
#     url = base_url
#     html = urlopen(url).read().decode('utf-8')
#     print(html)
#     soup = BeautifulSoup(html, features='lxml')
#     print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls

    # sub_urls = soup.find_all("a", {"href": re.compile('(https?://[^\s)";]+\.(\w|/)*)')})
    # print(sub_urls)

    # if len(sub_urls) != 0:
    #     his.append(random.sample(sub_urls, 1)[0]['href'])
    # else:
    #     # no valid sub link found
    #     his.pop()
# # #
# def getlink(url):
#     # 模拟成浏览器
#     headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36")
#     opener = urllib.request.build_opener()
#     opener.addheaders = [headers]
#
#     # 将opener安装为全局
#     urllib.request.install_opener(opener)
#     file = urllib.request.urlopen(url)
#     data = str(file.read())
#
#     r = requests.get(url, timeout=0.5, allow_redirects=False)
#     soup = BeautifulSoup(r.text, features="lxml")
#     catalog = soup.find_all('a')
#     print(catalog)
#
#
#     # 根据需求构建好链接表达式
#     pat = '(/[thredds][^\s)";]+\.(\w|/)*[.nc])'
#     link = re.compile(pat).findall(data)
#
#     # 去除重复元素
#     link = list(set(link))
#     return link
#
# # 要爬取的网页链接
# url = 'http://152.83.2.100/thredds/catalog.xml'
# # 获取对应网页中包含的链接地址
# linklist = getlink(url)
# # 通过for循环分别遍历输出获取的链接地址到屏幕上
# suburls = []
# for link in linklist:
#     print(link[0])
#     suburls.append(link[0])

def getlink(urls):

    for url in urls:


        r = requests.get(url, timeout=0.5, allow_redirects=False)
        soup = BeautifulSoup(r.text, features="lxml")

        catalog = soup.find('catalog')

        try:
            try:
                for catalogRef in catalog.find_all('catalogref'):
                    print(url, catalogRef['xlink:href'])

            except:
                for dataset in catalog.find_all('dataset'):
                    for catalogRef in dataset.find_all('catalogref'):
                        print(url, catalogRef)
        except:
            print("something wrong")



if __name__ == '__main__':
    host = tds_host.getCandiateUrl()
    test = getlink(host)
