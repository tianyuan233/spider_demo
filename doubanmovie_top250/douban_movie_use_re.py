import requests
import re
import xlwt
path='D:/PyPro/'

movie_info = []
urls = ["https://movie.douban.com/top250?start={}&filter=".format(str(i))
            for i in range(0, 250, 25)]

pattern = re.compile('<li.*?pic">.*?<img.*?src="(.*?)".*?"hd.*?href="(.*?)".*?title">(.*?)</span>.*?star">.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>',re.S)

for url in urls:
    data = requests.get('https://movie.douban.com/top250').text
    info = re.findall(pattern,data)
    for i in info:
        movie_info.append(i)

print(movie_info[0])
excel_title = ["ID", "图片url", "详情url", "电影名称", "电影评分", "一句话总结"]

new_workbook = xlwt.Workbook()
new_sheet = new_workbook.add_sheet("sheet-1")
for i in range(0, len(excel_title)):
    new_sheet.write(0, i, excel_title[i])
for i in range(0, 250):
    new_sheet.write(i + 1, 0, i + 1)
for i in range(1, len(movie_info) + 1):
    for j in range(1, len(movie_info[0]) + 1):
        new_sheet.write(i, j, movie_info[i - 1][j - 1])
new_workbook.save("doubantop250.xls")
