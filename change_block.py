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
import stockeval as se
import ssa_new


dir_=os.getcwd()+'\\stock_financial_sina\\'
files=os.listdir(dir_)

done_stock_list=[]
for file in files:
    stock_code=file[:6]
    if stock_code not in done_stock_list:
        stock_name=ssa.get_stockname(stock_code)
        labels,operate_cash_flow,free_cash_flow=ssa_new.GetFreeCashFlowSum(stock_code)
        #print(labels)
        if len(free_cash_flow)>=30:
            y=free_cash_flow[-30:]
            
            y=1-(max(y)-y)/(max(y)-min(y))
            x=range(0,len(y))
            print(len(y))



            plt.plot(x,y)
            plt.ylabel('累计自由现金流')
            plt.xlabel('期数')
            plt.title(stock_code+stock_name)
            plt.show()
        done_stock_list.append(stock_code)

'''
stock_code='000723'
stock_name=ssa.get_stockname(stock_code)
labels,operate_cash_flow,free_cash_flow=ssa_new.GetFreeCashFlowSum(stock_code)
#print(labels)
if len(free_cash_flow)>=30:
    y=free_cash_flow[-30:]
    y=y/max(y)
    x=range(0,len(y))
    print(len(y))



    plt.plot(x,y)
    plt.ylabel('累计自由现金流')
    plt.xlabel('期数')
    plt.title(stock_code+stock_name)
    plt.show()

'''




