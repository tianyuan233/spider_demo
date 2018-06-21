# -*- coding:utf-8 -*-
import codecs
import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import re
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def get_ids_by_singer_id(singer_ID):
    url = 'http://music.163.com/artist?id=' + str(singer_ID)
    r = requests.get(url).text
    tree = html.fromstring(r)
    data_json = tree.xpath('//textarea[@style="display:none;"]')[0].text
    jsob = json.loads(data_json)
    return jsob

songs = get_ids_by_singer_id(3681)

def getSongLyric(songID):
    url = 'http://music.163.com/api/song/lyric?os=pc&id='+str(songID)+'&lv=-1&kv=-1&tv=-1'
    r = requests.post(url)
    data = r.text
    songLyric = json.loads(data)
    return songLyric

def save_to_file(content, filename):
    try:
        f = codecs.open(filename, 'w', encoding='utf-8')
        f.writelines(content)
    except FileNotFoundError as e:
        pass

for song in songs:
    name = song["name"]
    id = song["id"]
    try:
        songLyric = getSongLyric(id)
        lyric = songLyric["lrc"]["lyric"]
        lrc = re.sub(r"\[(.*)\]", '', lyric)
        filename = name
        save_to_file(lrc, "D:\\lizhi\\" + filename + ".txt")
    except KeyError as e:
        pass
