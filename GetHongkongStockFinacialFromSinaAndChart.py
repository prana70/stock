#coding :utf8

import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def AccumulateList(list): #将列表元素依次累计，返回新的列表。注意，要处理的列表必须是数字的！！！
        list_return=[]
        new_value=0
        for ele in list:
                new_value+=ele
                list_return.append(new_value)
        return list_return



headers_string='''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Connection: keep-alive
Cookie: name=sinaAds; page=23333; post=massage; NowDate=Tue Jan 05 2021 21:22:00 GMT+0800; SINAGLOBAL=223.87.206.16_1562114457.622019; U_TRS1=00000010.7dd32ec75.5d1bf99a.93b25189; vjuids=-107c09220.16bcce450f0.0.decafdd774db8; vjlast=1562510643; SGUID=1562510648574_45952354; lxlrttp=1578733570; SCF=AvgysSyB5iE0EOBhbTWVSE87yhrGIkl3rwfEjuKUzJouvg47bIqcQ-uam3l-ch1CFNg3mCqgf1-QpF2BjgiJZwc.; sso_info=v02m6alo5qztKWRk5iljpSMpY6DpKWRk5iljoOQpY6UmK2LkpWFjZKUuJGClYKMspWFjZKUuJGilLmMkpm1mpaQvY2jiLSNk5i5jLOgt4yAwMA=; _ga=GA1.3.1062711943.1592923555; UOR=,,; UM_distinctid=173ddeaca9e118-060f8eb1e3b82e-3323765-144000-173ddeaca9fb76; __gads=ID=5e6cbbb21b1fc024-2228e9ba7ac4006e:T=1604123205:RT=1604123205:S=ALNI_MZNZPunGtPOy0rRzMFJ-br_vdCYiQ; FINA_V_S_2=sz002555,sz300770,sz002001,sh601360,sh603393,sz000895,sz300498,sz002714,sz000661,sz002195,sz002294,sz002382,sh600887,sz000651,sh600867,sh600438,sh601658,sz000790,sh601003,sh600782; SR_SEL=1_511; hk_visited_stocks=01810; Apache=183.220.95.81_1609852452.72159; ULV=1609852454320:123:9:6:183.220.95.81_1609852452.72159:1609852450122; rotatecount=2; U_TRS2=00000051.ab177708.5ff46627.22e30c45; STOCK7-FINANCE-SINA-COM-CN=; sinaH5EtagStatus=y; visited_uss=gb_xiacy%7Cgb_mcd%7Cgb_cost%7Cgb_fb%7Cgb_twtr%7Cgb_brk.a%7Cgb_tsla%7Cgb_goog%7Cgb_aapl%7Cgb_jd%7Cgb_baba%7Cgb_xpev%7Cgb_nio%7Cgb_kc%7Cgb_snow; hqEtagMode=1; FIN_ALL_VISITED=01810%2Cxiacy%2Cmcd%2Ccost%2Cfb%2Ctwtr%2Cbrk.a%2Ctsla%2Cgoog%2Caapl%2Cjd%2Cbaba%2Cxpev%2Cnio%2Ckc%2Csnow
Host: stock.finance.sina.com.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
'''
headers={}
for item in headers_string.strip().split('\n'):
    index_=item.find(':',1)
    headers[item[:index_]]=item[index_+1:].strip()

stock_code=input('请输入港股代码：') #'01810'

url='http://stock.finance.sina.com.cn/hkstock/finance/%s.html'%stock_code

resp=rq.get(url,headers=headers)
soup=bs(resp.text,'lxml')

dfs=pd.read_html(soup.select('body > div.wrap > div:nth-child(19) > div > div.sub01_cc > div > table')[0].prettify(),header=0,index_col=0)
df_balance=dfs[0].drop(['报表类型','币种'],axis=0).fillna(0).replace('--',0).applymap(lambda x: float(x)*10**6)
df_balance.sort_index(axis=1,inplace=True)

xticks=df_balance.columns
y_cos=np.arange(len(df_balance.columns))

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

