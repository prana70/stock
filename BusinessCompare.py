import pandas as pd
import os
import stockeval as se
import numpy

file=os.getcwd()+'\\market_data\\StockClass.csv'
df=pd.read_csv(file)
file1=os.getcwd()+'\\stock_pickup\\BusinessCompare.csv'
f=open(file1,'w')
f.write('行业类别,股票代码,股票名称,安全边际,利润成长,营收增长,营运现金,供应链地位\n')
print(file1)
i=0
for row in df.iterrows():
    i+=1
    if i>10000:
        break
    Business=row[1]['行业类别']
    StockCode=row[1]['股票代码'][-6:]
    print(i,StockCode)
    stockcode, stockname, SecurityLevel, GrowthLevel, IncomeLevel, CashLevel, TradePositionLevel=se.GetTotalLevel(StockCode)
    #if type(SecurityLevel)==numpy.float64 and type(GrowthLevel)==float and type(IncomeLevel)==float and type(CashLevel)==float and type(TradePositionLevel)==numpy.float64:
    if stockcode!=None:
        f.write(Business+','+str(stockcode)+','+stockname+','+str(SecurityLevel)+','+str(GrowthLevel)+','+str(IncomeLevel)+','+str(CashLevel)+','+str(TradePositionLevel)+'\n')
#StockCode='000338'
#print(se.GetTotalLevel(StockCode))
f.close()