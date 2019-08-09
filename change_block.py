#coding:utf-8

import pandas as pd
#import get_stockprice_from_hexun as gsfh
from bs4 import BeautifulSoup as bs
import requests as rq
import os,time
import ssa
import numpy as np
from intervalue import InterValue as iv
import matplotlib.pyplot as plt
import tushare as ts
import math
import re
import json



def GetROE(stockcode):  # 获取资产收益率
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'incomestatements.csv'

    df1 = pd.read_csv(file1, index_col=0)  # type: Union[Union[type, DataFrame, TextFileReader], Any]
    df2 = pd.read_csv(file2, index_col=0)

    if '现金及存放同业款项' in df1.index.values:  # 科目、文字不相同，导致对金融类和非金融类要作区分

        # <新改造>
        df1_1 = df1.loc[['短期借款', '拆入资金', '交易性金融负债', '衍生金融负债', '卖出回购金融资产款', '吸收存款',
                         '长期借款', '应付债券', '向中央银行借款', '所有者权益（或股东权益）合计', '同业及其他金融机构存放款项',
                         '资产总计']].fillna('0').applymap(ssa.str_to_float) / 100000000
        df1_1.loc['总资产'] = df1_1.loc['资产总计']
        df1_1.loc['净资产'] = df1_1.loc['所有者权益（或股东权益）合计']
        df1_1.loc['有息负债'] = df1_1.loc['短期借款'] + df1_1.loc['拆入资金'] + df1_1.loc['交易性金融负债'] + df1_1.loc['衍生金融负债'] + \
                            df1_1.loc['卖出回购金融资产款'] + df1_1.loc['吸收存款'] + df1_1.loc['长期借款'] + df1_1.loc['应付债券'] + \
                            df1_1.loc['向中央银行借款'] + df1_1.loc['同业及其他金融机构存放款项']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]
        # print(df1_2)

        # </新改造>

    else:

        # <新改造>
        df1_1 = df1.loc[['短期借款', '长期借款', '应付债券', '所有者权益(或股东权益)合计', '资产总计']].fillna('0').applymap(
            ssa.str_to_float) / 100000000
        df1_1.loc['总资产'] = df1_1.loc['资产总计']
        df1_1.loc['净资产'] = df1_1.loc['所有者权益(或股东权益)合计']
        df1_1.loc['有息负债'] = df1_1.loc['短期借款'] + df1_1.loc['长期借款'] + df1_1.loc['应付债券']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]
        # print(df1_2)
        # </新改造>

    if '五、净利润' in df2.index.values:  # 金融企业与非金融企业，科目、文字不一样，应区别获取

        # <新改造>
        df2_1 = df2.loc[['保单红利支出', '利息支出', '四、利润总额', '五、净利润']].fillna('0').applymap(
            ssa.str_to_float) / 100000000
        df2_1.loc['净利润'] = df2_1.loc['五、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['保单红利支出'] + df2_1.loc['利息支出'] + df2_1.loc['四、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['保单红利支出'] + df2_1.loc['利息支出']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
        # print(df2_2)

        # </新改造>

    else:
        # <新改造>
        df2_1 = df2.loc[['财务费用', '三、利润总额', '四、净利润']].fillna('0').applymap(ssa.str_to_float) / 100000000
        df2_1.loc['净利润'] = df2_1.loc['四、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['财务费用'] + df2_1.loc['三、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['财务费用']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
        # print(df2_2)

        # </新改造>

    # <新改造>
    # 将季度利润表数据转变为年度数据，并将列名修改为与资产负债表的一致
    # print(df2_2)
    for column in df2_2.columns:
        if '1-3月' in column:
            df2_2[column] = df2_2[column] * 4
            df2_2.rename(columns={column: column[0:4] + '-03-31'}, inplace=True)
        if '1-6月' in column:
            df2_2[column] = df2_2[column] / 2 * 4
            df2_2.rename(columns={column: column[0:4] + '-06-30'}, inplace=True)

        if '1-9月' in column:
            df2_2[column] = df2_2[column] / 3 * 4
            df2_2.rename(columns={column: column[0:4] + '-09-30'}, inplace=True)
        if '年度' in column:
            df2_2.rename(columns={column: column[0:4] + '-12-31'}, inplace=True)
    df3 = pd.concat([df1_2, df2_2], join='inner')
    df3.loc['净资产收益率'] = df3.loc['净利润'] / df3.loc['净资产'] * 100
    df3.loc['息税前资产收益率'] = df3.loc['息税前利润'] / df3.loc['总资产'] * 100
    df3.loc['有息负债利率'] = df3.loc['负债成本'] / df3.loc['有息负债'] * 100
    df3 = df3.replace(np.inf, np.nan).replace(-(np.inf), np.nan)
    df3 = df3.fillna(0)
    # print(df3)

    # </新改造>

    labels = list(df3.columns)
    # print(labels)
    data1 = list(df3.loc['息税前资产收益率'])
    # print(data1)
    data2 = list(df3.loc['净资产收益率'])
    # print(data2)
    data3 = list(df3.loc['有息负债利率'])
    # print(data3)
    return labels, data1, data2, data3
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'profitstatement.csv'

    df1 = pd.read_csv(file1, index_col=0)  
    df2 = pd.read_csv(file2, index_col=0)

    if '贵金属' in df1.index:  # 银行类
        df1_1 = df1.loc[['向中央银行借款',
                         '同业存入及拆入',
                         '拆入资金',
                         '衍生金融工具负债',
                         '交易性金融负债',
                         '卖出回购金融资产款',
                         '客户存款(吸收存款)',
                         '应付债券',
                         '股东权益合计',
                         '负债及股东权益总计']] / 10000
        df1_1.loc['总资产'] = df1_1.loc['负债及股东权益总计']
        df1_1.loc['净资产'] = df1_1.loc['股东权益合计']
        df1_1.loc['有息负债'] = df1_1.loc['向中央银行借款'] + df1_1.loc['同业存入及拆入'] + df1_1.loc['拆入资金'] + df1_1.loc['衍生金融工具负债'] + \
                            df1_1.loc['交易性金融负债'] + df1_1.loc['卖出回购金融资产款'] + df1_1.loc['客户存款(吸收存款)'] + df1_1.loc['应付债券']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]

        df2_1 = df2.loc[['减：利息支出','四、利润总额','五、净利润']] / 10000
        df2_1.loc['净利润'] = df2_1.loc['五、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['减：利息支出'] + df2_1.loc['四、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['减：利息支出']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
    elif '融出资金' in df1.index: # 证券类
        df1_1 = df1.loc[['短期借款',
                         '应付短期融资款',
                         '拆入资金',
                         '交易性金融负债',
                         '衍生金融负债',
                         '卖出回购金融资产款',
                         '长期借款',
                         '应付债券款',
                         '所有者权益合计',
                         '负债及股东权益总计']] / 10000
        df1_1.loc['总资产'] = df1_1.loc['负债及股东权益总计']
        df1_1.loc['净资产'] = df1_1.loc['所有者权益合计']
        df1_1.loc['有息负债'] = df1_1.loc['短期借款'] + df1_1.loc['应付短期融资款'] + df1_1.loc['拆入资金'] + df1_1.loc['交易性金融负债'] + \
                            df1_1.loc['衍生金融负债'] + df1_1.loc['卖出回购金融资产款'] + df1_1.loc['长期借款'] + df1_1.loc['应付债券款']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]

        df2_1 = df2.loc[['利息支出','四、利润总额','五、净利润']] / 10000
        df2_1.loc['净利润'] = df2_1.loc['五、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['利息支出'] + df2_1.loc['四、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['利息支出']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
    elif '应收保费' in df1.index: # 保险类
        df1_1 = df1.loc[['短期借款',
                         '拆入资金',
                         '交易性金融负债',
                         '衍生金融负债',
                         '卖出回购金融资产款',
                         '长期借款',
                         '应付债券',
                         '所有者权益合计',
                         '负债及股东权益总计']] / 10000
        df1_1.loc['总资产'] = df1_1.loc['负债及股东权益总计']
        df1_1.loc['净资产'] = df1_1.loc['所有者权益合计']
        df1_1.loc['有息负债'] = df1_1.loc['短期借款'] + df1_1.loc['拆入资金'] + df1_1.loc['交易性金融负债'] + \
                            df1_1.loc['衍生金融负债'] + df1_1.loc['卖出回购金融资产款'] + df1_1.loc['长期借款'] + df1_1.loc['应付债券']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]

        df2_1 = df2.loc[['保户红利支出','四、利润总额','五、净利润']] / 10000
        df2_1.loc['净利润'] = df2_1.loc['五、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['保户红利支出'] + df2_1.loc['四、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['保户红利支出']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
    else: #普通类
        df1_1 = df1.loc[['短期借款',
                         '交易性金融负债',
                         '应付短期债券',
                         '长期借款',
                         '应付债券',
                         '所有者权益(或股东权益)合计',
                         '负债和所有者权益(或股东权益)总计']] / 10000
        df1_1.loc['总资产'] = df1_1.loc['负债和所有者权益(或股东权益)总计']
        df1_1.loc['净资产'] = df1_1.loc['所有者权益(或股东权益)合计']
        df1_1.loc['有息负债'] = df1_1.loc['短期借款'] + df1_1.loc['交易性金融负债'] + df1_1.loc['应付短期债券'] + \
                            df1_1.loc['长期借款'] + df1_1.loc['应付债券']
        df1_2 = df1_1.loc[['总资产', '净资产', '有息负债']]
        print(df1_2)

        df2_1 = df2.loc[['财务费用','四、利润总额','五、净利润']] / 10000
        df2_1.loc['净利润'] = df2_1.loc['五、净利润']
        df2_1.loc['息税前利润'] = df2_1.loc['财务费用'] + df2_1.loc['四、利润总额']
        df2_1.loc['负债成本'] = df2_1.loc['财务费用']
        df2_2 = df2_1.loc[['净利润', '息税前利润', '负债成本']]
        
    # 将季度利润表数据转变为年度数据
    for column in df2_2.columns:
        if '03-31' in column:
            df2_2[column] = df2_2[column] * 4
        if '06-30' in column:
            df2_2[column] = df2_2[column] / 2 * 4
        if '09-30' in column:
            df2_2[column] = df2_2[column] / 3 * 4
    df3 = pd.concat([df1_2, df2_2], join='inner')
    df3.loc['净资产收益率'] = df3.loc['净利润'] / df3.loc['净资产'] * 100
    df3.loc['息税前资产收益率'] = df3.loc['息税前利润'] / df3.loc['总资产'] * 100
    df3.loc['有息负债利率'] = df3.loc['负债成本'] / df3.loc['有息负债'] * 100
    df3 = df3.replace(np.inf, np.nan).replace(-(np.inf), np.nan)
    df3 = df3.fillna(0)


    # </新改造>

    labels = list(df3.columns)
    # print(labels)
    data1 = list(df3.loc['息税前资产收益率'])
    # print(data1)
    data2 = list(df3.loc['净资产收益率'])
    # print(data2)
    data3 = list(df3.loc['有息负债利率'])
    # print(data3)
    return labels, data1, data2, data3
    

print(GetROE('000651'))





