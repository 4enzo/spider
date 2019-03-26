# -*- coding: UTF-8 -*-
'''
Created on 2016-08-24

@author: Enzo
'''

#请在Shadowsocks.exe同目录下执行

import urllib2
import urllib
import re
import os
import time

def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def get_account(html):
    reg = '<div class="col-sm-4 text-center".*?服务器地址:(.*?)</h4.*?端口:(.*?)</h4.*?密码:(.*?)</h4.*?加密方式:(.*?)</h4.*?'
    compile = re.compile(reg,re.S)
    items = re.findall(compile,html)
    return items

def update_config(list):
    path = os.getcwd()
    file = '%s\gui-config.json'%path
    f = open(file,'wt')
    newdata = '''{
"configs" : [
  {
"server" : "%s",
"server_port" : %s,
"password" : "%s",
"method" : "%s",
"remarks" : ""}
,
  {
"server" : "%s",
"server_port" : %s,
"password" : "%s",
"method" : "%s",
"remarks" : ""}
,
  {
"server" : "%s",
"server_port" : %s,
"password" : "%s",
"method" : "%s",
"remarks" : ""}

],
"strategy" : "com.shadowsocks.strategy.ha",
"index" : -1,
"global" : false,
"enabled" : true,
"shareOverLan" : false,
"isDefault" : false,
"localPort" : 1080,
"pacUrl" : null,
"useOnlinePac" : false,
"availabilityStatistics" : false}
'''%(list[0][0],list[0][1],list[0][2],list[0][3],list[1][0],list[1][1],list[1][2],list[1][3],list[2][0],list[2][1],list[2][2],list[2][3],)
    try:
        f.write(newdata)
    finally:
        f.close()
#         accountConfig = '''{\n"server" : "%s",\n"server_port" :%s,\n"password" : "%s",\n"method" : "%s",\n"remarks" : ""}\n'''%(list[i][0],list[i][1],list[i][2],list[i][3])


try:
    url = 'http://www.ishadowsocks.org/'
    html = get_html(url)
    result = get_account(html)
    update_config(result)
    print "config file 'gui-config.json' update success !"
except Exception,e:
    print 'error!',e
time.sleep(5)