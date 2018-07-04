import pandas as pd
import os

def GetHkStockFinancial(StockCode):
    FilePath=os.getcwd()+'\\HkStockFinancial\\'
    if os.path.exists(FilePath+StockCode+'Balance.csv') and os.path.exists(FilePath+StockCode+'Cashflow.csv') and os.path.exists(FilePath+StockCode+'Income.csv'):
        #将港股的三大财务报表合成一个表，并将列的顺序调整为升序。
        df1=pd.read_csv(FilePath+StockCode+'Balance.csv',index_col=0)
        df2=pd.read_csv(FilePath+StockCode+'Cashflow.csv',index_col=0)
        df3=pd.read_csv(FilePath+StockCode+'Income.csv',index_col=0)
        df4=pd.concat([df1,df2,df3])
        df=df4.reindex_axis(sorted(df4.columns),axis=1)

        #提取报表日期、总资产、净资产
        Terms=list(df.columns)
        #print(Terms)
        TotalAsset=list(df.loc['总资产'].fillna('0').astype(float)/100)
        #print(TotalAsset)
        NetAsset=list(df.loc['净资产/(负债)'].fillna('0').astype(float)/100)
        #print(NetAsset)

        return df,Terms,TotalAsset,NetAsset
    else:
        return None,None,None,None

if __name__=='__main__':
    StockCode='01751' #input('请输入港股代码：')
    df, Terms, TotalAsset, NetAsset=GetHkStockFinancial(StockCode)