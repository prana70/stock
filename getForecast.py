#coding:utf8

import pandas as pd
import os
import tushare as ts

#获取业绩预测年份、报告期
year=input('请输入年份：')
quarter=input('请输入报告期：')

df=ts.forecast_data(int(year),int(quarter))
#print(df)
df.to_csv(os.getcwd()+'\\market_data\\业绩预测.csv',encoding='utf-8',index=False)
print('ok!')
