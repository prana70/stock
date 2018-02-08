#coding:utf8

import requests as rq
from bs4 import BeautifulSoup as bs

from pandas import DataFrame
import pandas as pd

import time

import os
from functools import reduce

#调取指定巨潮信息网页的数据，调取成功则整理加入一个dataframe返回，不成功返回None.
def get_dataframe(url,hd):
    try:
        resp=rq.post(url,headers=hd)
        soup=bs(resp.text,'html.parser')
        main_div=soup.find('div',class_='clear')
        if 'balancesheet' in url:
            sub_tags=main_div.find_all('div')
        else:
            sub_tags=main_div.find_all('td')
        item=[]
        data=[]
        i=0
        for sub_tag in sub_tags:
            if i>1:
                if i%2==0:
                    item.append(sub_tag.string.strip())
                else:
                    data.append(sub_tag.string.strip())
            i+=1
        dataset=list(zip(item,data))
        df=pd.DataFrame(data=dataset)
        df.to_csv('ls.csv',index=False,header=False,encoding='utf8')
        new_df=pd.read_csv('ls.csv')
        os.remove('ls.csv')
        return new_df
    except:
        return None

#获取股票的财务数据
def get_stock_financial(stockcode,stockname):
    base_url='http://www.cninfo.com.cn/information/stock/'
    financial_indexs=['balancesheet','incomestatements','cashflow']
    for cwzb in financial_indexs:
        urls=[]
        yrs=range(2007,2018)
        for yyyy in yrs:
            mths=['-03-31','-06-30','-09-30','-12-31']
            for mm in mths:
                urls.append(base_url+cwzb+'_.jsp?stockCode='+stockcode+'&yyyy='+str(yyyy)+'&mm='+mm)
        urls.append(base_url+cwzb+'_.jsp?stockCode='+stockcode)
        hd={'User-Agent':'Mozilla/5.0'}
        dfs=[]
        for url in urls:
            df=get_dataframe(url,hd)
            if type(df)!=type(None):
                dfs.append(df)
                #print(url+' 数据读取成功')
            else:
                pass
                #print(url+' 数据读取失败')
        if len(dfs)>1:
            total_df=reduce(pd.merge,dfs)
        else:
            if len(dfs)==1:
                total_df=dfs[0]
            else:
                total_df=None
        if type(total_df)!=type(None):
            total_df.to_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+cwzb+'.csv',encoding='utf8',index=False)
            print(stockcode+stockname+cwzb+'.csv写入成功')
        else:
            print(stockcode,stockname,'没有数据')
    return

#根据股票代码查找股票简称，如果查找到，则调用函数获取股票的财务数据
def check_stockname(stockcode):
    stockname=''
    f=open('stocks.txt','r')
    for line in f.readlines():
        if line[-8:-2]==stockcode:
            stockname=line[:-9].strip('*')
            break
    if stockname=='':
        print(stockcode+'--该股票代码没有对应的股票简称，请核查！')
        pass
    else:
        print(stockcode,stockname,'财务数据添加......')
        get_stock_financial(stockcode,stockname)
    f.close()

    
if __name__=='__main__':
    #计时开始
    t0=time.time()

    #定义股票代码
    stockcode=input('请输入股票代码:')
    check_stockname(stockcode)
    t1=time.time()
    print('用时：','%f'%(t1-t0),'秒')



'''
f=open('stocks.txt','r')
lines=f.readlines()
i=0
for line in lines:
    t0=time.time()
    stockcode=line[-8:-2]
    stockname=line[:-9].replace('*','')
    if os.path.isfile('d:\python34\stock_financial\\'+stockcode+stockname+'balancesheet.csv') and os.path.isfile('d:\python34\stock_financial\\'+stockcode+stockname+'incomestatements.csv') and os.path.isfile('d:\python34\stock_financial\\'+stockcode+stockname+'cashflow.csv'):
        print(stockcode,stockname,'财务数据已下载')
    else:
        get_stock_financial(stockcode,stockname)
    t1=time.time()
    i=i+1
    print('第',i,'条','用时',str(t1-t0),'秒')
    #if i>62:
        #break


f.close()
'''


             








