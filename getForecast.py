#coding:utf8

import pandas as pd
import os
import tushare as ts

#获取业绩预测年份、报告期
year=str(2017)#int(input('请输入年份：'))
quarter=str(4)#int(input('请输入报告期：'))

df=ts.forecast_data(int(year),int(quarter))
#print(df)
df.to_csv(os.getcwd()+'\\market_data\\业绩预测.csv',encoding='utf-8',index=False)
print('ok!')
