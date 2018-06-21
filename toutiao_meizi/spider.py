import json
import os
import re
from hashlib import md5
from json.decoder import JSONDecodeError
from urllib.parse import urlencode

import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'asdf': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页错误')
        return None


def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'}
    proxies = {"http": "http://118.114.77.47:8080", "https": "http://50.233.137.36:80", }
    try:
        response = requests.get(url, headers=header, proxies=proxies)
        if response.status_code == 200:
            return response.text
            print(response.text)
        print('not 200000')
        return None

    except RequestException:
        # print('请求详情页错误')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())
    title = soup.select('title')[0].get_text()
    image_pattern = re.compile(';&quot;http://(.*?)&quot;', re.S)
    images = re.findall(image_pattern, html)
    for image in images:
        imgurl = 'http://' + image
        print('正在下载', imgurl)
        download_image(imgurl)
    if images:
        return {
            'title': title,
            'url': url,
            'images': ['http://' + image for image in images]
        }


def save_to_mongo(data):
    if db[MONGO_TABLE].insert(data):
        # print('存储成功', data)
        return True
    return False


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
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        print(url)
        html = get_page_detail(url)
        if html:
            data = parse_page_detail(html, url)
            if data:
                print('正在保存到mongodb')
                save_to_mongo(data)


if __name__ == '__main__':
    #
    # groups = [x*20 for x in range(START,END + 1)]
    # pool = Pool()
    # pool.map(main, groups)
    main(20)
