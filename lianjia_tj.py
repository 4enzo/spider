# -*- coding: utf-8 -*-
'''
Created on 2019-01-08

@author: Enzo
'''

import random
import time

import requests
import bs4

# 链家官网爬取天津二手房信息


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
}

def get_request(url):
    request = requests.get(url,headers=headers)
    if request.status_code == 200:
        return request
    else:
        return None

def get_total_page(url):
    #目前看官网是固定100页，pg100+会跳转到首页，所以total_page直接写死100???
    # request = get_request(url)
    # soup = bs4.BeautifulSoup(request.text,'html.parser')
    # total_page = soup.find_all('dev',class_='page-box house-lst-page-box') #未实现，未完待续。。。
    # print(total_page)
    total_page = 100
    return total_page

def get_house_url(url):
    #获取page下所有house的title和url
    request = get_request(url)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    house = []
    curr_page_house_count = len(soup.find_all('li',class_="clear LOGCLICKDATA"))
    for i in range(0,curr_page_house_count):
        house_title = soup.find_all('li',class_="clear LOGCLICKDATA")[i].find('div',class_="title").find('a').string
        house_url = soup.find_all('li',class_="clear LOGCLICKDATA")[i].find('div',class_="title").find('a',class_="").get('href')
        house.append('{%s,%s}'%(house_title,house_url))

    return house

if __name__ == '__main__':
    url = "https://tj.lianjia.com/ershoufang/"
    # get_total_page(url)
    a = get_house_url(url)
    for j in a:
        print(j)