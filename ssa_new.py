#coding:utf8

import pandas as pd
import time,datetime
import os
import ssa

def GetAssets(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    print (file)
    df=pd.read_csv(file,index_col=0)
    s_zzc=df.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
    s_jzc=df.loc['所有者权益(或股东权益)合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    #print(s_zzc.index.values)
    #print(s_zzc.values)
    l_index=list(s_zzc.index.values) #报告期列表
    l_zzc=list(s_zzc.values) #总资产列表
    l_jzc=list(s_jzc.values) #净资产列表
    return l_index,l_zzc,l_jzc

if __name__=='__main__':
    stockcode=input('请输入股票代码:')
    GetAssets(stockcode)
