import pandas as pd
import os


def GetHkStockFinancialFromXueqiu(StockCode):
    url='http://stock.finance.sina.com.cn/hkstock/finance/'+StockCode+'.html'
    #url='http://www.cninfo.com.cn/information/companyinfo_n.html?financialreport?szcn300400'
    dfs=pd.read_html(url,header=0,index_col=0)
    if len(dfs)>=4:
        print('  写入资产负债表....')
        df1=dfs[1]
        df1.to_csv(os.getcwd()+'\\HkStockFinancial\\'+StockCode+'Balance.csv',encoding='utf8')
        print('  成功！')
        print('  写入现金流量表...')
        df2=dfs[2]
        df2.to_csv(os.getcwd()+'\\HkStockFinancial\\'+StockCode+'Cashflow.csv',encoding='utf8')
        print('  成功！')
        print('  写入损益表...')
        df3=dfs[3]
        df3.to_csv(os.getcwd()+'\\HkStockFinancial\\'+StockCode+'Income.csv',encoding='utf8')
        print('  成功！')
    else:
        print('调取页面可能不包含想爬取的数据，请核查！')

if __name__=='__main__':
    #df=pd.read_csv(os.getcwd()+'\\market_data\\HkStockList.csv')
    #StockCodeList=df['股票代码']
    StockCode=input('请输入股票代码：')
    try:
        GetHkStockFinancialFromXueqiu(StockCode)
    except:
        f = open(os.getcwd() + '\\HkStockFinancial\error.txt', 'a')
        f.write(str(i) + ' ' + StockCode + '\n')
        f.close()

    '''    
    i=0
    for StockCode in StockCodeList:
        i=i+1
        print(i,StockCode)
        try:
            GetHkStockFinancialFromXueqiu(StockCode)
        except:
            f=open(os.getcwd()+'\\HkStockFinancial\error.txt','a')
            f.write(str(i)+' '+StockCode+'\n')
            f.close()

    print(i,'只股票数据已获取并存入本地硬盘！')
    '''


