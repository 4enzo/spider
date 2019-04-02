# -*- coding: utf-8 -*-
'''
Created on 2019-01-08

@author: Enzo
'''

import random
import time

import requests
import bs4
import pymongo

# 链家官网爬取天津二手房信息


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
}

def get_request(url):
    request = requests.get(url,headers=headers)
    if request.status_code == 200:
        return request
    else:
        print(url + "error:"+request.status_code)
        return None

def get_total_page():
    #目前看官网是固定100页，pg100+会跳转到首页，所以total_page直接写死100???
    # request = get_request(url)
    # soup = bs4.BeautifulSoup(request.text,'html.parser')
    # total_page = soup.find_all('dev',class_='page-box house-lst-page-box') #未实现，未完待续。。。
    # print(total_page)
    total_page = 100
    return total_page

def get_pages_url():
    #生成所有page的URL：https://tj.lianjia.com/ershoufang/pg2/
    pages_url = []

    for i in range(1,int(get_total_page())+1):
        page_url = 'https://tj.lianjia.com/ershoufang/pg'+str(i)
        pages_url.append(page_url)

    return pages_url


def get_house_url(url_list):
    #获取page下所有house的title和url
    #只获取url  2019-04-01
    house_url_list = []
    for url in url_list:
        request = get_request(url)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        # house = []
        curr_page_house_count = len(soup.find_all('li',class_="clear LOGCLICKDATA"))
        for i in range(0,curr_page_house_count):
            house_title = soup.find_all('li',class_="clear LOGCLICKDATA")[i].find('div',class_="title").find('a').string
            house_url = soup.find_all('li',class_="clear LOGCLICKDATA")[i].find('div',class_="title").find('a',class_="").get('href')
            # house.append('{%s,%s}'%(house_title,house_url))
            get_house_info(house_url)
            # house_url_list.append(house_url)

    # return house_url_list

def get_house_info(url):
    house_info = {}
    request = get_request(url)
    soup = bs4.BeautifulSoup(request.text,'html.parser')
    basic = soup.find('div',class_='newwrap baseinform').find_all('li')
    #获取全部信息，方便后期分析
    house_info['房屋户型'] = basic[0].text[4:]
    house_info['所在楼层'] = basic[1].text[4:]
    house_info['建筑面积'] = basic[2].text[4:]
    house_info['户型结构'] = basic[3].text[4:]
    house_info['套内面积'] = basic[4].text[4:]
    house_info['建筑类型'] = basic[5].text[4:]
    house_info['房屋朝向'] = basic[6].text[4:]
    house_info['建筑结构'] = basic[7].text[4:]
    house_info['装修情况'] = basic[8].text[4:]
    house_info['梯户比例'] = basic[9].text[4:]
    house_info['供暖方式'] = basic[10].text[4:]
    house_info['配备电梯'] = basic[11].text[4:]
    house_info['产权年限'] = basic[12].text[4:]
    house_info['挂牌时间'] = basic[13].find_all('span')[1].text
    house_info['交易权属'] = basic[14].find_all('span')[1].text
    house_info['上次交易'] = basic[15].find_all('span')[1].text
    house_info['房屋用途'] = basic[16].find_all('span')[1].text
    house_info['房屋年限'] = basic[17].find_all('span')[1].text
    house_info['产权所属'] = basic[18].find_all('span')[1].text
    house_info['抵押信息'] = basic[19].find_all('span')[1].text.strip()
    house_info['房本备件'] = basic[20].find_all('span')[1].text
    with open('./lianjia_tj.txt','a') as f:
        f.write(str(house_info)+'\n')
    write2db(house_info)


def write2db(info):
    #写入mongodb数据库
    conn = pymongo.MongoClient('192.168.199.170', 27017)
    db = conn.spider
    my_collection = db.lianjia_tj
    my_collection.insert(info)


def main():
    page_url = get_pages_url()
    get_house_url(page_url)
    # for url in house_url_list:
    #     time.sleep(random.randint(1,10))
    #     get_house_info(url)


if __name__ == '__main__':
    main()