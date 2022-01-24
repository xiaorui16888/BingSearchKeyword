# -*- coding: utf-8 -*-
OpenFile = input("请输入要去重的文件名:")
SaveFile = input("请输入保存的文件名:")

of = open(OpenFile,'r',encoding='utf-8')

url = set()
for _ in of.readlines():
    url.add(_.strip('/n'))


print('导入完成')
url = list(url)

sf = open(SaveFile,'a+',encoding='utf-8')

for u in url:
    sf.write(u)

sf.close()