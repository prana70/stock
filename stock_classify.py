#coding:utf8

import pandas as pd
#import matplotlib.pyplot as plt
#import time,datetime
import os

#import matplotlib as mpl
#mpl.rcParams['font.sans-serif'] = ['SimHei']
#mpl.rcParams['font.serif'] = ['SimHei']
#mpl.rcParams['axes.unicode_minus']=False

#用于将dataframe的数字型字符串转换成浮点数
'''
def str_to_float(str):
    if type(str)==type('ok'):
        return float(str.replace(',',''))
    else:
        return str
'''


stockcode=''
stockname=''
f1=open('stocks.txt','r')
f2=open('stock_type.txt','w')
lines=f1.readlines()
i=0
for line in lines:
    print (i)
    i+=1
    stockcode=line[-8:-2]
    stockname=line[:-9]
    if os.path.isfile(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'balancesheet.csv'):
        df=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'balancesheet.csv',index_col=0)
        if '现金及存放同业款项' in df.index:
            f2.write(stockcode+'--金融类\n')
            print(stockcode+'--金融类')
        else:
            f2.write(stockcode+'--普通类\n')
            print(stockcode+'--普通类')
    else:
        f2.write(stockcode+'--财务数据文件不存在！\n')
        print(stockcode+'--财务数据文件不存在！')

f2.close()
f1.close()
