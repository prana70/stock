#coding:utf8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
import os


def get_financial_data_from_sina(stock_code):

    #从浏览器中复制出request headers字符串，将其转换成字典
    headers_string='''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Cache-Control: max-age=0
Cookie: SINAGLOBAL=223.87.206.16_1562114457.622019; U_TRS1=00000010.7dd32ec75.5d1bf99a.93b25189; vjuids=-107c09220.16bcce450f0.0.decafdd774db8; vjlast=1562510643; SGUID=1562510648574_45952354; SCF=AvgysSyB5iE0EOBhbTWVSE87yhrGIkl3rwfEjuKUzJouvg47bIqcQ-uam3l-ch1CFNg3mCqgf1-QpF2BjgiJZwc.; sso_info=v02m6alo5qztKWRk5iljpSMpY6DpKWRk5iljoOQpY6UmK2LkpWFjZKUuJGClYKMspWFjZKUuJGilLmMkpm1mpaQvY2jiLSNk5i5jLOgt4yAwMA=; _ga=GA1.3.1062711943.1592923555; UOR=,,; gatheruuid=162867963rr157g9; newgatheruuid=162867963rr157g9; refer_domain=bing.com; UM_distinctid=17b830711d27a3-0b8920fe0996ce-c343365-144000-17b830711d3c22; __utma=269849203.1062711943.1592923555.1637139387.1637139387.1; __utmz=269849203.1637139387.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ULV=1641007002287:172:1:1::1637459130223; MONEY-FINANCE-SINA-COM-CN-WEB5=; hqEtagMode=0; SFA_version=2021-08-02%2009%3A00; directAd_samsung=true; close_farmgamepop=1; directAd_dell_fidx=true; U_TRS2=000000ec.833edcf.61e290dd.b1e21bc6; FIN_ALL_VISITED=sh600398; FINA_V_S_2=sh600398,sh601360,sz000895,sh600519,sz002507,sh603816,sh600585,sh601003,sh600875,sh603866,sz003816,sh600782,sh688513,sz000858,sh600260,sz000338,sh600867,sh601318,sh603393,sz300146; _s_upa=3
Host: vip.stock.finance.sina.com.cn
If-Modified-Since: Sat, 15 Jan 2022 09:16:40 GMT
Proxy-Connection: keep-alive
Referer: https://finance.sina.com.cn/realstock/company/sh600398/nc.shtml
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36
'''
    headers=dict(line.split(': ',1) for line in headers_string.strip().split('\n'))




    report_types=['BalanceSheet','ProfitStatement','CashFlow']
    table_names={
        'BalanceSheet':'BalanceSheet',
        'ProfitStatement':'ProfitStatement',
        'CashFlow':'ProfitStatement'
        }
    file_names={
        'BalanceSheet':'balancesheet',
        'ProfitStatement':'profitstatement',
        'CashFlow':'cashflow'
        }

    for report_type in report_types:
        url='http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_%s/stockid/%s/ctrl/part/displaytype/4.phtml'%(report_type,stock_code)
        resp=rq.get(url,headers=headers)
        soup=bs(resp.text,'lxml')
        hrefs=[financial_year['href'] for financial_year in soup.select('#con02-1 > table:nth-child(1)')[0].find_all('a')]
        dfs=[]
        for href in hrefs:
            print(href)
            try:
                df=pd.read_html(rq.get(href,headers=headers).text,header=1,index_col=0,attrs={'id':'%sNewTable0'%table_names[report_type]})[0]
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

        file=os.getcwd()+'\\stock_financial_sina\\%s%s.csv'%(stock_code,file_names[report_type])

        if not df is None:
            #如果已有数据文件，则将已有数据与爬取数据合表到一个df,并将列按升序重排
            if os.path.exists(file):
                print('已有文件，添加写入！！！')
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
            print('*'*50)
            print('写入%s'%file)
            df.to_csv(file)
            print('写入成功！')
if __name__=='__main__':
    stock_code=input('请输入股票代码：')
    get_financial_data_from_sina(stock_code)
