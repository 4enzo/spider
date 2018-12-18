# -*- coding: utf-8 -*-
'''
Created on 2018-11-27

@author: Enzo
'''


import requests
import bs4
import logging
import time

'''
爬取one:http://wufazhuce.com/
'''

def spider_one(num):
    logging.basicConfig(level=logging.ERROR,
                        filename='./one.log',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    url = "http://wufazhuce.com/one/"
    start_time = time.time()
    for i in range(1,num+1):
        try:
            full_url = url+str(i)
            page = requests.get(full_url).content
            soup = bs4.BeautifulSoup(page,'html.parser')
            # print(soup)
            title = soup.find('div',class_="one-titulo").text.strip()
            # print(title)
            content = soup.find('div',class_="one-cita").text.strip()

            with open('one.txt','a',encoding='utf-8') as f:
                f.write(title +'\n'+ content +'\n')
            print('Success %s'%full_url)
            # time.sleep(5)

        except Exception as e:
            print('Failed:%s'%full_url)
            logging.error('Error:%s'%(full_url))
            logging.error(e)
            continue
    end_time = time.time()
    print('time spend %ss'%(end_time-start_time))

if __name__ == '__main__':
    spider_one(2294)