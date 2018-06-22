import requests as rq
from bs4 import BeautifulSoup as bs
import json
import InstitutionalPerspective as ip
import math
import os


#从雪球行情中心获取证监会行业分类，并将每个行业对业的股票数据下载并写入StockClass.csv
url='https://xueqiu.com/hq'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
CookiesUrl='https://xueqiu.com/'
_cookies=ip.GetCookies(CookiesUrl)

resp=rq.get(url,headers=headers)
soup=bs(resp.text,'html.parser')
f=open(os.getcwd()+'\\market_data\\StockClass.csv','w',encoding='utf8')
f.write('行业类别,股票代码,股票名称\n')
for row in soup.find_all('div',class_='third-nav')[1].find_all('a'):
    StockClass=row['title']
    level2code=row['href'][-3:]
    StockListUrl='https://xueqiu.com/industry/quote_order.json?page=1&size=90&order=desc&exchange=CN&plate='+StockClass+'&orderBy=percent&level2code='+level2code+'&_=1529068704076'
    resp1=rq.get(StockListUrl,headers=headers,cookies=_cookies)
    dict=json.loads(resp1.text)
    for line in dict['data']:
        print(StockClass,line['symbol'][-8:],line['name'])
        f.write(StockClass+','+line['symbol'][-8:]+','+line['name']+'\n')
    if dict['count']>90:
        #print('超过90：',StockClass)
        pages=math.ceil(dict['count']/90)
        for i in range(2,pages+1):
            StockListUrl = 'https://xueqiu.com/industry/quote_order.json?page='+str(i)+'&size=90&order=desc&exchange=CN&plate=' + StockClass + '&orderBy=percent&level2code=' + level2code + '&_=1529068704076'
            resp1 = rq.get(StockListUrl, headers=headers, cookies=_cookies)
            dict = json.loads(resp1.text)
            for line in dict['data']:
                print(StockClass, line['symbol'][-8:],line['name'])
                f.write(StockClass + ',' + line['symbol'][-8:] + ','+line['name']+'\n')
f.close()