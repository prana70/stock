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
   
        #打开利润表
        df_original=pd.read_csv('d:\python34\stock_financial\\'+filename,index_col=0).fillna('0').applymap(str_to_float)
        #调整利润表，将季度数据转换成年度数据
        for column in df_original.columns:
            if '1-3月' in column:
                df_original[column]=df_original[column]*4
            if '1-6月' in column:
                df_original[column]=df_original[column]/2*4
            if '1-9月' in column:
                df_original[column]=df_original[column]/3*4

        df_yyqk=df_original.ix[['一、营业收入','减:营业成本','营业税金及附加','销售费用','管理费用','财务费用']]#营业情况
        s_hxlr=df_yyqk.loc['一、营业收入']-df_yyqk.loc['减:营业成本']-df_yyqk.loc['营业税金及附加']-df_yyqk.loc['销售费用']-df_yyqk.loc['管理费用']-df_yyqk.loc['财务费用']
        score=0
        growth_rate=[]
        for i in range(len(s_hxlr)):
            if i==len(s_hxlr):
                break
            growth_rate.append((s_hxlr[-i]/s_hxlr[-(i+1)]-1)*100)
            if s_hxlr[-i]>s_hxlr[-(i+1)] and s_hxlr[-i]>0:
                score+=1
        average_growth_rate=sum(growth_rate)/len(growth_rate)
        compound_growth_rate=(s_hxlr[-1]/s_hxlr[0])*100**(1/(len(s_hxlr)-1))
        
        return True,stockcode,stockname,average_growth_rate,compound_growth_rate,score
    except:
        return False,stockcode,stockname,'未成功！','哈哈','哈哈'


f=open('pickup_stock_by_hxlrhb.csv','w')
f.write('股票代码,股票名称,平均增长率（%）,复合增长率（%）,增长频次\n')
listfiles=os.listdir('d:\python34\stock_financial')
i=0
for listfile in listfiles:
    if listfile[-20:-1]=='incomestatements.cs':
        ok,stockcode,stockname,average_growth_rate,compound_growth_rate,score=pickup_stock(listfile)
        i=i+1
        print(i)
        if ok==True:
            print('oh,yes!')
            f.write(stockcode+','+stockname+','+'%.2f'%average_growth_rate+','+'%.2f'%compound_growth_rate+','+'%i'%score)
            f.write('\n')

f.close()

