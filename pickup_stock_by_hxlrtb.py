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
        df_original=pd.read_csv(os.getcwd()+'\\'+filename,index_col=0).fillna('0').applymap(str_to_float)

        df_original['2015Q1']=df_original['2015年1-3月']
        df_original['2015Q2']=df_original['2015年1-6月']-df_original['2015年1-3月']
        df_original['2015Q3']=df_original['2015年1-9月']-df_original['2015年1-6月']
        df_original['2015Q4']=df_original['2015年度']-df_original['2015年1-9月']
        df_original['2016Q1']=df_original['2016年1-3月']
        df_original['2016Q2']=df_original['2016年1-6月']-df_original['2016年1-3月']
        df_original['2016Q3']=df_original['2016年1-9月']-df_original['2016年1-6月']

        df_yyqk=df_original.ix[['一、营业收入','减:营业成本','营业税金及附加','销售费用','管理费用','财务费用'],['2015Q1','2015Q2','2015Q3','2015Q4','2016Q1','2016Q2','2016Q3']]#营业收入
        s_hxlr=df_yyqk.loc['一、营业收入']-df_yyqk.loc['减:营业成本']-df_yyqk.loc['营业税金及附加']-df_yyqk.loc['销售费用']-df_yyqk.loc['管理费用']-df_yyqk.loc['财务费用']
        if s_hxlr['2016Q3']/s_hxlr['2015Q3']>1 and s_hxlr['2016Q2']/s_hxlr['2015Q2']>1 and s_hxlr['2016Q1']/s_hxlr['2015Q1']>1:
            return True,stockcode,stockname,s_hxlr
        else:
            return False,stockcode,stockname,'不符合条件！'
    except:
        return False,stockcode,stockname,'未成功！'


f=open('pickup_stock_by_hxlrtb.csv','w')
f.write('股票代码,股票名称,2015Q1,2015Q2,2015Q3,2015Q4,2016Q1,2016Q2,2106Q3\n')
listfiles=os.listdir(os.getcwd()+'\stock_financial')
i=0
for listfile in listfiles:
    if listfile[-20:-1]=='incomestatements.cs':
        print(listfile)
        ok,stockcode,stockname,result=pickup_stock(listfile)
        i=i+1
        if ok==True:
            print('oh,yes!')
            f.write(stockcode+','+stockname)
            for ele in result:
                f.write(','+str(ele))
            f.write('\n')
    if i==10:
        break
f.close()

