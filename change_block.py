#coding:utf-8

import pandas as pd
#import get_stockprice_from_hexun as gsfh
from bs4 import BeautifulSoup as bs
import requests as rq
import os,time
import ssa
import numpy as np
from intervalue import InterValue as iv
import matplotlib.pyplot as plt
import tushare as ts
import math
import re
import json


#if ssa.get_stock_type(stockcode)=='金融类':  # 对金融类和非金融类要作区分
'''
        for item in df.columns:
            if df[item]['应收票据及应收账款']==0:
                df[item]['应收票据及应收账款']=df[item]['应收票据']+df[item]['应收账款']
            #if df[item]['应付票据及应付账款']==0:
                #df[item]['应付票据及应付账款']=df[item]['应付票据']+df[item]['应付账款']
'''
'''
def GetReceivablesRate(stockcode):  # 获取应收账款比率
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'incomestatements.csv'

    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)

    if '现金及存放同业款项' in df1.index.values:  # 对金融类和非金融类要作区分,计算应收账款
        df3 = df1.loc[['应收利息', '应收保费', '应收代位追偿款', '应收分保帐款', '应收分保未到期责任准备金', '应收分保未决赔款准备金',
                       '应收分保寿险责任准备金', '应收分保长期健康险责任准备金', '应收款项']].fillna('0').applymap(ssa.str_to_float) / 100000000
        s_yszk = df3.loc['应收利息'] + df3.loc['应收保费'] + df3.loc['应收代位追偿款'] + df3.loc['应收分保帐款'] + \
                 df3.loc['应收分保未到期责任准备金'] + df3.loc['应收分保未决赔款准备金'] + df3.loc['应收分保寿险责任准备金'] + \
                 df3.loc['应收分保长期健康险责任准备金'] + df3.loc['应收款项']
    else:
        s_yszk = df1.loc['应收账款'].str.replace(',', '').fillna('0').astype(float) / 100000000

    s_yysr = df2.loc['一、营业收入'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 获取营业收入
    s_yysr_new_index = []
    for index in s_yysr.index.values:  # 将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index] = s_yysr[index] * 4
            s_yysr_new_index.append(index[0:4] + '-03-31')
        if '1-6月' in index:
            s_yysr[index] = s_yysr[index] / 2 * 4
            s_yysr_new_index.append(index[0:4] + '-06-30')
        if '1-9月' in index:
            s_yysr[index] = s_yysr[index] / 3 * 4
            s_yysr_new_index.append(index[0:4] + '-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4] + '-12-31')
    s_yysr = pd.Series(s_yysr.values, index=s_yysr_new_index)
    ReceivableRate = s_yszk / s_yysr * 100
    labels = list(ReceivableRate.index.values)
    data = list(ReceivableRate.values)
    # print(labels,data)
    return labels, data

print(GetAssetsSource('600036'))
'''
'''
df1=pd.read_csv(os.getcwd()+'\\stock_financial_sina\\000651cashflow.csv',index_col=0)
df2=pd.read_csv(os.getcwd()+'\\stock_financial_sina\\600036cashflow.csv',index_col=0)
df3=pd.read_csv(os.getcwd()+'\\stock_financial_sina\\600837cashflow.csv',index_col=0)
df4=pd.read_csv(os.getcwd()+'\\stock_financial_sina\\601318cashflow.csv',index_col=0)

for item in df4.index:
    if item not in list(df1.index)+list(df2.index)+list(df3.index):
        print(item)

'''
#获取供应链地位
def GetTradePosition(stockcode):
    '''
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    df0=pd.read_csv(file,index_col=0).fillna('0')
    df1=df0.loc[['应收票据','应收账款','预付款项','应付票据','应付账款','预收款项']].applymap(ssa.str_to_float)
    #print(df1)
    s_jyxzc=sum(df1[df1.columns[-1]][['应收票据','应收账款','预付款项']])#经营性资产
    #print(s_jyxzc)
    s_jyxfz=sum(df1[df1.columns[-1]][['应付票据','应付账款','预收款项']])#经营性负债
    #print (s_jyxfz)
    return (s_jyxfz-s_jyxzc)/s_jyxzc
    '''
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial_sina\\'+stockcode+'balancesheet.csv'
    df=pd.read_csv(file,index_col=0)
    if '贵金属' in df.index: #银行类。
        serr=df.loc[['存放同业款项','拆出资金','同业存入及拆入','拆入资金'],df.columns[-1]]
        s_jyxzc=sum(serr[['存放同业款项','拆出资金']])#经营性资产
        s_jyxfz=sum(serr[['同业存入及拆入','拆入资金']])#经营性负债
    elif '融出资金' in df.index: #证券类
        serr=df.loc[['融出资金','应收账款','应收利息','拆入资金','应付账款','应付利息'],df.columns[-1]]
        s_jyxzc=sum(serr[['融出资金','应收账款','应收利息']])#经营性资产
        s_jyxfz=sum(serr[['拆入资金','应付账款','应付利息']])#经营性负债
    elif '应收保费' in df.index: #保险类
        serr=df.loc[['拆出资金','应收保费','应收利息','应收分保账款','拆入资金','预收账款','预收保费','应付手续费及佣金','应付分保账款','应付利息'],df.columns[-1]]
        s_jyxzc=sum(serr[['拆出资金','应收保费','应收利息','应收分保账款']])#经营性资产
        s_jyxfz=sum(serr[['拆入资金','预收账款','预收保费','应付手续费及佣金','应付分保账款','应付利息']])#经营性负债
        
    else:
        serr=df.loc[['应收票据及应收账款','应收票据','应收账款','预付款项','应付票据及应付账款','应付票据','应付账款','预收款项'],df.columns[-1]]
        if serr['应收票据及应收账款']==0:
            s_jyxzc=sum(serr[['应收票据','应收账款','预付款项']])#经营性资产
        else:
            s_jyxzc=sum(serr[['应收票据及应收账款','预付款项']])#经营性资产
        if serr['应付票据及应付账款']==0:
            s_jyxfz=sum(serr[['应付票据','应付账款','预收款项']])#经营性负债
        else:
            s_jyxfz=sum(serr[['应付票据及应付账款','预收款项']])#经营性负债
        
    return s_jyxfz/(s_jyxfz+s_jyxzc)

print(GetTradePosition('601318'))





