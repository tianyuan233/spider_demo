import os
from _md5 import md5

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
def get_page_detail(pg):
    url = 'https://tieba.baidu.com/p/5718316075?pn=' + str(pg)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    try:
        print(url)
        response = requests.get(url, headers=header)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        # return None
    except RequestException:
        print('请求详情页错误')
        return None

def pagse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())
    image = soup.select('.BDE_Image')
    for i in image:
        print(i.get('src'))
        download_image(i.get('src'))

def download_image(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        # print('请求详情页错误')
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format('E:\\touxiang', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

for j in range(7):
    pagse_page_detail(get_page_detail(j))