assets_total=[x/10**8 for x in df_balance.loc['总资产']]
stock_holders_equity=[x/10**8 for x in df_balance.loc['股东权益/(亏损)']]

fig1=plt.figure()
plt.bar(y_cos,assets_total,align='center',color='r',alpha=0.5,label='总资产')
for x,y in zip(y_cos,assets_total):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points',ha='center')
plt.bar(y_cos,stock_holders_equity,align='center',color='g',alpha=0.5,label='净资产')
for x,y in zip(y_cos,stock_holders_equity):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points',ha='center')
plt.xticks(y_cos,xticks,rotation=30)
plt.title('%s资产负债总览'%stock_code)
plt.legend()
plt.ylabel('亿港元')

dfs=pd.read_html(soup.select('body > div.wrap > div:nth-child(23) > div > div.sub01_cc > div > table')[0].prettify(),header=0,index_col=0)
df_income=dfs[0].drop(['报表类型','币种'],axis=0).fillna(0).replace('--',0).applymap(lambda x: float(x)*10**6)
df_income.sort_index(axis=1,inplace=True)

for ele in df_income.columns:
    if ele[5:10]=='03-31':
        df_income[ele]=df_income[ele]*4
    if ele[5:10]=='06-30':
        df_income[ele]=df_income[ele]*2
    if ele[5:10]=='09-30':
        df_income[ele]=df_income[ele]*4/3

xticks=df_income.columns
y_cos=np.arange(len(df_income.columns))


income_total=[x/10**8 for x in df_income.loc['营业额']]
profit_gross=[x/10**8 for x in df_income.loc['毛利']]
profit=[x/10**8 for x in df_income.loc['除税后盈利/(亏损)']]

fig2=plt.figure()
plt.plot(y_cos,income_total,color='r',alpha=0.5,label='营业额')
for x,y in zip(y_cos,income_total):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points')
plt.plot(y_cos,profit_gross,color='b',alpha=0.5,label='毛利')
for x,y in zip(y_cos,profit_gross):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points')
plt.plot(y_cos,profit,color='g',alpha=0.5,label='净利润')
for x,y in zip(y_cos,profit):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points')
plt.xticks(y_cos,xticks,rotation=30)
plt.title('%s营收总览'%stock_code)
plt.legend()
plt.ylabel('亿港元')

dfs=pd.read_html(soup.select('body > div.wrap > div:nth-child(21) > div > div.sub01_cc > div > table')[0].prettify(),header=0,index_col=0)
df_cash=dfs[0].drop(['报表类型','币种'],axis=0).fillna(0).replace('--',0).applymap(lambda x: float(x)*10**6)
df_cash.sort_index(axis=1,inplace=True)

for ele in df_cash.columns:
    if ele[5:10]=='12-31':
        df_cash[ele]=df_cash[ele]/4
    if ele[5:10]=='06-30':
        df_cash[ele]=df_cash[ele]/2
    if ele[5:10]=='09-30':
        df_cash[ele]=df_cash[ele]/3

xticks=df_cash.columns
y_cos=np.arange(len(df_cash.columns))


cash_operate=[x/10**8 for x in AccumulateList(df_cash.loc['经营业务所得之现金流入净额'])]
cash_invest=[x/10**8 for x in AccumulateList(df_cash.loc['投资活动之现金流入净额'])]
cash_finacial=[x/10**8 for x in AccumulateList(df_cash.loc['融资活动之现金流入净额'])]

fig3=plt.figure()
bar_width=0.3
plt.bar(y_cos,cash_operate,bar_width,color='r',align='center',alpha=0.5,label='经营现金流')
for x,y in zip(y_cos,cash_operate):
    plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points')
plt.bar(y_cos+bar_width,cash_invest,bar_width,align='center',color='b',alpha=0.5,label='投资现金流')
plt.bar(y_cos+bar_width*2,cash_finacial,bar_width,align='center',color='g',alpha=0.5,label='融资现金流')
plt.xticks(y_cos,xticks,rotation=30)
plt.title('%s累计现金流总览'%stock_code)
plt.legend()
plt.ylabel('亿港元')









plt.show()
