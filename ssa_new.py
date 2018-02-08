#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import time,datetime
import os

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#用于将dataframe的数字型字符串转换成浮点数
def str_to_float(str):
    if type(str)==type('ok'):
        return float(str.replace(',',''))
    else:
        return str


stockcode=input('请输入股票代码：')

#从stocks.txt中查询股票简称
stockname=''
f=open('stocks.txt','r')
lines=f.readlines()
for line in lines:
    if line[-8:-2]==stockcode:
        stockname=line[:-9].replace('*','')
        break
f.close()

#打开利润表和现金流量表
df_lrb=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'incomestatements.csv',index_col=0).fillna('0').applymap(str_to_float)
df_xjllb=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'cashflow.csv',index_col=0).fillna('0').applymap(str_to_float)

print(df_lrb.columns[3])
