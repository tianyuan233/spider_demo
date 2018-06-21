import requests
import sys
import io
import xlwt


from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
urls = ["https://movie.douban.com/top250?start={}&filter=".format(str(i)) 
            for i in range(0, 250, 25)]


def get_movie_info():
    all_movies = []
    rating_num = []
    #inq = []
    for url in urls:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        movies_q = soup.select("span.title")
        #inq_q = soup.select("span.inq")
        rating_num_q = soup.select("span.rating_num")

        movies_w = [movie.get_text() for movie in movies_q]
        #inq_w = [inq.get_text() for inq in inq_q]
        rating_num_w = [rating_num.get_text() for rating_num in rating_num_q]
        
        all_movies = all_movies + movies_w
        #inq = inq + inq_w
        rating_num = rating_num + rating_num_w
    for i in all_movies:
        if '/' in i:
            all_movies.remove(i)
    info = [(all_movies[i], rating_num[i]) for i in range(0, 250)]
    return info


movie_info = get_movie_info()
excel_title = ["ID", "电影名称", "电影评分"]


def write_to_excel_xlwt():
    '''Write content to a new excel'''
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


write_to_excel_xlwt()
