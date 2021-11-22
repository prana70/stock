#coding:utf8

import pandas as pd
import os
import datetime


def get_balancesheet(stock_code):
    #因为网站按年份提供当年四季的财报，因此需要确定要爬取网页的年份列表，初始列表为当前年分至2007年（注：2016年不会处理）
    years={}
    for year in range(datetime.datetime.now().year,2006,-1):
        years[str(year)]=[str(year)+'-03-31',str(year)+'-06-30',str(year)+'-09-30',str(year)+'-12-31']
    #如果存在已有的数据文件，则应当将已有数据年份（四季报表都齐全）从初始年份列表中剔除
    file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'balancesheet.csv'
    if os.path.exists(file):
        df_base=pd.read_csv(file,index_col=0)
        for year in years.copy():
            if set(years[year])<=set(df_base.columns):
                del(years[year])
    #根据年份列表，爬取网页，读入df,dfs为数个df的列表
    dfs=[]
    if not years is None:
        for year in years.keys():
            try:
                url='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/'+stock_code+'/ctrl/'+year+'/displaytype/4.phtml'
                df=pd.read_html(url,header=1,index_col=0,attrs={'id':'BalanceSheetNewTable0'})[0]
                #因为爬出的数据有异常列，故根据特征构造删除列表，并从数据中删除。
                drop_columns=[]
                for column in df.columns:
                    if 'Unnamed' in column:
                        drop_columns.append(column)
                if len(drop_columns)>0:
                    df.drop(columns=drop_columns,inplace=True)
                #将数据中的‘--’转为‘0.00’
                #df.dropna(axis=0,inplace=True)
                df.replace('--','0.00',inplace=True)
                #用to_numeric()将数据中非数字转为nan值（数字转为float64）,删除带nan值的行
                for column in df.columns:
                    df[column]=pd.to_numeric(df[column],errors='coerce')
                df.dropna(axis=0,inplace=True)
                dfs.append(df)
            except:
                with open('get_balancesheet_log.txt','a') as f:
                    print(stock_code,year,'balancesheet数据获取失败！url:',url)
                    f.write(str(datetime.datetime.now()))
                    f.write(' | '+stock_code+' '+year+' '+'balancesheet数据获取失败！url:'+url+'\n')
    #如果爬取到数据，则合成一个df
    if len(dfs)>1:
        df=dfs[0].join(dfs[1:])
    elif len(dfs)==1:
        df=dfs[0]
    elif len(dfs)==0:
        df=None

    if not df is None:
        #如果已有数据文件，则将已有数据与爬取数据合表到一个df,并将列按升序重排
        if os.path.exists(file):
            df_base=pd.read_csv(file,index_col=0)
            drop_columns=[]
            for column in df.columns:
                if column in df_base.columns:
                    drop_columns.append(column)
            if len(drop_columns)>0:
                df.drop(columns=drop_columns,inplace=True)
            df=df_base.join(df)
            
        columns=list(df.columns)
        columns.sort()
        df=df.reindex(columns=columns)
        file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'balancesheet.csv'
        print(file)
        print('*'*50)
        print('写入',stock_code,'资产负债表文件......')
        df.to_csv(file)
        print('写入成功！')
    
def get_profitstatement(stock_code):
    #因为网站按年份提供当年四季的财报，因此需要确定要爬取网页的年份列表，初始列表为当前年分至2007年（注：2016年不会处理）
    years={}
    for year in range(datetime.datetime.now().year,2006,-1):
        years[str(year)]=[str(year)+'-03-31',str(year)+'-06-30',str(year)+'-09-30',str(year)+'-12-31']
    #如果存在已有的数据文件，则应当将已有数据年份（四季报表都齐全）从初始年份列表中剔除
    file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'profitstatement.csv'
    if os.path.exists(file):
        df_base=pd.read_csv(file,index_col=0)
        for year in years.copy():
            if set(years[year])<=set(df_base.columns):
                del(years[year])
    #根据年份列表，爬取网页，读入df,dfs为数个df的列表
    dfs=[]
    if not years is None:
        for year in years.keys():
            try:
                url='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/'+stock_code+'/ctrl/'+year+'/displaytype/4.phtml'
                df=pd.read_html(url,header=1,index_col=0,attrs={'id':'ProfitStatementNewTable0'})[0]
                #因为爬出的数据有异常列，故根据特征构造删除列表，并从数据中删除。
                drop_columns=[]
                for column in df.columns:
                    if 'Unnamed' in column:
                        drop_columns.append(column)
                if len(drop_columns)>0:
                    df.drop(columns=drop_columns,inplace=True)
                #将数据中的‘--’转为‘0.00’
                #df.dropna(axis=0,inplace=True)
                df.replace('--','0.00',inplace=True)
                #用to_numeric()将数据中非数字转为nan值（数字转为float64）,删除带nan值的行
                for column in df.columns:
                    df[column]=pd.to_numeric(df[column],errors='coerce')
                df.dropna(axis=0,inplace=True)
                dfs.append(df)
            except:
                with open('get_profitstatement_log.txt','a') as f:
                    print(stock_code,year,'profitstatement数据获取失败！url:',url)
                    f.write(str(datetime.datetime.now()))
                    f.write(' | '+stock_code+' '+year+' '+'profitstatement数据获取失败！url:'+url+'\n')
    #如果爬取到数据，则合成一个df
    if len(dfs)>1:
        df=dfs[0].join(dfs[1:])
    elif len(dfs)==1:
        df=dfs[0]
    elif len(dfs)==0:
        df=None

    if not df is None:
        #如果已有数据文件，则将已有数据与爬取数据合表到一个df,并将列按升序重排
        if os.path.exists(file):
            df_base=pd.read_csv(file,index_col=0)
            drop_columns=[]
            for column in df.columns:
                if column in df_base.columns:
                    drop_columns.append(column)
            if len(drop_columns)>0:
                df.drop(columns=drop_columns,inplace=True)
            df=df_base.join(df)
            
        columns=list(df.columns)
        columns.sort()
        df=df.reindex(columns=columns)
        file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'profitstatement.csv'
        print(file)
        print('*'*50)
        print('写入',stock_code,'利润表文件......')
        df.to_csv(file)
        print('写入成功！')


