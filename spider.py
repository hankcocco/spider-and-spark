#coding=utf-8

from bs4 import BeautifulSoup
import re
import requests
import time
import csv
import codecs
#处理python编码格式
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#------------------------

class moveItem(object):
    def __init__(self):
        self.name = ""
        self.star = ""
        self.comment = []
        self.url = ""
        self.id = ""
    pass

moveList = []
def getMovies(pageUrl):
    global moveList
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    if(pageUrl == ""):
        res = session.get("https://movie.douban.com/top250", headers=headers)
    else:
        res = session.get(pageUrl, headers=headers)
    bsObj = BeautifulSoup(res.text, "html.parser")
    for item in bsObj.findAll(class_="item"):
        temp = moveItem()
        temp.name = item.find(class_="title").get_text()
        temp.star = item.find(class_="rating_num").get_text()
        temp.url = item.find("a")["href"]
        pattern = re.compile(r'.*/([0-9]+)/')
        temp.id = pattern.findall(temp.url)[0]
        moveList.append(temp)
def getComment(id):
    global moveList
    comment = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    res = session.get("https://movie.douban.com/subject/"+str(id)+"/comments?status=P",headers=headers)
    bsObj = BeautifulSoup(res.text, "html.parser")
    for item in bsObj.findAll(class_="comment"):
        comment.append(item.p.get_text())
    return comment

getMovies("")
for i in range(1, 10):
    getMovies("https://movie.douban.com/top250"+"?start="+str(25*i)+"&filter=")


for i in moveList:
    time.sleep(3)
    i.comment = getComment(i.id)

csvFile = open("./movieItem.csv", "wt")
#处理csv写入时的编码格式
csvFile.write(codecs.BOM_UTF8)
writer = csv.writer(csvFile)
writer.writerow(("name", "id", "star", "url", "comment"))
for i in moveList:
    Tolcomment = ""
    for k in i.comment:
        Tolcomment += k
    writer.writerow((i.name, i.id, i.star, i.url, Tolcomment))

csvFile.close()






