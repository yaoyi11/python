# python
## 小目标：单个网页静态分析

### 功能

- 对目标网站的一个特定页面进行采集。
- 静态分析，保存分析结果
  - 获取网页的大小
  - 获取网页的标题或特定内容
  - 获取网页里所有的链接地址
- 把采集的结果和分析结果保存在mysql。

### 配置项

- 目标url:'http://baike.baidu.com/item/Python

### 环境及软件

- Windows7 64位+python3.6+pycharm-community-2017.1.5+wampserver

### 结果显示

- file:Python_百度百科.txt
- ALL Down
- 网页标题是：Python_百度百科
- 网页大小是：169262b
- 链接准备存入数据库...
- 数据成功插入！

### 主要函数

- ```python
  def getTitle(url):#获取网页标题
  ```


- ```python
  def getLinks(url):  #获取网页里所有的链接地址
  ```


- ```python
  def nsfile(url):#将爬取到的网页以TXT形式存放到指定目录下
  ```


- ```python
  def getDocSize(path):# 获取文件大小
  ```


- ```python
  def getmysql(title,size,link):#连接数据库并存储
  ```


- ```python
  if __name__ == '__main__':#主函数
  ```



