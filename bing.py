# -*- coding: utf-8 -*-
import lib.engine.BING as BING
import threading
import queue

    
#关键词队列
keyword_q = queue.Queue()
#爬取URL结果列表
value_url_q = queue.Queue()   #导入的为列表类型

result_url_list =[]
#搜索函数
def SEARCH(grammar,BINGcookie):
    global result_url_list
    while not keyword_q.empty():
        keywords = keyword_q.get()[0]
        index = keyword_q.get()[1]
        BING_result_url_list = BING.search(keyword=keywords,page=index,grammar=grammar,cookies=BINGcookie)  #bing搜索
        result_url_list.extend(list(set(BING_result_url_list)))  #统计结果
        value_url_q.put(result_url_list)
        result_url_list = [] #清空本次记录

#解析函数
def PARSING():
    save_value_file = open('success.txt','a+',encoding='utf-8')
    while True:
        url_list = value_url_q.get()
        # #判断解析队列是否为空
        if url_list ==None:
            break
        if url_list == "END":
            print("程序运行完毕")
            break

        for urls in url_list:
            # print(urls)
            save_value_file.write(urls.strip('\n')+'\n')
    save_value_file.close()

num = 50
page = 300
grammar='';
keyword_list = []  #暂时存储关键词


print("初始化Bing中....")
#存放bing的cookie
BINGcookie = BING.getCookie()
print("Bing初始化完成")

#导入关键词
with open('./1.txt','r',encoding='utf-8') as f:
    for keywords in f.readlines():
        keyword_list.append(keywords.strip('\n').strip(''))

for index in range(1,page+1):
    for keyword in keyword_list:
        keyword_q.put((keyword,index))

#搜索线程
search_th = []
#解析线程
parsing_th = []
for x in range(int(num/2)):
    t = threading.Thread(target=SEARCH,args=(grammar,BINGcookie,),name='SEARCH_THREAD')
    search_th.append(t)
    t.start()

for x in range(int(num/2)):
    t = threading.Thread(target=PARSING,name='PARSING_THREAD')
    parsing_th.append(t)
    t.start()

for x in search_th:
    x.join()
# 等搜索线程终止后，导入解析标志物
for i in range(int(num/2)):
    if i == num - 1:
        value_url_q.put("END")
    value_url_q.put(None)

print('本程序结束')
