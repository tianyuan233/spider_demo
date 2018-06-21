import re
import json
import requests
from requests import RequestException
from multiprocessing import Pool
def get_onePage(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_onePage(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?">(.*?)</i>.*?title="(.*?)".*?data-src="(.*?)".*?alt="(.*?)".*?star">(.*?)</p>'
        + '.*?releasetime">(.*?)</p>'
        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'name': item[1],
            'image': item[2],
            'actor': item[4].strip()[3:],
            'time': item[5][5:],
            'score': item[6] + item[7]
        }


def write_to_file(content):
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_onePage(url)
    for item in parse_onePage(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
