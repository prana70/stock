#coding: utf-8

import pandas as pd
import tushare as ts
import os
import datetime as dt


today=dt.date.today()

year_=str(2017)#input('请输入要预测的年份：')
quarter=str(4)#input('请输入要预测的季度：')

if os.path.exists(year_+'年'+quarter+'季度业绩预测.csv'):
    DFofForecastData=pd.read_csv(year_+'年'+quarter+'季度业绩预测.csv',index_col=0)
else:
    DFofForecastData=ts.forecast_data(int(year_),int(quarter))
    DFofForecastData.to_csv(year_+'年'+quarter+'季度业绩预测.csv',encoding='utf-8',index=False)
    

if os.path.exists(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日上市公司基本情况.csv'):
    DFofStockBasics=pd.read_csv(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日上市公司基本情况.csv',index_col=0)
else:
    DFofStockBasics=ts.get_stock_basics()
    DFofStockBasics.to_csv(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日上市公司基本情况.csv',encoding='utf-8')


if os.path.exists(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日股票收盘价.csv'):
    DFofPrice=pd.read_csv(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日股票收盘价.csv',index_col=0)
else:
    DFofPrice=ts.get_today_all()
    DFofPrice.to_csv(str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日股票收盘价.csv',encoding='utf-8',index=False)

print(DFofStockBasics.columns)
print(DFofStockBasics[['name','esp','bvps','pe','pb']])
#print(DFofForecastData.columns)
#print(DFofForecastData[['name', 'type',  'pre_eps', 'range']])
#print(DFofPrice)
#print(DFofPrice[['name', 'trade', 'per', 'pb']])

#df=pd.merge(DFofStockBasics[['name','esp','bvps','pe','pb']],DFofPrice[['name', 'trade', 'per', 'pb']],left_index=True,right_index=True)
#print(df)
'''
df=pd.merge(DFofStockBasics,DFofForecastData,left_index=True,right_index=True)[['name_x', 'pe',  'type',
        'pre_eps', 'range']]
df1=df[(df.type=='预增')&(df.pre_eps>0)]
df1['growth']=df1['range'].str.extract('(\d+)').astype('float')
df1['gpe']=df1['growth']/df1['pe']
df2=df1.sort_values(by='gpe',ascending=False).rename(columns={'name_x':'股票名称','pe':'市盈率','pre_eps':'上年同期每股收益','range':'预增范围','growth':'增长率','gpe':'GPE水准'})
print(df2)
df2.to_csv('gpe.csv',encoding='utf-8')
'''

