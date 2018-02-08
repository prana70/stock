#coding:utf-8

import pandas as pd
import stockeval as se
import os
import numpy

f0=open(os.getcwd()+'\\stocks.txt','r')
f1=open(os.getcwd()+'\\stock_pickup\\pickup_stock_by_stockeval.csv','w')
f1.write('股票代码,股票名称,股价合理性,利润成长,营收增长,现金能力,供应链地位\n')
i=0
for line in f0.readlines():
    stockcode=line[-8:-2]
    stockcode,stockname,SecurityLevel,GrowthLevel,IncomeLevel,CashLevel,TradePositionLevel=se.GetTotalLevel(stockcode)
    if type(SecurityLevel)==numpy.float64 and type(GrowthLevel)==float and type(IncomeLevel)==float and type(CashLevel)==float and type(TradePositionLevel)==numpy.float64:
        if SecurityLevel>4 and CashLevel>4 and TradePositionLevel>4:
            f1.write(str(stockcode)+','+stockname+','+str(SecurityLevel)+','+str(GrowthLevel)+','+str(IncomeLevel)+','+str(CashLevel)+','+str(TradePositionLevel)+'\n')
            print(i,stockcode,stockname,'符合条件，已加入备选池！')
        else:
            print(i,stockcode,stockname,'不符合条件！')
    else:
        print(i,stockcode,stockname,'不符合条件！')
    i+=1
f0.close()
f1.close()