#url='http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/000651/ctrl/part/displaytype/4.phtml'
#dfs=pd.read_html(url,header=1,index_col=0,attrs={'id':'ProfitStatementNewTable0'})

def get_cashflow(stock_code):
    #因为网站按年份提供当年四季的财报，因此需要确定要爬取网页的年份列表，初始列表为当前年分至2007年（注：2016年不会处理）
    years={}
    for year in range(datetime.datetime.now().year,2006,-1):
        years[str(year)]=[str(year)+'-03-31',str(year)+'-06-30',str(year)+'-09-30',str(year)+'-12-31']
    #如果存在已有的数据文件，则应当将已有数据年份（四季报表都齐全）从初始年份列表中剔除
    file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'cashflow.csv'
    if os.path.exists(file):
        df_base=pd.read_csv(file,index_col=0)
        for year in years.copy():
            if set(years[year])<=set(df_base.columns):
                del(years[year])
    #根据年份列表，爬取网页，读入df,dfs为数个df的列表
    dfs=[]
    if not years is None:
        for year in years.keys():
            try:
                url='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/'+stock_code+'/ctrl/'+year+'/displaytype/4.phtml'
                df=pd.read_html(url,header=1,index_col=0,attrs={'id':'ProfitStatementNewTable0'})[0]
                #因为爬出的数据有异常列，故根据特征构造删除列表，并从数据中删除。
                drop_columns=[]
                for column in df.columns:
                    if 'Unnamed' in column:
                        drop_columns.append(column)
                if len(drop_columns)>0:
                    df.drop(columns=drop_columns,inplace=True)
                #将数据中的‘--’转为‘0.00’
                #df.dropna(axis=0,inplace=True)
                df.replace('--','0.00',inplace=True)
                #用to_numeric()将数据中非数字转为nan值（数字转为float64）,删除带nan值的行
                for column in df.columns:
                    df[column]=pd.to_numeric(df[column],errors='coerce')
                df.dropna(axis=0,inplace=True)
                df=df[~df.index.duplicated()] #证券类或保险类公司的现金流量表中“经营活动中产生的现金流量净额”有重复行，去除
                dfs.append(df)
            except:
                with open('get_cashflow_log.txt','a') as f:
                    print(stock_code,year,'cashflow数据获取失败！url:',url)
                    f.write(str(datetime.datetime.now()))
                    f.write(' | '+stock_code+' '+year+' '+'cashflow数据获取失败！url:'+url+'\n')
    #如果爬取到数据，则合成一个df
    if len(dfs)>1:
        df=dfs[0].join(dfs[1:])
    elif len(dfs)==1:
        df=dfs[0]
    elif len(dfs)==0:
        df=None
    #print(df)
    if not df is None:
        #如果已有数据文件，则将已有数据与爬取数据合表到一个df,并将列按升序重排
        if os.path.exists(file):
            df_base=pd.read_csv(file,index_col=0)
            drop_columns=[]
            for column in df.columns:
                if column in df_base.columns:
                    drop_columns.append(column)
            if len(drop_columns)>0:
                df.drop(columns=drop_columns,inplace=True)
            df=df_base.join(df)
            
        columns=list(df.columns)
        columns.sort()
        df=df.reindex(columns=columns)
        
        file=os.getcwd()+'\\stock_financial_sina\\'+stock_code+'cashflow.csv'
        print(file)
        print('*'*50)
        print('写入',stock_code,'现金流量表文件......')
        df.to_csv(file)
        print('写入成功！')



if __name__=='__main__':
    df=pd.read_csv(os.getcwd()+'\\market_data\\stock_list.csv',converters={'股票代码':str})
    i=0
    for stock_code in df['股票代码']:
        print(i,stock_code)
        if i==2:
            break
        i+=1
        get_balancesheet(stock_code)
        get_profitstatement(stock_code)
        get_cashflow(stock_code)
    
    
