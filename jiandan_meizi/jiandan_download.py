from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

path='D:/jd_image/'
urls = ["http://jandan.net/ooxx/page-{}#comments".format(str(i)) for i in range(1, 50)]
img_url=[]
driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

for url in urls:
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    images = soup.select("a.view_img_link")

    for i in images:               
         z=i.get('href')
         if str('gif') in str(z):
            pass
         else:
         	http_url = "http:" + z
         	img_url.append(http_url)
            #print("http:%s" % z)

    for j in img_url:
        r=requests.get(j)
        print('正在下载 %s......' % j)
        with open(path+j[-15:],'wb')as jpg:
            jpg.write(r.content)
