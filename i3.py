# -*- coding: utf-8 -*-
import re
import os
import codecs
from bs4 import BeautifulSoup
from urllib.error import HTTPError,URLError
from urllib.request import urlopen
import pymysql

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

def formatSize(bytes):# 字节bytes转化kb\M\G
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)

def getDocSize(path):# 获取文件大小
    try:
        size = os.path.getsize(path)
        return formatSize(size)
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

url = 'http://baike.baidu.com/item/Python'
#url = input("请输入要访问的网址：")
urlText = urlopen(url)
content = urlText.read()
fp = codecs.open("index.txt","w+","gb18030")#保存在文件夹下
#content = content.decode('utf-8')
content = content.decode('utf-8','ignore')
fp.write(content)
fp.close()
size = getDocSize("index.txt")
print("网页大小是："+getDocSize("index.txt"))
title = getTitle(url)
print("网页标题是：" + title)
link = getLinks(url)
getmysql(title,size,link)