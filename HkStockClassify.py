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
f=open(os.getcwd()+'\\market_data\\HkStockClass.csv','w',encoding='utf8')
f.write('行业类别,股票代码,股票名称\n')
for row in soup.find_all('div',class_='third-nav')[3].find_all('a'):
    StockClass=row['title']
    level2code=row['href'][-3:]
    StockListUrl='https://xueqiu.com/stock/cata/stocklist.json?page=1&size=90&order=desc&orderby=percent&exchange=HK&plate='+StockClass+'&isdelay=1&_=1529198893432'
    resp1=rq.get(StockListUrl,headers=headers,cookies=_cookies)
    dict=json.loads(resp1.text)
    for line in dict['stocks']:
        print(StockClass,line['symbol'],line['name'])
        f.write(StockClass+','+line['symbol']+','+line['name']+'\n')
    if dict['count']['count']>90:
        pages=math.ceil(dict['count']['count']/90)
        for i in range(2,pages+1):
            StockListUrl = 'https://xueqiu.com/stock/cata/stocklist.json?page='+str(i)+'&size=90&order=desc&orderby=percent&exchange=HK&plate='+StockClass+'&isdelay=1&_=1529198893432'
            resp1 = rq.get(StockListUrl, headers=headers, cookies=_cookies)
            dict = json.loads(resp1.text)
            for line in dict['data']:
                print(StockClass, line['symbol'],line['name'])
                f.write(StockClass + ',' + line['symbol'] + ','+line['name']+'\n')
f.close()
print('香港股票爬取并写入完成！')
