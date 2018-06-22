import requests as rq
import os
import math
import InstitutionalPerspective as ip
import json

url='https://xueqiu.com/stock/cata/stocklist.json?page=1&size=90&order=desc&orderby=percent&type=30&isdelay=1&_=1529201880625'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
CookiesUrl='https://xueqiu.com/'
_cookies=ip.GetCookies(CookiesUrl)
f=open(os.getcwd()+'\\market_data\\HkStockList.csv','w',encoding='utf8')
f.write('股票代码,股票名称\n')

resp=rq.get(url,headers=headers,cookies=_cookies)
dict=json.loads(resp.text)
pages=math.ceil(dict['count']['count']/90)
print(pages)
for row in dict['stocks']:
    print(row['symbol'],row['name'])
    f.write(row['symbol']+','+row['name']+'\n')
for i in range(2,pages+1):
    url = 'https://xueqiu.com/stock/cata/stocklist.json?page='+str(i)+'&size=90&order=desc&orderby=percent&type=30&isdelay=1&_=1529201880625'
    resp=rq.get(url,headers=headers,cookies=_cookies)
    dict=json.loads(resp.text)
    for row in dict['stocks']:
        print(row['symbol'],row['name'])
        f.write(row['symbol']+','+row['name']+'\n')
f.close()
print('香港股票代码及名称爬取并写入HkStockList.csv!')
