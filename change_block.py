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



def GetInvestmentCash(stockcode):  # 获取投资、经营性投资支付的现金
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    if '预计负债' in df6.index: # 普通类
        s_tzzfxj = df6.loc['投资所支付的现金'] / 10000  # 投资现金净额
    else: # 银行类、证券类、保险类
        s_tzzfxj = df6.loc['投资支付的现金'] / 10000  # 投资现金净额
    
    # 投资现金净额换算成季度数据
    s_tzzfxj_value = []
    s_tzzfxj_index = []
    for i in range(len(s_tzzfxj)):
        if i > 0 and '12-31' in s_tzzfxj.index[i] and '09-30' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '10-12月')
        elif '09-30' in s_tzzfxj.index[i] and '06-30' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '7-9月')
        elif '06-30' in s_tzzfxj.index[i] and '03-31' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '4-6月')
        else:
            s_tzzfxj_value.append(s_tzzfxj[i])
            s_tzzfxj_index.append(s_tzzfxj.index[i])
    s_tzzfxj_new = pd.Series(s_tzzfxj_value, index=s_tzzfxj_index)
    s_tzzfxj_new.name = s_tzzfxj.name

    if '预计负债' in df6.index: # 普通类
        print('执行普通类')
        s_jytzxj = df6.loc['购建固定资产、无形资产和其他长期资产所支付的现金'] / 10000  # 经营投资现金
    else: # 银行类、证券类、保险类
        print('执行金融类')
        s_jytzxj = df6.loc['购建固定资产、无形资产和其他长期资产支付的现金'] / 10000  # 经营投资现金
    s_jytzxj_value = []
    s_jytzxj_index = []
    for i in range(len(s_jytzxj)):
        if i > 0 and '12-31' in s_jytzxj.index[i] and '09-30' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '10-12月')
        elif '09-30' in s_jytzxj.index[i] and '06-30' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '7-9月')
        elif '06-30' in s_jytzxj.index[i] and '03-31' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '4-6月')
        else:
            s_jytzxj_value.append(s_jytzxj[i])
            s_jytzxj_index.append(s_jytzxj.index[i])
    s_jytzxj_new = pd.Series(s_jytzxj_value, index=s_jytzxj_index)
    s_jytzxj_new.name = s_jytzxj.name

    # 数据整理
    labels = list(s_jytzxj_new.index.values)  # x轴标签
    data1 = list(s_tzzfxj_new.values)  # 投资支付的现金
    data2 = list(s_jytzxj_new.values)  # 购建固定资产、无形资产和其他长期资产支付的现金

    return labels, data1, data2
    
    

print(GetInvestmentCash('600036'))





