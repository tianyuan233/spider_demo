#-*-coding:utf-8 -*-
import jieba.analyse
import os
from os import path
import jieba
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

d = path.dirname(__file__)

all_words = []
ipath = 'd:\\lizhi'
lyrics= ''

stopwords = [line.strip() for line in open('stop_words.txt').readlines()]
for filename in os.listdir(ipath):
    with open(ipath + '\\' + filename,'rb') as f:
        lyrics += f.read().decode('utf-8')

result = jieba.analyse.textrank(lyrics, topK = 1000, withWeight = True)
keywords = dict()

for i in result:
    if i[0] not in stopwords:#去停用词
        keywords[i[0]] = i[1]
print(keywords)
backgroud_Image = imread(path.join(d, "lizhi.jpg"))
wc = WordCloud(
                background_color = 'white',    # 设置背景颜色
                mask = backgroud_Image,        # 设置背景图片
                max_words = 8000,            # 设置最大显示的字数
                font_path = 'C:/Users/Windows/fonts/msyh.ttf',# 设置字体格式，如不设置显示不了中文
                max_font_size = 80,            # 设置字体最大值
                random_state = 50,            # 设置有多少种随机生成状态，即有多少种配色方案

                )
wc.generate_from_frequencies(keywords)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func = image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()
d = path.dirname(__file__)
wc.to_file(path.join(d, "词云图.png"))
