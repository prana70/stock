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



#获取供应链地位
def GetTradePosition(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial_sina\\'+stockcode+'balancesheet.csv'
    df=pd.read_csv(file,index_col=0)
    if ssa.get_stock_type(stockcode)=='金融类': #金融类与非金融类股票的项目名称不同，故要作区别对待。
        serr=df.loc[['存放同业款项','拆出资金','同业存入及拆入','拆入资金'],df.columns[-1]]
        s_jyxzc=sum(serr[['存放同业款项','拆出资金']])#经营性资产
        s_jyxfz=sum(serr[['同业存入及拆入','拆入资金']])#经营性负债
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

print(GetTradePosition('000651'))
