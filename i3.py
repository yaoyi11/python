# -*- coding: utf-8 -*-
import codecs
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pymysql
from bs4 import BeautifulSoup

def getTitle(url):#获取网页标题
    try:
        html = urlopen(url)
    except (HTTPError,URLError) as e:
        return None
    try:
        bs0bj = BeautifulSoup(html.read())
        title = bs0bj.title.get_text()
    except AttributeError as e:
        return None
    return title

def getLinks(url):  #获取网页里所有的链接地址
    website = urlopen(url)
    html = website.read()
    #use re.findall to get all the links
    r =  re.compile('"((http|ftp)s?://.*?)"')
    html=html.decode('utf-8')#python3
    link = r.findall(html)
    if link==None:
        print("There is no link!")
    else:
        #print(link)
        print("链接准备存入数据库...")
    return link

def nsfile(url):#将爬取到的网页以TXT形式存放到指定目录下
    path = os.path.exists("D:\\testFile\\")#判断文件夹是否存在，如果不存在则创建
    if path:
        print("File Exist!")
    else:
        os.mkdir("D:\\testFile\\")

    urlText = urlopen(url)
    content = urlText.read()
    title = getTitle(url)
    filename = "D:\\testFile\\"+title+".txt"
    fp = codecs.open(filename, "w+", "utf-8")  # 保存在文件夹下
    content = content.decode('utf-8', 'ignore')
    fp.write(content)
    fp.close()
    #生成文件
    print("file"+":"+str(title)+".txt")
    print("ALL Down")
    return filename

def getDocSize(path):# 获取文件大小
    try:
        size = os.path.getsize(path)
        return size
    except Exception as err:
        print(err)

def getmysql(title,size,link):#连接数据库并存储
    n = 0
    conn = pymysql.connect(user='root', passwd=None,
                           host='localhost', db='first', charset='utf8')
    cur = conn.cursor()  # 获取游标
    try:
        for i in link:
            n += 1
            l = i[0]
            cur.execute("INSERT INTO url(id,link) VALUES(%s,%s)", (n,l))  # 插入链接数据
            conn.commit()
        print('数据成功插入！')
        cur.execute("INSERT INTO test (title,size) VALUES(%s,%s)", (title,size))  # 插入标题数据
        conn.commit()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    url = 'http://baike.baidu.com/item/Python'
    file = nsfile(url)
    title = getTitle(url)
    print("网页标题是：" + title)
    size = getDocSize(file)
    size = str(size)
    print("网页大小是：" + size+"b")
    link = getLinks(url)
    getmysql(title, size, link)