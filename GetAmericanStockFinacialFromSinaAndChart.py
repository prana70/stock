#coding:utf8

import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
import json
import re

import matplotlib.pyplot as plt
import numpy as np



def DataConvert(raw_data): #根据数据后面的单位，将数据转换成“元”的数值
        clean_data=raw_data.replace(',','')
        reg=re.compile(r'(^\-?\d+.\d*)(\w*)')

        unit_mult={'亿':10**8,'万':10**4,'千':10**3,'百':10**2}

        reg_match=reg.match(clean_data)
        
        if reg_match:
                if len(reg_match.group(2))>0:
                        clean_data=float(reg_match.group(1))*unit_mult[reg_match.group(2)]
                else:
                        clean_data=float(reg_match.group(1))
        else:
                clean_data=0
                
        return clean_data

def FindListDuplicate(list): #查找列表中的重项，并返回重复项列表
        list1=[x[:10] for x in list]
        list2=set(list1)
        duplicate_list=[]
        for ele in list2:
                if list1.count(ele)>1:
                        duplicate_list.append(ele)
        return duplicate_list

def AccumulateList(list): #将列表元素依次累计，返回新的列表。注意，要处理的列表必须是数字的！！！
        list_return=[]
        new_value=0
        for ele in list:
                new_value+=ele
                list_return.append(new_value)
        return list_return

        

header_string='''
:authority: quotes.sina.com.cn
:method: GET
:path: /usstock/hq/income.php?s=tsla
:scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
cookie: SINAGLOBAL=223.87.206.16_1562114457.622019; U_TRS1=00000010.7dd32ec75.5d1bf99a.93b25189; vjuids=-107c09220.16bcce450f0.0.decafdd774db8; vjlast=1562510643; SGUID=1562510648574_45952354; lxlrttp=1578733570; SCF=AvgysSyB5iE0EOBhbTWVSE87yhrGIkl3rwfEjuKUzJouvg47bIqcQ-uam3l-ch1CFNg3mCqgf1-QpF2BjgiJZwc.; sso_info=v02m6alo5qztKWRk5iljpSMpY6DpKWRk5iljoOQpY6UmK2LkpWFjZKUuJGClYKMspWFjZKUuJGilLmMkpm1mpaQvY2jiLSNk5i5jLOgt4yAwMA=; _ga=GA1.3.1062711943.1592923555; UOR=,,; UM_distinctid=173ddeaca9e118-060f8eb1e3b82e-3323765-144000-173ddeaca9fb76; __gads=ID=5e6cbbb21b1fc024-2228e9ba7ac4006e:T=1604123205:RT=1604123205:S=ALNI_MZNZPunGtPOy0rRzMFJ-br_vdCYiQ; Apache=183.220.95.0_1608623800.85645; rotatecount=3; ULV=1608623802470:111:6:4:183.220.95.0_1608623800.85645:1608623798739; U_TRS2=00000000.dd286e17.5fe1a6bb.a6cba9a1; hqEtagMode=1; QUOTES-SINA-CN=
referer: https://quotes.sina.com.cn/usstock/hq/balance.php?s=tsla
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
'''
headers={}
for item in header_string.strip().split('\n'):
        index_=item.find(':',1)
        headers[item[:index_].strip(':')]=item[index_+1:].strip()

stock_code=input('请输入美股的代码：') #'docu'

#try:
terms=['annual','quarter']
report_types=['balance','income','cash']

for report_type in report_types:
        df_list=[]
        for term in terms:
                url='https://quotes.sina.com.cn/usstock/hq/{}.php?s={}&t={}'.format(report_type,stock_code,term)

                resp=rq.get(url,headers=headers)
                soup=bs(resp.text,'lxml')

                dfs=pd.read_html(soup.select('body > div.wrap > div.news.keyratios > div.tbl_wrap > table.data_tbl.os_tbl')[1].prettify(),header=0,index_col=0)
                df=dfs[0].fillna('').applymap(DataConvert)
                df.set_axis([x[1:]+term for x in df.columns],axis='columns',inplace=True) #更改列名
                df_list.append(df)
        locals()['df_%s'%report_type]=pd.concat(df_list,axis=1) #将季度和年度数据合成一个表。
        if report_type=='balance' or report_type=='income':
                locals()['df_%s'%report_type].drop([x+'quarter'for x in FindListDuplicate(list(locals()['df_%s'%report_type].columns))],axis=1,inplace=True)#如果重复，删除重复的季度数据
        else:
                locals()['df_%s'%report_type].drop([x+'annual'for x in FindListDuplicate(list(locals()['df_%s'%report_type].columns))],axis=1,inplace=True)#如果重复，删除重复的年度数据
        if report_type=='income': #将利润表的季度数据调整成年度数据
                for ele in locals()['df_%s'%report_type].columns:
                        if ele[10:]=='quarter':
                              locals()['df_%s'%report_type][ele]=locals()['df_%s'%report_type][ele]*4
                                
        if report_type=='cash': #将现金流量表年度数据调整为季度数据
                for ele in locals()['df_%s'%report_type].columns:
                        if ele[5:10]=='06-30' and ele[10:]=='annual':
                                locals()['df_%s'%report_type][ele]=locals()['df_%s'%report_type][ele]/2
                        if ele[5:10]=='09-30' and ele[10:]=='annual':
                                locals()['df_%s'%report_type][ele]=locals()['df_%s'%report_type][ele]/3
                        if ele[5:10]=='12-31' and ele[10:]=='annual':
                                locals()['df_%s'%report_type][ele]=locals()['df_%s'%report_type][ele]/4
        locals()['df_%s'%report_type].columns=[x[:10] for x in locals()['df_%s'%report_type].columns]
