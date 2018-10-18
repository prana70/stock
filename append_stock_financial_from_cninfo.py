# coding:utf8

from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import os
import requests as rq
from datetime import datetime


def GetEndPeriod():
    today = datetime.now().strftime('%Y-%m-%d')
    # print('today is',today)
    period0 = str(int(today[:4]) - 1) + '-12-31'
    period1 = today[:4] + '-03-31'
    period2 = today[:4] + '-06-30'
    period3 = today[:4] + '-09-30'
    EndPeriod = today
    periods = [period0, period1, period2, period3]
    for period in periods:
        if today > period:
            EndPeriod = period
    # print('EndPeriod is',EndPeriod)
    return EndPeriod

# 调取指定巨潮信息网页的数据，调取成功则整理加入一个dataframe返回，不成功返回None.
def get_dataframe(url):
    try:
        hd = {'User-Agent': 'Mozilla/5.0'}
        resp = rq.post(url, headers=hd, timeout=9)
        soup = bs(resp.text, 'html.parser')
        main_div = soup.find('div', class_='clear')
        if 'balancesheet' in url:
            sub_tags = main_div.find_all('div')
        else:
            sub_tags = main_div.find_all('td')
        item = []
        data = []
        i = 0
        for sub_tag in sub_tags:
            if i > 1:
                if i % 2 == 0:
                    item.append(sub_tag.string.strip())
                else:
                    data.append(sub_tag.string.strip())
            i += 1
        dataset = list(zip(item, data))
        df = pd.DataFrame(data=dataset)
        df.to_csv('ls.csv', index=False, header=False, encoding='utf8')
        new_df = pd.read_csv('ls.csv')
        os.remove('ls.csv')
        return new_df
    except:
        return None



def append_stock_financial(file):
    df1 = pd.read_csv(os.getcwd() + '\stock_financial\\' + file)
    stockcode = file[0:6]
    end_period = GetEndPeriod()
    # 获取应添加的下一期的年月日
    if 'balancesheet' in file:
        if '-12-31' in df1.columns[-1]:
            yyyy = str(int(df1.columns[-1][0:4]) + 1)
            mm = '-03-31'
        elif '-03-31' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-06-30'
        elif '-06-30' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-09-30'
        else:
            yyyy = df1.columns[-1][0:4]
            mm = '-12-31'
        start_period = yyyy + mm
        cwzb = 'balancesheet'
    elif 'incomestatements' in file:
        if '年度' in df1.columns[-1]:
            yyyy = str(int(df1.columns[-1][0:4]) + 1)
            mm = '-03-31'
        elif '1-3月' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-06-30'
        elif '1-6月' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-09-30'
        else:
            yyyy = df1.columns[-1][0:4]
            mm = '-12-31'
        start_period = yyyy + mm
        cwzb = 'incomestatements'
    else:
        if '年度' in df1.columns[-1]:
            yyyy = str(int(df1.columns[-1][0:4]) + 1)
            mm = '-03-31'
        elif '1-3月' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-06-30'
        elif '1-6月' in df1.columns[-1]:
            yyyy = df1.columns[-1][0:4]
            mm = '-09-30'
        else:
            yyyy = df1.columns[-1][0:4]
            mm = '-12-31'
        start_period = yyyy + mm
        cwzb = 'cashflow'
    print('本地数据截止：', df1.columns[-1], cwzb)
    print('拟添加：', start_period, cwzb)
    if start_period <= end_period and start_period >= '2016-03-31':  # 如果应添加的下一期小于或等于截止期，大于等于'2016-03-31'，则添加数据
        url = 'http://www.cninfo.com.cn/information/stock/' + cwzb + '_.jsp?stockCode=' + stockcode + '&yyyy=' + str(
            yyyy) + '&mm=' + mm
        print(url)
        df2 = get_dataframe(url)
        if type(df2) != type(None):
            df3 = pd.merge(df1, df2)
            df3.to_csv(os.getcwd() + '\stock_financial\\' + file, encoding='utf8', index=False)
            print('添加数据成功！')
            return 1
        else:
            url = 'http://www.cninfo.com.cn/information/stock/' + cwzb + '_.jsp?stockCode=' + stockcode
            print(url)
            df2 = get_dataframe(url)
            if type(df2) != type(None):
                if cwzb == 'balancesheet':
                    current_period = df2.columns[-1]
                else:
                    if '年度' in df2.columns[-1]:
                        yyyy = df2.columns[-1][0:4]
                        mm = '-12-31'
                    elif '1-3月' in df2.columns[-1]:
                        yyyy = df2.columns[-1][0:4]
                        mm = '-03-31'
                    elif '1-6月' in df2.columns[-1]:
                        yyyy = df2.columns[-1][0:4]
                        mm = '-06-30'
                    else:
                        yyyy = df2.columns[-1][0:4]
                        mm = '-09-30'
                    current_period = yyyy + mm
                print('当前期数据期间：', current_period)
                if current_period == start_period:
                    df3 = pd.merge(df1, df2)
                    df3.to_csv(os.getcwd() + '\stock_financial\\' + file, encoding='utf8', index=False)
                    print('添加数据成功！')
                    return 1
            else:
                print('调取巨潮数据失败，请查找原因!')
                return 2
            print('原因不明，数据调取失败！')
            return 2
    else:  # 如果应添加的下一期大于截止期，则勿须添加！
        print('本地数据已是最新，勿须添加！')
        return 3

def append_stock_financial_by_stockcode(stockcode):
    filelist = os.listdir(os.getcwd() + '\\stock_financial')
    for file in filelist:
        if stockcode==file[0:6]:
            append_stock_financial(file)
            

if __name__=='__main__':
    filelist = os.listdir(os.getcwd() + '\\stock_financial')
    i = 0
    append_num = 0
    not_append_num = 0
    #not_append_num = 0
    fail_get_num = 0
    for file in filelist:
        i += 1
        stockcode = file[0:6]
        print(i, stockcode)
        append_result=append_stock_financial(file)
        if append_result==1:
            append_num+=1
        elif append_result==2:
            fail_get_num+=1
        elif append_result==3:
            not_append_num+=1
            
        if i > 100000:
            break
    print('-' * 60)
    print('本次添加：', append_num)
    print('本次未添加：', not_append_num)
    print('调取数据失败：', fail_get_num)

# 思路：
'''
1、调取文件列表
2、编历文件列表：
a)提取股票代码
b)将文件读入df
c)查看df最后一列是否是“2016-12-31”or“2016年度”
i.如是，则“数据是新的”，PASS
ii.如不是，调取相应巨潮网页，提取数据到DF，查看DF最后一列是否是“2016-12-31”or“2016年度”
1.如是，则合并到之前DF，并写入原文件
2.如否，则PASS
'''
