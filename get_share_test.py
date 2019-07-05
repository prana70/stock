#coding:utf8

import requests as rq
import pandas as pd
import re
import json


'''
MarketType={'600':'shmb','601':'shmb','603':'shmb','000':'szmb','002':'szsme','300':'szcn'} #根据股票代码确定市场类型

stockcode=input('请输入股票代码：')

if stockcode[0:3] in ('000','002','300'):

    
    url='http://www.szse.cn/api/report/index/companyGeneralization?random=0.9215521283280892&secCode='+stockcode
    headers={'User-Agent':'Mozilla/5.0'}
    resp=rq.get(url,headers=headers,timeout=9)
    print(float(resp.json()['data']['agzgb'].replace(',',''))*10000)
    
elif stockcode[0:3] in ('600','601','603'):
    url='http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?jsonCallBack=jsonpCallback55789&isPagination=false&companyCode=600398&_=1560706165309'

    headers={'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml?COMPANY_CODE=600398',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
             }

    resp=rq.get(url,headers=headers,timeout=9)
    resp.encoding='utf8'
    str=resp.text
    reg=re.compile(r".*\((.*)\)")
    m=re.match(reg,str)
    m=m.groups(1)[0]
    n=json.loads(m)
    print(float(n['result']['totalShares'])*10000)
else:
    print('股票代码不是深交所或上交所的！！！')

'''
url='http://finance.sina.com.cn/realstock/company/sz002323/nc.shtml'
resp=rq.get(url)
print(resp.status_code)
resp.encoding='gb2312'
reg=re.compile(r'var totalcapital = ([\d.]*)')
text=resp.text
r=reg.findall(text)

print(float(r[0])*10000)
