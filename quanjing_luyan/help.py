# coding:utf-8
import codecs
import json
import os
import random
import re
from json.decoder import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#请求index页
def get_page_index(page):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'
    }
    data = {
        'companyType': 1,
        #companyType 1 A股公司, 13 B股公司, 3 新三板
        'roadshowDate': 4,
        'roadshowType': 5,
        #roadshowTitle 关键字筛选 格式 '哈哈哈'
        'roadshowTitle': '',
        #start end 日期筛选 格式：'2018/03/18'
        'start': '',
        'end': '',
        'stationId': '',
        'page': page,
        'rows': 9
    }
    url = 'http://rs.p5w.net/roadshow/getRoadshowList.shtml'
    print(url)
    try:
        #请求为post请求
        response = requests.post(url, headers=header, data=data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页错误')
        return None

#获取每个页面下9个公司的pid
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'rows' in data.keys():
            for item in data.get('rows'):
                yield item.get('pid')
    except JSONDecodeError:
        pass

# 请求详情页
def get_page_detail(pid,page_d):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'
    }
    data = {
        'roadshowId': pid,
        'isPagination': 1,
        'type': 2,
        'page': page_d,
        'rows': 10
    }
    url = 'http://rs.p5w.net/roadshowLive/getNInteractionDatas.shtml'
    print(url)
    try:
        response = requests.post(url, headers=header, data=data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页错误')
        return None
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'rows' in data.keys():
            for item in data.get('rows'):
                yield {
                    'pid':item.get('pid'),
                    'title':item.get('roadshowTitle')
                }                
    except JSONDecodeError:
        pass

def parse_page_detail(html):
    try:
        data = json.loads(html)
        if data and 'rows' in data.keys():
            for item in data.get('rows'):
                yield {
                'pid':item.get('pid'),
                'speakName':item.get('speakUserName'),
                'ques':item.get('speakContent'),
                'speaktime':item.get('speakTime'),
                'replyName':item.get('replyList')[0].get('speakUserName'),
                'reply':item.get('replyList')[0].get('speakContent'),
                'replytime':item.get('replyList')[0].get('speakTime')
                }
    except JSONDecodeError:
        pass
#写入文件
def save_to_file(content, filename):
    try:
        f = codecs.open(filename, 'a', encoding='utf-8')
        f.writelines(json.dumps(content, ensure_ascii=False) + '\n')
    except FileNotFoundError as e:
        pass

if __name__ == "__main__":
    for page in range(1, 20):
        html = get_page_index(page)
        for dict in parse_page_index(get_page_index(page)):
            #print(dict.get('title'))
            for page_d in range(0,5):
                content = get_page_detail(dict.get('pid'),page_d)
                title = dict.get('title')
                for item in parse_page_detail(content):
                    print(item)
                    save_to_file(item,title)