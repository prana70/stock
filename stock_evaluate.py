#coding:utf8

import pandas as pd
#import matplotlib.pyplot as plt
import datetime as dt
import os
import tushare as ts
import intervalue as iv

today=dt.date.today()

#获取业绩预测年份、报告期
year=str(2017)#int(input('请输入年份：'))
quarter=str(4)#int(input('请输入报告期：'))

#根据预测数据算出内在价值
if os.path.exists(year+'年'+quarter+'季度业绩预测.csv'):
    DFofForecastData=pd.read_csv(year+'年'+quarter+'季度业绩预测.csv')
else:
    DFofForecastData=ts.forecast_data(int(year),int(quarter))
    DFofForecastData.to_csv(year+'年'+quarter+'季度业绩预测.csv',encoding='utf-8',index=False)

DFofForecastData['pre_eps']=DFofForecastData['pre_eps']/int(quarter)*4
DFofForecastData['growth']=DFofForecastData['range'].str.extract('(-*\d+)').astype('float')
#DFofForecastData['intervalue']=iv.InterValue(DFofForecastData['growth']/100,DFofForecastData['pre_eps'],0.07,15)
#for i in DFofForecastData.index:
    #print(DFofForecastData.loc[i]['growth'])
    #DFofForecastData.loc[i]['intervalue']=iv.InterValue(DFofForecastData.loc[i]['growth']/100,DFofForecastData.loc[i]['pre_eps'],0.07,15)
#print(DFofForecastData.values)
cls=list(DFofForecastData.columns)
cls.append('intervalue')
#print(cls)
data=[]
for line in DFofForecastData.values:
    line=list(line)
    line.append(iv.InterValue(line[6]/100,line[4],0.07,15))
    data.append(line)
DFofInterValue=pd.DataFrame(data,columns=cls)

#print(DFofInterValue)

if os.path.exists('stock_price.csv'):
    DFofPrice=pd.read_csv('stock_price.csv')
else:
    print('未找到stock_price.csv文件')
#print(DFofPrice)

DFofCompare=pd.merge(DFofInterValue,DFofPrice,left_on='code',right_on='股票代码')
DFofCompare['安全度']=DFofCompare['intervalue']/DFofCompare['最新价']
DFofSecurity=DFofCompare[['code', 'name', 'report_date', 'pre_eps', 'growth',
       'intervalue', '最新价','安全度']]
DFofSecurity.rename(columns={'code':'股票代码', 'name':'股票简称', 'report_date':'预测日期', 'pre_eps':'同期每股收益', 'growth':'增长率（%）','intervalue':'估值'},inplace=True)
DFofSecurity.sort(columns=['安全度'],ascending=False,inplace=True)
DFofSecurity.to_csv('股票估值.csv',index=False)
#print(DFofSecurity)
    
