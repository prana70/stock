#coding:utf8

import requests as rq
import pandas as pd
import re
import json
import os




def abstract_stock_name(str):
    reg=re.compile(r"<u>(.*)</u>")
    return reg.findall(str)[0]

#get stock list from 深交所
def get_stocklist_from_sz():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
    dfs=[]
    for i in range(1,110):#110
        print(i)
        url='http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO='+str(i)+'&random=0.18658872394186599'
        resp=rq.get(url,headers=headers,timeout=9)
        x=resp.json()
        df=pd.DataFrame(x[0]['data'])
        if not df is None:
            dfs.append(df)
    df=pd.concat(dfs,ignore_index=True)
    df.rename(columns={'agdm':'股票代码','agjc':'股票名称'},inplace=True)
    df=df[['股票代码','股票名称']]
    df['交易所']='深圳'
    df['股票名称']=df['股票名称'].apply(abstract_stock_name)
    df['股票名称']=df['股票名称'].str.replace(' ','')
    
    return df

#get stock list from 上交所
def get_stocklist_from_sh():
    headers={'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml?COMPANY_CODE=600398',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
                 }
    dfs=[]
    for i in range(1,60):#60
        print(i)
        url='http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback77223&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage='+str(i)+'&pageHelp.pageSize=25&pageHelp.pageNo='+str(i)+'&_=1563794020990'
        resp=rq.get(url,headers=headers,timeout=9)
        str_=resp.text
        reg=re.compile(r".*\((.*)\)")
        m=re.match(reg,str_)
        m=m.groups(1)[0]
        n=json.loads(m)
        df=pd.DataFrame(n['pageHelp']['data'])
        if not df is None:
            dfs.append(df)
    df=pd.concat(dfs,ignore_index=True)
    df.rename(columns={'SECURITY_CODE_A':'股票代码','SECURITY_ABBR_A':'股票名称'},inplace=True)
    df=df[['股票代码','股票名称']]
    df['交易所']='上海'
    df['股票名称']=df['股票名称'].str.replace(' ','')

    return df

if __name__=='__main__':
    df1=get_stocklist_from_sz()
    df2=get_stocklist_from_sh()
    df=pd.concat([df1,df2])
    df.to_csv(os.getcwd()+'\\market_data\\stock_list.csv',index=False)

