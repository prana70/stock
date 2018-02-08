#coding:utf8

import requests as rq
from bs4 import BeautifulSoup as bs

url='http://quote.eastmoney.com/stocklist.html'
hd={'User-Agent':'Mozilla/5.0'}

resp=rq.get(url,headers=hd)
resp.encoding='gb2312'
soup=bs(resp.text,'html.parser')
lists=soup.find_all('a')
f=open('stocks.txt','w')
#i=0
for list in lists:
    if list.string!=None:
        if '(60' in list.string or '(30' in list.string or '(00' in list.string:
            try:
                f.write(list.string.replace(r'昇','升')+'\n')
                print(list.string.replace(r'昇','升'))
            except:
                f.write('写入错误!\n')
                print('写入错误！')
#            i+=1
#    if i==10:
#        break

f.close()
