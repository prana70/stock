#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import time,datetime

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']

import os

#用于将dataframe的数字型字符串转换成浮点数
def str_to_float(str):
    return float(str.replace(',',''))

def pickup_stock(filename):
    stockcode=filename[0:6]
    stockname=filename[6:10]
    try:
   
        #打开现金流量表
        df_original=pd.read_csv('d:\python34\stock_financial\\'+filename,index_col=0).fillna('0').applymap(str_to_float)
        df_original['2015Q1']=df_original['2015年1-3月']
        df_original['2015Q2']=df_original['2015年1-6月']-df_original['2015年1-3月']
        df_original['2015Q3']=df_original['2015年1-9月']-df_original['2015年1-6月']
        df_original['2015Q4']=df_original['2015年度']-df_original['2015年1-9月']
        df_original['2016Q1']=df_original['2016年1-3月']
        df_original['2016Q2']=df_original['2016年1-6月']-df_original['2016年1-3月']
        df_original['2016Q3']=df_original['2016年1-9月']-df_original['2016年1-6月']

        df_xjqk=df_original.ix[['经营活动产生的现金流量净额','购建固定资产、无形资产和其他长期资产支付的现金'],['2015Q1','2015Q2','2015Q3','2015Q4','2016Q1','2016Q2','2016Q3']]#营业收入
        s_fcf=df_xjqk.loc['经营活动产生的现金流量净额']-df_xjqk.loc['购建固定资产、无形资产和其他长期资产支付的现金']
        if s_fcf['2016Q3']>s_fcf['2016Q2'] and s_fcf['2016Q2']>s_fcf['2016Q1'] and s_fcf['2016Q1']>s_fcf['2015Q4'] and s_fcf['2015Q4']>s_fcf['2015Q3'] and s_fcf['2015Q3']>s_fcf['2015Q2']:
            return True,stockcode,stockname,s_fcf
        else:
            return False,stockcode,stockname,'不符合条件！'
    except:
        return False,stockcode,stockname,'未成功！'


f=open('pickup_stock_by_fcfhb.csv','w')
f.write('股票代码,股票名称,2015Q1,2015Q2,2015Q3,2015Q4,2016Q1,2016Q2,2106Q3\n')
listfiles=os.listdir('d:\python34\stock_financial')
i=0
for listfile in listfiles:
    if listfile[-12:-1]=='cashflow.cs':
        ok,stockcode,stockname,result=pickup_stock(listfile)
        i=i+1
        print(i)
        if ok==True:
            print('oh,yes!')
            f.write(stockcode+','+stockname)
            for ele in result:
                f.write(','+str(ele))
            f.write('\n')

f.close()

