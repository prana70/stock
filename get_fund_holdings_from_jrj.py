#coding:utf8

from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import os
import requests as rq



def get_fund_holdings(stockcode,stockname):
    try:
        hd={'User-Agent':'Mozilla/5.0'}
        url='http://fund.jrj.com.cn/fhs/history/'+stockcode+'.shtml'
        print(url)
        resp=rq.get(url,headers=hd)
        soup=bs(resp.text,'html.parser')
        main_table=soup.find('table',class_='sbtable')
        rows=main_table.find_all('tr')
        lines=[]
        for row in rows:
            cells=row.strings
            line=[]
            for cell in cells:
                if cell not in ('(万元)','(%)','\n', '本期明细'):
                    line.append(cell.strip('%'))
            lines.append(line)
        df=pd.DataFrame(data=lines)
        df.to_csv(os.getcwd()+'\\fund_holdings\\'+stockcode+stockname+'.csv',index=False,header=False,encoding='utf8')
        print('添加成功！')
    except:
        print('添加失败！')

f=open('stocks.txt')
i=0
for line in f.readlines():
    stockcode=line[-8:-2]
    stockname=line[0:-9]
    print(stockcode,stockname)
    get_fund_holdings(stockcode,stockname)
    i+=1
    if i==10000:
        break
f.close()
print('-'*60)
print('一共添加：',i)
