#coding:utf-8

import pandas as pd
import get_stockprice_from_hexun as gsfh
from bs4 import BeautifulSoup as bs
import requests as rq
import os,time
import ssa
import numpy as np
from intervalue import InterValue as iv
import matplotlib.pyplot as plt
import tushare as ts
import math




#获取股票价格
def GetStockPrice(stockcode):
    df=ts.get_k_data(stockcode)
    RowNo=len(df.index)-1
    return df.at[RowNo,'close']

#获取最新股本
def GetShares(stockcode):
    header={'User-Agent':'Mozilla/5.0'}
    MarketType={'600':'shmb','601':'shmb','603':'shmb','000':'szmb','002':'szsme','300':'szcn'} #根据股票代码确定市场类型
    url='http://www.cninfo.com.cn/information/lastest/'+MarketType[stockcode[0:3]]+stockcode+'.html'
    #print(url)
    resp=rq.get(url,headers=header,timeout=9)
    resp.encoding='gbk'
    soup=bs(resp.text,'html.parser')
    shares=float(soup.find_all('table')[1].find_all('td')[1].string.replace(',',''))
    return shares
    
#获取最近年度的净利润（亦可采用“归属于母公司所有者的净利润”）
def GetNetProfit(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'
    df=pd.read_csv(file,index_col=0)    
    #print(df)
    i=len(df.columns)-1
    while i>=0:
        if '年度' in df.columns[i]:
            LastYear=df.columns[i]
            #print(LastYear)
            break
        i-=1
    if ssa.get_stock_type(stockcode)=='金融类': #金融类与非金融类股票的净利润项目名称不同，故要作区别对待。
        NetProfitName='（一）归属于母公司所有者的净利润'#'五、净利润'
    else:
        NetProfitName='归属于母公司所有者的净利润'#'四、净利润'
    #print(df.loc[NetProfitName])
    NetProfit=float(df.at[NetProfitName,LastYear].replace(',',''))
    return NetProfit

#获取净利润增长率
def GetNetProfitGrowth(stockcode):
    file=os.getcwd()+'\\market_data\\'+'业绩预测.csv'
    #print(file)
    df=pd.read_csv(file,index_col=0)
    df['growth']=df['range'].str.extract('(\d+|-\d+)',expand=True).astype('float')
    #print(df)
    if int(stockcode) in list(df.index.values):
        growth=df.at[int(stockcode),'growth']
        if type(growth)==np.float64:
            #print(growth/100)
            return growth/100
        else:
            #print(growth[0]/100)
            return growth[0]/100
    else:
        stockname=ssa.get_stockname(stockcode)
        file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'
        df=pd.read_csv(file,index_col=0)
        #print(df)
        TermType={'1-3月':1,'1-6月':2,'1-9月':3,'度':4}
        i=len(df.columns)-1
        CurrentTerm=df.columns[i]
        LastTerm=str(int(CurrentTerm[:4])-1)+CurrentTerm[4:]
        if LastTerm not in df.columns:
            LastTerm=str(int(CurrentTerm[:4])-1)+'年度'
        if ssa.get_stock_type(stockcode)=='金融类': #金融类与非金融类股票的净利润项目名称不同，故要作区别对待。
            NetProfitName='（一）归属于母公司所有者的净利润'#'五、净利润'
        else:
            NetProfitName='归属于母公司所有者的净利润'#'四、净利润'
        CurrentProfit=float(df.at[NetProfitName,CurrentTerm].replace(',',''))/TermType[CurrentTerm[5:]]*4
        #print(CurrentTerm,CurrentProfit)
        LastProfit=float(df.at[NetProfitName,LastTerm].replace(',',''))/TermType[LastTerm[5:]]*4
        #print(LastTerm,LastProfit)
        #print(CurrentProfit/LastProfit-1)
        return CurrentProfit/LastProfit-1
        
#获取营业收入增长率
def GetIncomeGrowth(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'
    df=pd.read_csv(file,index_col=0)
    #print(df)
    TermType={'1-3月':1,'1-6月':2,'1-9月':3,'度':4}
    i=len(df.columns)-1
    CurrentTerm=df.columns[i]
    LastTerm=str(int(CurrentTerm[:4])-1)+CurrentTerm[4:]
    if LastTerm not in df.columns:
        LastTerm=str(int(CurrentTerm[:4])-1)+'年度'
    IncomeName='一、营业收入'
    CurrentIncome=float(df.at[IncomeName,CurrentTerm].replace(',',''))/TermType[CurrentTerm[5:]]*4
    #print(CurrentTerm,CurrentProfit)
    LastIncome=float(df.at[IncomeName,LastTerm].replace(',',''))/TermType[LastTerm[5:]]*4
    return CurrentIncome/LastIncome-1

#获取累计经营现金净额
def GetNetIncomeCashSum(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'cashflow.csv'
    df=pd.read_csv(file,index_col=0).fillna('0')
    sr=df.loc['经营活动产生的现金流量净额']
    ls=[]
    for i in range(len(sr.index)):
        if i>0 and sr.index[i][5:]!='1-3月' and sr.index[i-1][5:]!='度':
            ls.append(float(sr[sr.index[i]].replace(',',''))-float(sr[sr.index[i-1]].replace(',','')))
        else:
            ls.append(float(sr[sr.index[i]].replace(',','')))
    return sum(ls)        

#获取累计投资现金净额
def GetNetInvestmentCashSum(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'cashflow.csv'
    df=pd.read_csv(file,index_col=0).fillna('0')
    sr=df.loc['投资活动产生的现金流量净额']
    ls=[]
    for i in range(len(sr.index)):
        if i>0 and sr.index[i][5:]!='1-3月' and sr.index[i-1][5:]!='度':
            ls.append(float(sr[sr.index[i]].replace(',',''))-float(sr[sr.index[i-1]].replace(',','')))
        else:
            ls.append(float(sr[sr.index[i]].replace(',','')))
    return sum(ls)

#刻度转换
def graduation(OldGraduation):
    if math.isnan(OldGraduation): #判断是否是nan值
        NewGraduation=5
    else:
        if OldGraduation<0:
            NewGraduation=0
        elif OldGraduation<=100:
            NewGraduation=OldGraduation/25
        else:
            NewGraduation=100/25+(OldGraduation-100)/10000
    return NewGraduation

#获取供应链地位
def GetTradePosition(stockcode):
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    df0=pd.read_csv(file,index_col=0).fillna('0')
    df1=df0.loc[['应收票据','应收账款','预付款项','应付票据','应付账款','预收款项']].applymap(ssa.str_to_float)
    #print(df1)
    s_jyxzc=sum(df1[df1.columns[-1]][['应收票据','应收账款','预付款项']])#经营性资产
    #print(s_jyxzc)
    s_jyxfz=sum(df1[df1.columns[-1]][['应付票据','应付账款','预收款项']])#经营性负债
    #print (s_jyxfz)
    return s_jyxfz/s_jyxzc


#从雪球调取主营业务
def GetBusiness(stockcode):
    #stockcode='002456'
    MarketCode={'600':'SH','601':'SH','603':'SH','000':'SZ','002':'SZ','300':'SZ'}
    url='https://xueqiu.com/S/'+MarketCode[stockcode[:3]]+stockcode
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    resp=rq.get(url,headers=headers)
    soup=bs(resp.text,'html.parser')
    return soup.find_all('div',attrs={'class':'widget-content'})[1].string

#主程序的copy，方便选股调用
def GetTotalLevel(stockcode):
    try:
        stockname=ssa.get_stockname(stockcode)
        #print(stockcode,stockname)
        StockPrice=GetStockPrice(stockcode)
        #print('股价：',StockPrice)
        shares=GetShares(stockcode)
        #print('总股本：',shares)
        NetProfit=GetNetProfit(stockcode)
        EPS=NetProfit/shares
        #print('每股收益：',EPS)
        NetProfitGrowth=GetNetProfitGrowth(stockcode)
        #print('净利润增长率：',NetProfitGrowth*100)
        IncomeGrowth=GetIncomeGrowth(stockcode)
        #print('营业收入增长率：',IncomeGrowth*100)
        InterValue=iv(NetProfitGrowth,EPS,0.07,15)
        #print('估值：',InterValue)
        #计算安全边际
        SecurityLevel=graduation(InterValue/StockPrice*100)
        #print('股价安全度：',SecurityLevel)
        #计算成长性
        GrowthLevel=graduation(NetProfitGrowth*100)
        #print('利润成长：',GrowthLevel)
        #计算营业能力
        IncomeLevel=graduation(IncomeGrowth*100)
        #print('营收增长：',IncomeLevel)
        #计算现金能力
        NetIncomeCashSum=GetNetIncomeCashSum(stockcode)
        #print('累计经营现金净额：',NetIncomeCashSum)
        NetInvestmentCashSum=GetNetInvestmentCashSum(stockcode)
        #print('累计投资现金净额：',NetInvestmentCashSum)
        CashLevel=graduation(NetIncomeCashSum/abs(NetInvestmentCashSum)*100)
        #print('运营现金：',CashLevel)
        #计算供应链地位
        TradePosition=GetTradePosition(stockcode)
        TradePositionLevel=graduation(TradePosition*100)
        #print('供应链地位：',TradePositionLevel)
        return stockcode,stockname,SecurityLevel,GrowthLevel,IncomeLevel,CashLevel,TradePositionLevel
    except:
        return None,None,None,None,None,None,None


    
if __name__=='__main__':
    stockcode=input('请输入股票代码：')#'000858'
    stockname=ssa.get_stockname(stockcode)
    print(stockcode,stockname)
    StockPrice=GetStockPrice(stockcode)
    label0='股价：'+str('{:.2f}'.format(StockPrice))+'元'
    print(label0)
    shares=GetShares(stockcode)
    label1='总股本：'+str('{:.2f}'.format(shares/100000000))+'亿'
    print(label1)
    NetProfit=GetNetProfit(stockcode)
    EPS=NetProfit/shares
    label2='每股收益：'+str('{:.2f}'.format(EPS))+'元'
    print(label2)
    NetProfitGrowth=GetNetProfitGrowth(stockcode)
    label3='净利润增长率：'+str('{:.2f}'.format(NetProfitGrowth*100))+'%'
    print(label3)
    IncomeGrowth=GetIncomeGrowth(stockcode)
    label4='营业收入增长率：'+str('{:.2f}'.format(IncomeGrowth*100))+'%'
    print(label4)
    InterValue=iv(NetProfitGrowth,EPS,0.07,15)
    label5='估值：'+str('{:.2f}'.format(InterValue))+'元'
    print(label5)
    #计算安全边际
    SecurityLevel=graduation(InterValue/StockPrice*100)
    #print('股价安全度：',SecurityLevel)
    #计算成长性
    GrowthLevel=graduation(NetProfitGrowth*100)
    #print('利润成长：',GrowthLevel)
    #计算营业能力
    IncomeLevel=graduation(IncomeGrowth*100)
    #print('营收增长：',IncomeLevel)
    #计算现金能力
    NetIncomeCashSum=GetNetIncomeCashSum(stockcode)
    #print('累计经营现金净额：',NetIncomeCashSum)
    NetInvestmentCashSum=GetNetInvestmentCashSum(stockcode)
    #print('累计投资现金净额：',NetInvestmentCashSum)
    CashLevel=graduation(NetIncomeCashSum/abs(NetInvestmentCashSum)*100)
    #print('运营现金：',CashLevel)
    #计算供应链地位
    TradePosition=GetTradePosition(stockcode)
    TradePositionLevel=graduation(TradePosition*100)
    #print('供应链地位：',TradePositionLevel)
    
    

    #雷达图练习


    #标签及数据
    labels=np.array(['营收增长','利润成长','安全边际','运营现金','供应链地位'])
    dataLenth=5
    data=np.array([IncomeLevel,GrowthLevel,SecurityLevel,CashLevel,TradePositionLevel])

    angles=np.linspace(0,2*np.pi,dataLenth,endpoint=False)
    data=np.concatenate((data,[data[0]]))#闭合
    angles=np.concatenate((angles,[angles[0]]))#闭合

    fig=plt.figure()
    ax=fig.add_subplot(111,polar=True) #polar参数很重要！
    ax.plot(angles,data,'bo-',linewidth=2)
    ax.fill(angles,data,facecolor='r',alpha=0.25)
    ax.set_thetagrids(angles*180/np.pi,labels,fontproperties='SimHei')
    ax.set_title(stockname+'-股票雷达图',va='bottom',fontproperties='SimHei')
    ax.set_rlim(0,5)
    ax.grid(True)
    label=label0+'\n'+label1+'\n'+label2+'\n'+label3+'\n'+label4+'\n'+label5
    ax.text(-9.5,5.5,label,verticalalignment="top",horizontalalignment="right")
    fig.canvas.set_window_title(stockname+stockcode)
    plt.show()

