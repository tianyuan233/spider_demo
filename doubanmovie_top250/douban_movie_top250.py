import re
import json
import requests
from requests import RequestException
from multiprocessing import Pool
def get_onePage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_onePage(html):
    pattern = re.compile(
        '<li.*?pic">.*?<em\sclass="">(.*?)</em>.*?<img.*?src="(.*?)".*?"hd.*?href="(.*?)".*?title">(.*?)</span>.*?star">.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>',
        re.S)

    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'detail':item[2],
            'name':item[3],
            'score':item[4],
            'comment':item[5].strip()
        }
def write_to_file(content):
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(num):
    url = 'https://movie.douban.com/top250?start={0}&filter='.format(num)
    html = get_onePage(url)
    for item in parse_onePage(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*25 for i in range(10)])
