# -*- coding: utf-8 -*-
import requests
from lib.settings import UA,TIMEOUT
from random import choice
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   #屏蔽验证证书的警告

temp_UA = choice(UA) #获取UA
#获取url正则
URL_PATTERN = re.compile('''<li.*?class="b_algo".*?>.*?<a.*?href="(.*?)".*?>''')

# #判断有无搜索结果正则
# NO_VALUE_PATTERN =re.compile('''''')
proxies = {
    'http:':None,
    'https:':None
}
#获取cookie
def getCookie():
    cookies = ''
    url = 'https://www.bing.com'
    headers = {
        'user-agent':temp_UA,   #该正则暂时只匹配此类ua头
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate,br',
    }
    try:
        response = requests.get(url,headers=headers,proxies=proxies,timeout=TIMEOUT,verify=False)
        if response.status_code == 200:
            res_cookie = response.cookies
            for keys in res_cookie.keys():
                key = keys
                value = res_cookie[keys]
                cookies += key+'='+value+';'
    except requests.exceptions.ProxyError as e:
        print('代理连接错误:',e)
    return cookies

def search(keyword='',page=1,grammar='loc:tw',cookies=''):
    url = 'https://www.bing.com/search?q='+keyword.replace(' ','%20')+'%20'+grammar.replace(' ','%20')+'&first='+str(page*10)
    headers = {
        'user-agent':temp_UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate,br',
        'cookie':cookies
    }
    try:
        print("正在搜素:%s  第%d页" % (keyword,page))
        response = requests.get(url,headers=headers,proxies=proxies,timeout=TIMEOUT,verify=False)
        text = response.text
        url_list = re.findall(URL_PATTERN, text)
        url_list = list(set(url_list))  # 最终结果去重
        return url_list
    except requests.exceptions.ProxyError as e:
        print('代理连接错误:',e)