#except:
#        print('没有查询到代码为{}的股票或者调取数据失败！'.format(stock_code))
#        
print('*'*50)
print('将三个财务报表合成一个表......')
df_total=pd.concat([df_balance,df_income,df_cash],axis=0,sort=True).fillna(0) #将三个表合成一个表,并将因三个表不一致而添加的列的空值初始成0
#df_total.sort_index(axis=1,inplace=True) #按列进行排序,因为在concat时，设置sort=True，已进行了排序，因此，此条语句已不需要

xticks=df_total.columns
y_pos=np.arange(len(xticks))

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


assets_total=[x/10**8 for x in df_total.loc['合计总资产']]
stock_holders_equity=[x/10**8 for x in df_total.loc['股东权益合计']]
fig1=plt.figure()
plt.bar(y_pos,assets_total,align='center',alpha=0.5,color='r',label='总资产')
for x,y in zip(y_pos,assets_total): #标注合计总资产
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points',ha='center')
plt.bar(y_pos,stock_holders_equity,align='center',alpha=0.5,color='g',label='净资产')
for x,y in zip(y_pos,stock_holders_equity): #标注股东权益合计
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points',ha='center')
plt.xticks(y_pos,xticks,rotation=30)
plt.ylabel('亿美元')
plt.title('%s的资产负债总览'%stock_code)
plt.grid()
plt.legend()

income_total=[x/10**8 for x in df_total.loc['营业总收入']]
profit_gross=[x/10**8 for x in df_total.loc['毛利']]
profit_before_interest=[x/10**8 for x in df_total.loc['计息税前利润']]
profit_before_tax=[x/10**8 for x in df_total.loc['税前净利润']]
profit=[x/10**8 for x in df_total.loc['净利润']]
fig2=plt.figure()
plt.plot(y_pos,income_total,alpha=0.5,color='r',label='营业总收入')
for x,y in zip(y_pos,income_total): #标注营业收入
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(-13,5),textcoords='offset points')
plt.plot(y_pos,profit_gross,alpha=0.5,color='g',label='毛利')
plt.plot(y_pos,profit_before_interest,alpha=0.5,color='c',label='计息税前利润')
#plt.plot(y_pos,profit_before_tax,alpha=0.5,color='y',label='税前净利润')
plt.plot(y_pos,profit,alpha=0.5,color='b',label='净利润')
for x,y in zip(y_pos,profit): #标注营业收入
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(-13,5),textcoords='offset points')
plt.xticks(y_pos,xticks,rotation=30)
plt.ylabel('亿美元')
plt.title('%s的营收总览'%stock_code)
plt.grid()
plt.legend()

cash_operate=[x/10**8 for x in AccumulateList(df_total.loc['经营现金流'])]
cash_invest=[x/10**8 for x in AccumulateList(df_total.loc['投资现金流'])]
cash_finacial=[x/10**8 for x in AccumulateList(df_total.loc['筹资现金流'])]
cash_free=[x/10**8 for x in AccumulateList(df_total.loc['自由现金流'])]
fig3=plt.figure()
bar_width=0.24
plt.bar(y_pos,cash_operate,bar_width,align='center',alpha=0.7,color='r',label='经营现金流')
for x,y in zip(y_pos,cash_operate): #标注经营现金流
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(0,3),textcoords='offset points',ha='center')
plt.bar(y_pos+2*bar_width,cash_invest,bar_width,align='center',alpha=0.7,color='b',label='投资现金流')
plt.bar(y_pos+3*bar_width,cash_finacial,bar_width,align='center',alpha=0.7,color='c',label='筹资现金流')
plt.bar(y_pos+bar_width,cash_free,bar_width,align='center',alpha=0.7,color='g',label='自由现金流')
for x,y in zip(y_pos,cash_free):
        plt.annotate('%s'%format(y,'0,.2f'),xy=(x,y),xytext=(10+bar_width,3),textcoords='offset points')
plt.xticks(y_pos,xticks,rotation=30)
plt.ylabel('亿美元')
plt.title('%s的累计现金流总览'%stock_code)
plt.grid()
plt.legend()

plt.show()

