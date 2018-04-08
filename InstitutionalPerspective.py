#coding: utf-8
import requests as rq
from bs4 import BeautifulSoup as bs
import json
import datetime
import re
import pandas as pd

def GetCookies(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    return rq.get(url,headers=headers).cookies


def GetScore(perspective):
    if perspective=='买入':
        return 2
    elif perspective=='增持':
        return 1
    else:
        return 0

def GetInstitutionalPerspective(StockCode):
    CookiesUrl='https://xueqiu.com/'
    #StockCode=input('请输入股票代码：')
    MarketCode={'600':'SH','601':'SH','603':'SH','000':'SZ','002':'SZ','300':'SZ'}

    #df=pd.DataFrame() #columns=['stockCode','institution','perspective','releaseDate']
    rows=[]
    count=10
    page=0
    maxPage=1
    while page<=maxPage:
        page+=1
        url='https://xueqiu.com/statuses/stock_timeline.json?symbol_id='+MarketCode[StockCode[:3]]+StockCode+'&count=10&source=%E7%A0%94%E6%8A%A5&page='+str(page)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
        _cookies=GetCookies(CookiesUrl)

        resp=rq.get(url,headers=headers,cookies=_cookies)
        dict=json.loads(resp.text)
        maxPage=dict['maxPage']
        #print(maxPage,page)
        #print(dict)
        #print(dict['maxPage'],dict['count'],dict['page'])
        for ele in dict['list']:
            row=[StockCode]

            #print(ele['description'])
            #print(ele['text'])
            #print(ele['title'])
            institutionPerspective=re.compile(r'［.+］')
            ReleaseDate=re.compile(r'发布时间：\d{4}-\d{2}-\d{2}|时间：\d{4}-\d{2}-\d{2}')
            #print(institutionPerspective.findall(ele['title'])[0][1:-1].split('：'),ReleaseDate.findall(ele['text'])[0][-10:])
            row.append(institutionPerspective.findall(ele['title'])[0][1:-1].split('：')[0])
            row.append(institutionPerspective.findall(ele['title'])[0][1:-1].split('：')[1])
            row.append(ReleaseDate.findall(ele['text'])[0][-10:])
            #df.append({'stockCode':StockCode,'institution':institutionPerspective.findall(ele['title'])[0][1:-1].split('：')[0],
                      # 'perspective':institutionPerspective.findall(ele['title'])[0][1:-1].split('：')[1],'releaseDate':ReleaseDate.findall(ele['text'])[0][-10:]},ignore_index=True)
            rows.append(row)
    #print(rows)
    df=pd.DataFrame(rows,columns=['stockCode','institution','perspective','releaseDate'])
    df['releaseMonth']=df['releaseDate'].str.slice(0,7)
    df['score']=df['perspective'].apply(lambda x:GetScore(x))
    df.groupby(['stockCode','releaseDate']).sum()
    df1=df.groupby(['stockCode','releaseMonth'],as_index=False).sum()
    #print(df1)
    labels=list(df1['releaseMonth'])
    #print(labels)
    data=list(df1['score'])
    #print(data)
    return labels,data

if __name__=="__main__":
    StockCode=input('请输入股票代码：')
    GetInstitutionalPerspective(StockCode)
    

    
        
