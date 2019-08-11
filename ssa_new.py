# coding:utf8

import pandas as pd
import time, datetime
import os

from pandas import DataFrame
from pandas.io.parsers import TextFileReader
import numpy as np
#
import ssa
import stockeval as se


def GetAssets(stockcode):  # 获取历年总资产与净资产
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    # print (file)
    df = pd.read_csv(file, index_col=0)
    if '现金及存放同业款项' in df.index.values:  # 略有文字不一致，导致对金融类和非金融类要作区分
        s_zzc = df.loc['资产总计'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 总资产
        s_jzc = df.loc['所有者权益（或股东权益）合计'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 净资产
    else:
        s_zzc = df.loc['资产总计'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 总资产
        s_jzc = df.loc['所有者权益(或股东权益)合计'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 净资产
    l_index = list(s_zzc.index.values)  # 报告期列表
    l_zzc = list(s_zzc.values)  # 总资产列表
    l_jzc = list(s_jzc.values)  # 净资产列表
    return l_index, l_zzc, l_jzc
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    # print (file)
    df = pd.read_csv(file, index_col=0)
    if '贵金属' in df.index: #银行类。
        s_zzc = df.loc['资产总计'] / 10000  # 总资产
        s_jzc = df.loc['股东权益合计'] / 10000  # 净资产
    elif '融出资金' in df.index: #证券类
        s_zzc = df.loc['资产总计'] / 10000  # 总资产
        s_jzc = df.loc['所有者权益合计'] / 10000  # 净资产
    elif '应收保费' in df.index: #保险类
        s_zzc = df.loc['资产总计'] / 10000  # 总资产
        s_jzc = df.loc['所有者权益合计'] / 10000  # 净资产
    else:
        s_zzc = df.loc['资产总计'] / 10000  # 总资产
        s_jzc = df.loc['所有者权益(或股东权益)合计'] / 10000  # 净资产
    l_index = list(s_zzc.index.values)  # 报告期列表
    l_zzc = list(s_zzc.values)  # 总资产列表
    l_jzc = list(s_jzc.values)  # 净资产列表
    return l_index, l_zzc, l_jzc


def GetAssetsStructure(stockcode):  # 获取最近一期的资产结构
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    #print(file)
    df = pd.read_csv(file, index_col=0)
    if '现金及存放同业款项' in df.index.values:  # 对金融类和非金融类要作区分
        df2 = df.loc[['现金及存放同业款项',
                      '货币资金',
                      '存放中央银行款项',
                      '结算备付金',
                      '贵金属',
                      '拆出资金',
                      '交易性金融资产',
                      '衍生金融资产',
                      '买入返售金融资产',
                      '应收利息',
                      '应收保费',
                      '应收代位追偿款',
                      '应收分保帐款',
                      '应收分保未到期责任准备金',
                      '应收分保未决赔款准备金',
                      '应收分保寿险责任准备金',
                      '应收分保长期健康险责任准备金',
                      '保户质押贷款',
                      '定期存款',
                      '发放贷款及垫款',
                      '存出保证金',
                      '代理业务资产',
                      '应收款项',
                      '预付款项',
                      '可供出售金融资产',
                      '持有至到期投资',
                      '长期股权投资',
                      '存出资本保证金',
                      '投资性房地产',
                      '存货',
                      '固定资产',
                      '在建工程',
                      '无形资产',
                      '长期待摊费用',
                      '固定资产清理',
                      '独立帐户资产',
                      '递延所得税资产',
                      '其他资产'], df.columns[-1]].str.replace(',', '').fillna('0').astype(float) / 100000000
    else:
        df2 = df.loc[['货币资金', '交易性金融资产', '应收票据', '应收账款', '预付款项',
                      '其他应收款', '应收关联公司款', '应收利息', '应收股利', '存货',
                      '一年内到期的非流动资产', '其他流动资产', '可供出售金融资产',
                      '长期应收款', '长期股权投资', '投资性房地产', '固定资产', '在建工程',
                      '工程物资', '固定资产清理', '生产性生物资产', '无形资产', '开发支出',
                      '商誉', '长期待摊费用', '递延所得税资产', '其他非流动资产'],
                     df.columns[-1]].str.replace(',', '').fillna('0').astype(float) / 100000000
    return list(df2.index.values), list(df2.values)
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    #print(file)
    df = pd.read_csv(file, index_col=0)
    if '贵金属' in df.index:  # 银行类
        df2 = df.loc[['现金及存放中央银行款项',
                      '存放同业款项',
                      '拆出资金',
                      '贵金属',
                      '交易性金融资产',
                      '衍生金融工具资产',
                      '买入返售金融资产',
                      '应收利息',
                      '发放贷款及垫款',
                      '代理业务资产',
                      '可供出售金融资产',
                      '持有至到期投资',
                      '长期股权投资',
                      '应收投资款项',
                      '固定资产合计',
                      '无形资产',
                      '商誉',
                      '递延税款借项',
                      '投资性房地产',
                      '其他资产'], df.columns[-1]] / 10000
    elif '融出资金' in df.index: #证券类
        df2 = df.loc[['货币资金',
                      '结算备付金',
                      '融出资金',
                      '交易性金融资产',
                      '衍生金融资产',
                      '买入返售金融资产',
                      '应收账款',
                      '应收利息',
                      '存出保证金',
                      '可供出售金融资产',
                      '持有至到期投资',
                      '长期股权投资',
                      '固定资产',
                      '无形资产',
                      '商誉',
                      '递延所得税资产',
                      '投资性房地产',
                      '其他资产'], df.columns[-1]] / 10000
    elif '应收保费' in df.index: #保险类
        df2 = df.loc[['货币资金',
                      '拆出资金',
                      '交易性金融资产',
                      '衍生金融资产',
                      '买入返售金融资产',
                      '应收保费',
                      '应收利息',
                      '应收分保账款',
                      '应收分保未到期责任准备金',
                      '应收分保未决赔款准备金',
                      '应收分保寿险责任准备金',
                      '应收分保长期健康险责任准备金',
                      '保户质押贷款',
                      '可供出售金融资产',
                      '持有至到期投资',
                      '长期股权投资',
                      '存出资本保证金',
                      '应收款项类投资',
                      '固定资产',
                      '无形资产',
                      '商誉',
                      '独立账户资产',
                      '递延所得税资产',
                      '投资性房地产',
                      '定期存款',
                      '其他资产'], df.columns[-1]] / 10000
    else: #普通类
        for item in df.columns:
            if df[item]['应收票据及应收账款']==0:
                df[item]['应收票据及应收账款']=df[item]['应收票据']+df[item]['应收账款']
            #if df[item]['应付票据及应付账款']==0:
                #df[item]['应付票据及应付账款']=df[item]['应付票据']+df[item]['应付账款']

        df2 = df.loc[['货币资金',
                      '交易性金融资产',
                      '衍生金融资产',
                      '应收票据及应收账款',
                      '预付款项',
                      '应收利息',
                      '应收股利',
                      '其他应收款',
                      '买入返售金融资产',
                      '存货',
                      '划分为持有待售的资产',
                      '一年内到期的非流动资产',
                      '待摊费用',
                      '待处理流动资产损益',
                      '其他流动资产',
                      '发放贷款及垫款',
                      '可供出售金融资产',
                      '持有至到期投资',
                      '长期应收款',
                      '长期股权投资',
                      '投资性房地产',
                      '固定资产净额',
                      '在建工程',
                      '工程物资',
                      '固定资产清理',
                      '生产性生物资产',
                      '公益性生物资产',
                      '油气资产',
                      '无形资产',
                      '开发支出',
                      '商誉',
                      '长期待摊费用',
                      '递延所得税资产',
                      '其他非流动资产'],df.columns[-1]] / 10000
    return list(df2.index.values), list(df2.values)



def GetAssetsSource(stockcode):  # 获取最近一期的资产来源
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    #print(file)
    df = pd.read_csv(file, index_col=0)
    if '现金及存放同业款项' in df.index.values:  # 对金融类和非金融类要作区分
        df2 = df.loc[['向中央银行借款',
                      '同业及其他金融机构存放款项',
                      '短期借款',
                      '拆入资金',
                      '交易性金融负债',
                      '衍生金融负债',
                      '卖出回购金融资产款',
                      '吸收存款',
                      '代理买卖证券款',
                      '代理承销证券款',
                      '应付帐款',
                      '应付票据',
                      '预收款项',
                      '预收保费',
                      '应付手续费及佣金',
                      '应付分保帐款',
                      '应付职工薪酬',
                      '应交税费',
                      '应付利息',
                      '代理业务负债',
                      '预计负债',
                      '应付赔付款',
                      '应付保单红利',
                      '保户储金及投资款',
                      '未到期责任准备金',
                      '未决赔款准备金',
                      '寿险责任准备金',
                      '长期健康险责任准备金',
                      '长期借款',
                      '应付债券',
                      '独立帐户负债',
                      '递延所得税负债',
                      '其他负债',
                      '实收资本（或股本）',
                      '资本公积',
                      '减：库存股',
                      '盈余公积',
                      '一般风险准备',
                      '未分配利润',
                      '少数股东权益',
                      '外币报表折算差额',
                      '非正常经营项目收益调整'], df.columns[-1]].str.replace(',', '').fillna('0').astype(float) / 100000000
    else:
        df2 = df.loc[['短期借款', '交易性金融负债', '应付票据', '应付账款', '预收款项',
                      '应付职工薪酬', '应交税费', '应付利息', '应付股利', '其他应付款',
                      '应付关联公司款', '一年内到期的非流动负债', '其他流动负债',
                      '长期借款', '应付债券', '长期应付款', '专项应付款', '预计负债',
                      '递延所得税负债', '其他非流动负债', '实收资本(或股本)', '资本公积', '盈余公积',
                      '未分配利润', '少数股东权益', '外币报表折算价差', '非正常经营项目收益调整'],
                     df.columns[-1]].str.replace(',', '').fillna('0').astype(float) / 100000000
    return list(df2.index.values), list(df2.values)
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    df = pd.read_csv(file, index_col=0)
    if '贵金属' in df.index:  #银行类
        df2 = df.loc[['向中央银行借款',
                      '同业存入及拆入',
                      '衍生金融工具负债',
                      '交易性金融负债',
                      '卖出回购金融资产款',
                      '客户存款(吸收存款)',
                      '应付职工薪酬',
                      '应交税费',
                      '应付利息',
                      '应付账款',
                      '代理业务负债',
                      '应付债券',
                      '递延所得税负债',
                      '预计负债',
                      '其他负债',
                      '股本',
                      '其他权益工具',
                      '资本公积',
                      '其他综合收益',
                      '盈余公积',
                      '未分配利润',
                      '一般风险准备',
                      '外币报表折算差额',
                      '其他储备'], df.columns[-1]] / 10000
    elif '融出资金' in df.index: #证券类
        df2 = df.loc[['短期借款',
                      '应付短期融资款',
                      '拆入资金',
                      '交易性金融负债',
                      '衍生金融负债',
                      '卖出回购金融资产款',
                      '代理买卖证券款',
                      '代理承销证券款',
                      '应付职工薪酬',
                      '应交税费',
                      '应付账款',
                      '应付利息',
                      '长期借款',
                      '应付债券款',
                      '递延所得税负债',
                      '预计负债',
                      '其他负债',
                      '股本',
                      '其他权益工具',
                      '资本公积金',
                      '其他综合收益',
                      '盈余公积金金',
                      '未分配利润',
                      '一般风险准备',
                      '交易风险准备',
                      '外币报表折算差额'], df.columns[-1]] / 10000
    elif '应收保费' in df.index: #保险类
        df2 = df.loc[['短期借款',
                      '拆入资金',
                      '交易性金融负债',
                      '衍生金融负债',
                      '卖出回购金融资产款',
                      '预收账款',
                      '预收保费',
                      '应付手续费及佣金',
                      '应付分保账款',
                      '应付职工薪酬',
                      '应交税费',
                      '应付利息',
                      '应付赔付款',
                      '应付保单红利',
                      '保户储金及投资款',
                      '未到期责任准备金',
                      '未决赔款准备金',
                      '寿险责任准备金',
                      '长期健康险责任准备金',
                      '长期借款',
                      '应付债券',
                      '独立账户负债',
                      '递延所得税负债',
                      '预计负债',
                      '其他负债',
                      '股本',
                      '资本公积金',
                      '其他综合收益',
                      '盈余公积金金',
                      '未分配利润',
                      '一般风险准备',
                      '外币报表折算差额'], df.columns[-1]] / 10000
    else:
        for item in df.columns:
            #if df[item]['应收票据及应收账款']==0:
                #df[item]['应收票据及应收账款']=df[item]['应收票据']+df[item]['应收账款']
            if df[item]['应付票据及应付账款']==0:
                df[item]['应付票据及应付账款']=df[item]['应付票据']+df[item]['应付账款']
        df2 = df.loc[['短期借款',
                      '交易性金融负债',
                      '应付票据及应付账款',
                      '预收款项',
                      '应付手续费及佣金',
                      '应付职工薪酬',
                      '应交税费',
                      '应付利息',
                      '应付股利',
                      '其他应付款',
                      '预提费用',
                      '一年内的递延收益',
                      '应付短期债券',
                      '一年内到期的非流动负债',
                      '其他流动负债',
                      '长期借款',
                      '应付债券',
                      '长期应付款',
                      '长期应付职工薪酬',
                      '专项应付款',
                      '预计非流动负债',
                      '递延所得税负债',
                      '长期递延收益',
                      '其他非流动负债',
                      '实收资本(或股本)',
                      '资本公积',
                      '其他综合收益',
                      '专项储备',
                      '盈余公积',
                      '一般风险准备',
                      '未分配利润'], df.columns[-1]] / 10000
    return list(df2.index.values), list(df2.values)



def GetPosition(stockcode):  # 获取供应链地位
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    # print(file)
    df = pd.read_csv(file, index_col=0)
    if '现金及存放同业款项' in df.index.values:  # 对金融类和非金融类要作区分
        df2 = df.loc[['吸收存款', '发放贷款及垫款']].fillna('0').applymap(ssa.str_to_float) / 100000000
        s_jyxzc = df2.loc['发放贷款及垫款']  # 经营性资产
        s_jyxfz = df2.loc['吸收存款']  # 经营性负债
    else:
        df2 = df.loc[['应收票据', '应收账款', '预付款项',
                      '应付票据', '应付账款', '预收款项']].fillna('0').applymap(ssa.str_to_float) / 100000000
        s_jyxzc = df2.loc['应收票据'] + df2.loc['应收账款'] + df2.loc['预付款项']  # 经营性资产
        s_jyxfz = df2.loc['应付票据'] + df2.loc['应付账款'] + df2.loc['预收款项']  # 经营性负债
    labels = list(s_jyxzc.index.values)  # 报告期
    data1 = list(s_jyxzc.values)  # 经营性资产
    data2 = list(s_jyxfz.values)  # 经营性负债
    return labels, data1, data2
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode +'balancesheet.csv'
    df = pd.read_csv(file, index_col=0)
    if '贵金属' in df.index:  # 银行类
        df2 = df.loc[['存放同业款项','拆出资金','同业存入及拆入','拆入资金']]/10000
        s_jyxzc = df2.loc['存放同业款项']+df2.loc['拆出资金']  # 经营性资产
        s_jyxfz = df2.loc['同业存入及拆入']+df2.loc['拆入资金'] # 经营性负债
    elif '融出资金' in df.index: #证券类
        df2 = df.loc[['融出资金',
                      '应收账款',
                      '应收利息',
                      '拆入资金',
                      '应付账款',
                      '应付利息']]/10000
        s_jyxzc = df2.loc['融出资金']+df2.loc['应收账款']+df2.loc['应收利息']  # 经营性资产
        s_jyxfz = df2.loc['拆入资金']+df2.loc['应付账款']+df2.loc['应付利息'] # 经营性负债
    elif '应收保费' in df.index: #保险类
        df2 = df.loc[['拆出资金',
                      '应收保费',
                      '应收利息',
                      '应收分保账款',
                      '应收分保未到期责任准备金',
                      '应收分保未决赔款准备金',
                      '应收分保寿险责任准备金',
                      '应收分保长期健康险责任准备金',
                      '拆入资金',
                      '预收账款',
                      '预收保费',
                      '应付手续费及佣金',
                      '应付分保账款',
                      '应付利息']]/10000
        s_jyxzc = df2.loc['拆出资金']+df2.loc['应收保费']+df2.loc['应收利息']+df2.loc['应收分保账款']+df2.loc['应收分保未到期责任准备金']+df2.loc['应收分保未决赔款准备金']+df2.loc['应收分保寿险责任准备金']+df2.loc['应收分保长期健康险责任准备金']  # 经营性资产
        s_jyxfz = df2.loc['拆入资金']+df2.loc['预收账款']+df2.loc['预收保费']+df2.loc['应付手续费及佣金']+df2.loc['应付分保账款']+df2.loc['应付利息'] # 经营性负债
    else: #普通类
        df2 = df.loc[['应收票据及应收账款','应收票据','应收账款','预付款项','应付票据及应付账款','应付票据','应付账款','预收款项']]/ 10000
        for item in df2.columns:
            if df2[item]['应收票据及应收账款']==0:
                df2[item]['应收票据及应收账款']=df2[item]['应收票据']+df2[item]['应收账款']
            if df2[item]['应付票据及应付账款']==0:
                df2[item]['应付票据及应付账款']=df2[item]['应付票据']+df2[item]['应付账款']
        s_jyxzc = df2.loc['应收票据及应收账款'] + df2.loc['预付款项']  # 经营性资产
        s_jyxfz = df2.loc['应付票据及应付账款'] + df2.loc['预收款项']  # 经营性负债
    labels = list(s_jyxzc.index.values)  # 报告期
    data1 = list(s_jyxzc.values)  # 经营性资产
    data2 = list(s_jyxfz.values)  # 经营性负债
    return labels, data1, data2


def GetReceivablesRate(stockcode):  # 获取应收账款比率
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'incomestatements.csv'

    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)

    if '现金及存放同业款项' in df1.index.values:  # 对金融类和非金融类要作区分,计算应收账款
        df3 = df1.loc[['应收利息', '应收保费', '应收代位追偿款', '应收分保帐款', '应收分保未到期责任准备金', '应收分保未决赔款准备金',
                       '应收分保寿险责任准备金', '应收分保长期健康险责任准备金', '应收款项']].fillna('0').applymap(ssa.str_to_float) / 100000000
        s_yszk = df3.loc['应收利息'] + df3.loc['应收保费'] + df3.loc['应收代位追偿款'] + df3.loc['应收分保帐款'] + \
                 df3.loc['应收分保未到期责任准备金'] + df3.loc['应收分保未决赔款准备金'] + df3.loc['应收分保寿险责任准备金'] + \
                 df3.loc['应收分保长期健康险责任准备金'] + df3.loc['应收款项']
    else:
        s_yszk = df1.loc['应收账款'].str.replace(',', '').fillna('0').astype(float) / 100000000

    s_yysr = df2.loc['一、营业收入'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 获取营业收入
    s_yysr_new_index = []
    for index in s_yysr.index.values:  # 将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index] = s_yysr[index] * 4
            s_yysr_new_index.append(index[0:4] + '-03-31')
        if '1-6月' in index:
            s_yysr[index] = s_yysr[index] / 2 * 4
            s_yysr_new_index.append(index[0:4] + '-06-30')
        if '1-9月' in index:
            s_yysr[index] = s_yysr[index] / 3 * 4
            s_yysr_new_index.append(index[0:4] + '-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4] + '-12-31')
    s_yysr = pd.Series(s_yysr.values, index=s_yysr_new_index)
    ReceivableRate = s_yszk / s_yysr * 100
    labels = list(ReceivableRate.index.values)
    data = list(ReceivableRate.values)
    # print(labels,data)
    return labels, data
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'profitstatement.csv'

    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)

    if '贵金属' in df1.index:  # 银行类
        df3 = df1.loc[['存放同业款项',
                       '拆出资金',
                       '应收利息']] / 10000
        s_yszk = df3.loc['存放同业款项'] + df3.loc['拆出资金'] + df3.loc['应收利息']
        s_yysr = df2.loc['一、营业收入'] / 10000  # 获取营业收入
    elif '融出资金' in df1.index: # 证券类
        df3 = df1.loc[['融出资金',
                       '应收账款',
                       '应收利息',]] / 10000
        s_yszk = df3.loc['融出资金'] + df3.loc['应收账款'] + df3.loc['应收利息']
        s_yysr = df2.loc['一、营业收入'] / 10000  # 获取营业收入
    elif '应收保费' in df1.index: # 保险类
        df3 = df1.loc[['拆出资金',
                       '应收保费',
                       '应收利息',
                       '应收分保账款',
                       '应收分保未到期责任准备金',
                       '应收分保未决赔款准备金',
                       '应收分保寿险责任准备金',
                       '应收分保长期健康险责任准备金']] / 10000
        s_yszk = df3.loc['拆出资金'] + df3.loc['应收保费']+df3.loc['应收利息']+df3.loc['应收分保账款']+df3.loc['应收分保未到期责任准备金']+df3.loc['应收分保未决赔款准备金']+df3.loc['应收分保寿险责任准备金']+df3.loc['应收分保长期健康险责任准备金']
        s_yysr = df2.loc['一、营业收入'] / 10000  # 获取营业收入
    else: #普通类
        s_yszk = df1.loc['应收账款'] / 10000
        s_yysr = df2.loc['一、营业总收入'] / 10000  # 获取营业收入
    for index in s_yysr.index.values:  # 将季度营业收入转变为年度营业收入
        if '03-31' in index:
            s_yysr[index] = s_yysr[index] * 4
        if '06-30' in index:
            s_yysr[index] = s_yysr[index] / 2 * 4
        if '09-30' in index:
            s_yysr[index] = s_yysr[index] / 3 * 4
    ReceivableRate = s_yszk / s_yysr * 100
    ReceivableRate.dropna(inplace=True)
    labels = list(ReceivableRate.index.values)
    data = list(ReceivableRate.values)
    return labels, data


def GetInventoryRate(stockcode):  # 获取存货比率
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'incomestatements.csv'

    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)

    if '现金及存放同业款项' in df1.index.values:  # 若是金融企业，没有存货，返回none
        return None, None

    s_ch = df1.loc['存货'].str.replace(',', '').fillna('0').astype(float) / 100000000
    s_yysr = df2.loc['一、营业收入'].str.replace(',', '').fillna('0').astype(float) / 100000000  # 获取营业收入
    s_yysr_new_index = []
    for index in s_yysr.index.values:  # 将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index] = s_yysr[index] * 4
            s_yysr_new_index.append(index[0:4] + '-03-31')
        if '1-6月' in index:
            s_yysr[index] = s_yysr[index] / 2 * 4
            s_yysr_new_index.append(index[0:4] + '-06-30')
        if '1-9月' in index:
            s_yysr[index] = s_yysr[index] / 3 * 4
            s_yysr_new_index.append(index[0:4] + '-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4] + '-12-31')
    s_yysr = pd.Series(s_yysr.values, index=s_yysr_new_index)
    InventoryRate = s_ch / s_yysr * 100
    labels = list(InventoryRate.index.values)
    data = list(InventoryRate.values)
    return labels, data
    '''
    stockname = ssa.get_stockname(stockcode)
    file1 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'balancesheet.csv'
    file2 = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'profitstatement.csv'

    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)

    if '贵金属' in df1.index.values or '融出资金' in df1.index.values or '应收保费' in df1.index.values:  # 若是金融企业，没有存货，返回none
        return None, None

    s_ch = df1.loc['存货'] / 10000
    s_yysr = df2.loc['一、营业总收入'] / 10000  # 获取营业收入
    for index in s_yysr.index.values:  # 将季度营业收入转变为年度营业收入
        if '03-31' in index:
            s_yysr[index] = s_yysr[index] * 4
        if '06-30' in index:
            s_yysr[index] = s_yysr[index] / 2 * 4
        if '09-30' in index:
            s_yysr[index] = s_yysr[index] / 3 * 4
    InventoryRate = s_ch / s_yysr * 100
    InventoryRate.dropna(inplace=True)
    labels = list(InventoryRate.index.values)
    data = list(InventoryRate.values)
    return labels, data


def GetIncomeProfit(stockcode):  # 获取营业状况
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'incomestatements.csv'
    df = pd.read_csv(file, index_col=0)

    if '五、净利润' in df.index.values:  # 金融企业与非金融企业，净利润的项目序号不一样，应区别获取
        # <新改造>
        df1 = df.loc[['一、营业收入', '资产减值损失', '其他业务成本', '三、营业利润', '投资收益', '公允价值变动收益',
                      '汇兑收益', '五、净利润', '其他业务收入']].fillna('0').applymap(ssa.str_to_float) / 100000000
        df1.loc['营业收入'] = df1.loc['一、营业收入']
        df1.loc['净利润'] = df1.loc['五、净利润']
        df1.loc['核心利润'] = df1.loc['三、营业利润'] - df1.loc['投资收益'] - df1.loc['公允价值变动收益'] - df1.loc['汇兑收益'] \
                          - df1.loc['其他业务收入'] + df1.loc['资产减值损失'] + df1.loc['其他业务成本']
        # print(df1)
        # </新改造>
    else:
        # <新改造>
        df1 = df.loc[['一、营业收入', '二、营业利润', '资产减值损失', '加:公允价值变动净收益', '投资收益', '四、净利润',
                      '影响营业利润的其他科目']].fillna('0').applymap(ssa.str_to_float) / 100000000
        df1.loc['营业收入'] = df1.loc['一、营业收入']
        df1.loc['净利润'] = df1.loc['四、净利润']
        df1.loc['核心利润'] = df1.loc['二、营业利润'] + df1.loc['资产减值损失'] - df1.loc['加:公允价值变动净收益'] - df1.loc['投资收益'] \
                          - df1.loc['影响营业利润的其他科目']

        # print(df1)
        # </新改造>

    # <新改造>
    #print(df1)
    for column in df1.columns:  # 将季度数据转变为年度数据
        if '1-3月' in column:
            df1[column] = df1[column] * 4
            df1.rename(columns={column: column[0:4] + '-03-31'}, inplace=True)
        if '1-6月' in column:
            df1[column] = df1[column] / 2 * 4
            df1.rename(columns={column: column[0:4] + '-06-30'}, inplace=True)
        if '1-9月' in column:
            df1[column] = df1[column] / 3 * 4
            df1.rename(columns={column: column[0:4] + '-09-30'}, inplace=True)
        if '年度' in column:
            df1.rename(columns={column: column[0:4] + '-12-31'}, inplace=True)
    # print(df1)
    # </新改造>


    labels = list(df1.columns)
    #print('标签：')
    #print(labels)
    data1 = list(df1.loc['营业收入'])
    #print('营业收入：')
    #print(data1)
    data2 = list(df1.loc['核心利润'])
    #print('核心利润：')
    #print(data2)
    data3 = list(df1.loc['净利润'])
    #print('净利润：')
    #print(data3)
    return labels, data1, data2, data3
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'profitstatement.csv'
    df = pd.read_csv(file, index_col=0)

    if '其他业务支出' in df.index:  # 银行类
        df1 = df.loc[['一、营业收入','汇兑收益','投资净收益','公允价值变动净收益','其他业务收入','资产减值损失','其他业务支出','三、营业利润','五、净利润',]] / 10000
        df1.loc['营业收入'] = df1.loc['一、营业收入']
        df1.loc['净利润'] = df1.loc['五、净利润']
        df1.loc['核心利润'] = df1.loc['三、营业利润'] - df1.loc['投资净收益'] - df1.loc['公允价值变动净收益'] - df1.loc['汇兑收益'] \
                          - df1.loc['其他业务收入'] + df1.loc['资产减值损失'] + df1.loc['其他业务支出']
    elif '利息支出' in df.index: # 证券类
        df1 = df.loc[['一、营业收入','投资收益','公允价值变动损益','汇兑损益','其他业务收入','资产减值损失','其他业务成本','三、营业利润','五、净利润']] / 10000
        df1.loc['营业收入'] = df1.loc['一、营业收入']
        df1.loc['净利润'] = df1.loc['五、净利润']
        df1.loc['核心利润'] = df1.loc['三、营业利润'] - df1.loc['投资收益'] - df1.loc['公允价值变动损益'] - df1.loc['汇兑损益'] \
                          - df1.loc['其他业务收入'] + df1.loc['资产减值损失'] + df1.loc['其他业务成本']
    elif '退保金' in df.index: # 保险类：
        df1 = df.loc[['一、营业收入','投资净收益','公允价值变动损益','汇兑损益','其他业务收入','其他业务成本','资产减值损失','三、营业利润','五、净利润']] / 10000
        df1.loc['营业收入'] = df1.loc['一、营业收入']
        df1.loc['净利润'] = df1.loc['五、净利润']
        df1.loc['核心利润'] = df1.loc['三、营业利润'] - df1.loc['投资净收益'] - df1.loc['公允价值变动损益'] - df1.loc['汇兑损益'] \
                          - df1.loc['其他业务收入'] + df1.loc['资产减值损失'] + df1.loc['其他业务成本']
    else: # 普通类
        df1 = df.loc[['一、营业总收入','资产减值损失','公允价值变动收益','投资收益','汇兑收益','三、营业利润','五、净利润']] / 10000
        df1.loc['营业收入'] = df1.loc['一、营业总收入']
        df1.loc['净利润'] = df1.loc['五、净利润']
        df1.loc['核心利润'] = df1.loc['三、营业利润'] + df1.loc['资产减值损失'] - df1.loc['公允价值变动收益'] - df1.loc['投资收益'] \
                          - df1.loc['汇兑收益']
    for column in df1.columns:  # 将季度数据转变为年度数据
        if '03-31' in column:
            df1[column] = df1[column] * 4
        if '06-30' in column:
            df1[column] = df1[column] / 2 * 4
        if '09-30' in column:
            df1[column] = df1[column] / 3 * 4


    labels = list(df1.columns)
    data1 = list(df1.loc['营业收入'])
    data2 = list(df1.loc['核心利润'])
    data3 = list(df1.loc['净利润'])
    return labels, data1, data2, data3


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


def GetNetCashFlowSum(stockcode):  # 获取累计经营、投资和筹资累计现金流
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0).fillna('0').applymap(ssa.str_to_float)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_tzxjje = df6.loc['投资活动产生的现金流量净额'] / 100000000  # 投资现金净额
    # 以下换算成季度数据
    s_tzxjje_value = []
    s_tzxjje_index = []
    s_tzxjje_lj_value = []  # 计算累计额
    s_tzxjje_lj_index = []
    for i in range(len(s_tzxjje)):
        if i > 0 and '年度' in s_tzxjje.index[i] and '1-9月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-12-31')
        elif '1-9月' in s_tzxjje.index[i] and '1-6月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-09-30')
        elif '1-6月' in s_tzxjje.index[i] and '1-3月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-06-30')
        else:
            s_tzxjje_value.append(s_tzxjje[i])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-03-31')
        s_tzxjje_lj_value.append(sum(s_tzxjje_value))  # 计算累计额
        s_tzxjje_lj_index.append(s_tzxjje_index[i])
    s_tzxjje_new = pd.Series(s_tzxjje_value, index=s_tzxjje_index)
    s_tzxjje_new.name = s_tzxjje.name
    s_tzxjje_lj_new = pd.Series(s_tzxjje_lj_value, index=s_tzxjje_lj_index)
    s_tzxjje_lj_new.name = s_tzxjje.name

    s_czxjje = df6.loc['筹资活动产生的现金流量净额'] / 100000000  # 筹资现金净额
    # 以下换算成季度数据
    s_czxjje_value = []
    s_czxjje_index = []
    s_czxjje_lj_value = []  # 计算累计额
    s_czxjje_lj_index = []
    for i in range(len(s_czxjje)):
        if i > 0 and '年度' in s_czxjje.index[i] and '1-9月' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-12-31')
        elif '1-9月' in s_czxjje.index[i] and '1-6月' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-09-30')
        elif '1-6月' in s_czxjje.index[i] and '1-3月' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-06-30')
        else:
            s_czxjje_value.append(s_czxjje[i])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-03-31')
        s_czxjje_lj_value.append(sum(s_czxjje_value))  # 计算累计额
        s_czxjje_lj_index.append(s_czxjje_index[i])

    s_czxjje_new = pd.Series(s_czxjje_value, index=s_czxjje_index)
    s_czxjje_new.name = s_czxjje.name
    s_czxjje_lj_new = pd.Series(s_czxjje_lj_value, index=s_czxjje_lj_index)
    s_czxjje_lj_new.name = s_czxjje.name

    s_jyxjje_0 = df6.loc['经营活动产生的现金流量净额'] / 100000000  # 未经年度换算的经营现金净额,因尽量偷懒，复制的ssa中的代码
    # 以下换算成季度数据
    s_jyxjje_0_value = []
    s_jyxjje_0_index = []
    s_jyxjje_0_lj_value = []  # 计算累计额
    s_jyxjje_0_lj_index = []

    for i in range(len(s_jyxjje_0)):
        if i > 0 and '年度' in s_jyxjje_0.index[i] and '1-9月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-12-31')
        elif '1-9月' in s_jyxjje_0.index[i] and '1-6月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-09-30')
        elif '1-6月' in s_jyxjje_0.index[i] and '1-3月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-06-30')
        else:
            s_jyxjje_0_value.append(s_jyxjje_0[i])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-03-31')
        s_jyxjje_0_lj_value.append(sum(s_jyxjje_0_value))  # 计算累计额
        s_jyxjje_0_lj_index.append(s_jyxjje_0_index[i])

    s_jyxjje_0_new = pd.Series(s_jyxjje_0_value, index=s_jyxjje_0_index)
    s_jyxjje_0_new.name = s_jyxjje_0.name
    s_jyxjje_0_lj_new = pd.Series(s_jyxjje_0_lj_value, index=s_jyxjje_0_lj_index)
    s_jyxjje_0_lj_new.name = s_jyxjje_0.name

    # 整理数据以便输出
    labels = list(s_jyxjje_0_lj_new.index.values)  # x刻度
    data1 = list(s_jyxjje_0_lj_new.values)  # 经营性现金净额
    data2 = list(s_czxjje_lj_new.values)  # 筹资性现金净额
    data3 = list(s_tzxjje_lj_new.values)  # 投资性现金净额

    return labels, data1, data2, data3
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_tzxjje = df6.loc['投资活动产生的现金流量净额'] / 10000  # 投资现金净额
    # 以下换算成季度数据
    s_tzxjje_value = []
    s_tzxjje_index = []
    s_tzxjje_lj_value = []  # 计算累计额
    s_tzxjje_lj_index = []
    for i in range(len(s_tzxjje)):
        if i > 0 and '12-31' in s_tzxjje.index[i] and '09-30' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-12-31')
        elif '09-30' in s_tzxjje.index[i] and '06-30' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-09-30')
        elif '06-30' in s_tzxjje.index[i] and '03-31' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-06-30')
        else:
            s_tzxjje_value.append(s_tzxjje[i])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-03-31')
        s_tzxjje_lj_value.append(sum(s_tzxjje_value))  # 计算累计额
        s_tzxjje_lj_index.append(s_tzxjje_index[i])
    s_tzxjje_new = pd.Series(s_tzxjje_value, index=s_tzxjje_index)
    s_tzxjje_new.name = s_tzxjje.name
    s_tzxjje_lj_new = pd.Series(s_tzxjje_lj_value, index=s_tzxjje_lj_index)
    s_tzxjje_lj_new.name = s_tzxjje.name

    s_czxjje = df6.loc['筹资活动产生的现金流量净额'] / 10000  # 筹资现金净额
    # 以下换算成季度数据
    s_czxjje_value = []
    s_czxjje_index = []
    s_czxjje_lj_value = []  # 计算累计额
    s_czxjje_lj_index = []
    for i in range(len(s_czxjje)):
        if i > 0 and '12-31' in s_czxjje.index[i] and '09-30' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-12-31')
        elif '09-30' in s_czxjje.index[i] and '06-30' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-09-30')
        elif '06-30' in s_czxjje.index[i] and '03-31' in s_czxjje.index[i - 1] and s_czxjje.index[i][:5] == \
                s_czxjje.index[i - 1][:5]:
            s_czxjje_value.append(s_czxjje[i] - s_czxjje[i - 1])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-06-30')
        else:
            s_czxjje_value.append(s_czxjje[i])
            s_czxjje_index.append(s_czxjje.index[i][:4] + '-03-31')
        s_czxjje_lj_value.append(sum(s_czxjje_value))  # 计算累计额
        s_czxjje_lj_index.append(s_czxjje_index[i])

    s_czxjje_new = pd.Series(s_czxjje_value, index=s_czxjje_index)
    s_czxjje_new.name = s_czxjje.name
    s_czxjje_lj_new = pd.Series(s_czxjje_lj_value, index=s_czxjje_lj_index)
    s_czxjje_lj_new.name = s_czxjje.name

    s_jyxjje_0 = df6.loc['经营活动产生的现金流量净额'] / 10000  # 未经年度换算的经营现金净额,因尽量偷懒，复制的ssa中的代码
    # 以下换算成季度数据
    s_jyxjje_0_value = []
    s_jyxjje_0_index = []
    s_jyxjje_0_lj_value = []  # 计算累计额
    s_jyxjje_0_lj_index = []

    for i in range(len(s_jyxjje_0)):
        if i > 0 and '12-31' in s_jyxjje_0.index[i] and '09-30' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-12-31')
        elif '09-30' in s_jyxjje_0.index[i] and '06-30' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-09-30')
        elif '06-30' in s_jyxjje_0.index[i] and '03-31' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-06-30')
        else:
            s_jyxjje_0_value.append(s_jyxjje_0[i])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-03-31')
        s_jyxjje_0_lj_value.append(sum(s_jyxjje_0_value))  # 计算累计额
        s_jyxjje_0_lj_index.append(s_jyxjje_0_index[i])

    s_jyxjje_0_new = pd.Series(s_jyxjje_0_value, index=s_jyxjje_0_index)
    s_jyxjje_0_new.name = s_jyxjje_0.name
    s_jyxjje_0_lj_new = pd.Series(s_jyxjje_0_lj_value, index=s_jyxjje_0_lj_index)
    s_jyxjje_0_lj_new.name = s_jyxjje_0.name

    # 整理数据以便输出
    labels = list(s_jyxjje_0_lj_new.index.values)  # x刻度
    data1 = list(s_jyxjje_0_lj_new.values)  # 经营性现金净额
    data2 = list(s_czxjje_lj_new.values)  # 筹资性现金净额
    data3 = list(s_tzxjje_lj_new.values)  # 投资性现金净额

    return labels, data1, data2, data3


def GetInvestmentCash(stockcode):  # 获取投资、经营性投资支付的现金
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0).fillna('0').applymap(ssa.str_to_float)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_tzzfxj = df6.loc['投资支付的现金'] / 100000000  # 投资现金净额
    # 投资现金净额换算成季度数据
    s_tzzfxj_value = []
    s_tzzfxj_index = []
    for i in range(len(s_tzzfxj)):
        if i > 0 and '年度' in s_tzzfxj.index[i] and '1-9月' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '10-12月')
        elif '1-9月' in s_tzzfxj.index[i] and '1-6月' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '7-9月')
        elif '1-6月' in s_tzzfxj.index[i] and '1-3月' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '4-6月')
        else:
            s_tzzfxj_value.append(s_tzzfxj[i])
            s_tzzfxj_index.append(s_tzzfxj.index[i])
    s_tzzfxj_new = pd.Series(s_tzzfxj_value, index=s_tzzfxj_index)
    s_tzzfxj_new.name = s_tzzfxj.name

    s_jytzxj = df6.loc['购建固定资产、无形资产和其他长期资产支付的现金'] / 100000000  # 经营投资现金
    s_jytzxj_value = []
    s_jytzxj_index = []
    for i in range(len(s_jytzxj)):
        if i > 0 and '年度' in s_jytzxj.index[i] and '1-9月' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '10-12月')
        elif '1-9月' in s_jytzxj.index[i] and '1-6月' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '7-9月')
        elif '1-6月' in s_jytzxj.index[i] and '1-3月' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '4-6月')
        else:
            s_jytzxj_value.append(s_jytzxj[i])
            s_jytzxj_index.append(s_jytzxj.index[i])
    s_jytzxj_new = pd.Series(s_jytzxj_value, index=s_jytzxj_index)
    s_jytzxj_new.name = s_jytzxj.name

    # 数据整理
    labels = list(s_jytzxj_new.index.values)  # x轴标签
    data1 = list(s_tzzfxj_new.values)  # 投资支付的现金
    data2 = list(s_jytzxj_new.values)  # 购建固定资产、无形资产和其他长期资产支付的现金

    return labels, data1, data2
    '''
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    if '预计负债' in df6.index: # 普通类
        s_tzzfxj = df6.loc['投资所支付的现金'] / 10000  # 投资现金净额
    else: # 银行类、证券类、保险类
        s_tzzfxj = df6.loc['投资支付的现金'] / 10000  # 投资现金净额
    
    # 投资现金净额换算成季度数据
    s_tzzfxj_value = []
    s_tzzfxj_index = []
    for i in range(len(s_tzzfxj)):
        if i > 0 and '12-31' in s_tzzfxj.index[i] and '09-30' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '10-12月')
        elif '09-30' in s_tzzfxj.index[i] and '06-30' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '7-9月')
        elif '06-30' in s_tzzfxj.index[i] and '03-31' in s_tzzfxj.index[i - 1] and s_tzzfxj.index[i][:5] == \
                s_tzzfxj.index[i - 1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i] - s_tzzfxj[i - 1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5] + '4-6月')
        else:
            s_tzzfxj_value.append(s_tzzfxj[i])
            s_tzzfxj_index.append(s_tzzfxj.index[i])
    s_tzzfxj_new = pd.Series(s_tzzfxj_value, index=s_tzzfxj_index)
    s_tzzfxj_new.name = s_tzzfxj.name

    if '预计负债' in df6.index: # 普通类
        s_jytzxj = df6.loc['购建固定资产、无形资产和其他长期资产所支付的现金'] / 10000  # 经营投资现金
    else: # 银行类、证券类、保险类
        s_jytzxj = df6.loc['购建固定资产、无形资产和其他长期资产支付的现金'] / 10000  # 经营投资现金
    s_jytzxj_value = []
    s_jytzxj_index = []
    for i in range(len(s_jytzxj)):
        if i > 0 and '12-31' in s_jytzxj.index[i] and '09-30' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '10-12月')
        elif '09-30' in s_jytzxj.index[i] and '06-30' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '7-9月')
        elif '06-30' in s_jytzxj.index[i] and '03-31' in s_jytzxj.index[i - 1] and s_jytzxj.index[i][:5] == \
                s_jytzxj.index[i - 1][:5]:
            s_jytzxj_value.append(s_jytzxj[i] - s_jytzxj[i - 1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5] + '4-6月')
        else:
            s_jytzxj_value.append(s_jytzxj[i])
            s_jytzxj_index.append(s_jytzxj.index[i])
    s_jytzxj_new = pd.Series(s_jytzxj_value, index=s_jytzxj_index)
    s_jytzxj_new.name = s_jytzxj.name

    # 数据整理
    labels = list(s_jytzxj_new.index.values)  # x轴标签
    data1 = list(s_tzzfxj_new.values)  # 投资支付的现金
    data2 = list(s_jytzxj_new.values)  # 购建固定资产、无形资产和其他长期资产支付的现金

    return labels, data1, data2


def GetRaiseCash(stockcode):  # 获取筹资、借款收到的现金
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0).fillna('0').applymap(ssa.str_to_float)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_xstzsdxj = df6.loc['吸收投资收到的现金'] / 100000000  # 吸收投资收到的现金
    # 吸收投资收到的现金换算成季度数据
    s_xstzsdxj_value = []
    s_xstzsdxj_index = []
    for i in range(len(s_xstzsdxj)):
        if i > 0 and '年度' in s_xstzsdxj.index[i] and '1-9月' in s_xstzsdxj.index[i - 1] and s_xstzsdxj.index[i][:5] == \
                s_xstzsdxj.index[i - 1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i] - s_xstzsdxj[i - 1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5] + '10-12月')
        elif '1-9月' in s_xstzsdxj.index[i] and '1-6月' in s_xstzsdxj.index[i - 1] and s_xstzsdxj.index[i][:5] == \
                s_xstzsdxj.index[i - 1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i] - s_xstzsdxj[i - 1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5] + '7-9月')
        elif '1-6月' in s_xstzsdxj.index[i] and '1-3月' in s_xstzsdxj.index[i - 1] and s_xstzsdxj.index[i][:5] == \
                s_xstzsdxj.index[i - 1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i] - s_xstzsdxj[i - 1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5] + '4-6月')
        else:
            s_xstzsdxj_value.append(s_xstzsdxj[i])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i])
    s_xstzsdxj_new = pd.Series(s_xstzsdxj_value, index=s_xstzsdxj_index)
    s_xstzsdxj_new.name = s_xstzsdxj.name

    s_qdjksdxj = df6.loc['取得借款收到的现金'] / 100000000  # 吸收借款收到的现金
    # 吸收借款收到的现金换算成季度数据
    s_qdjksdxj_value = []
    s_qdjksdxj_index = []
    for i in range(len(s_qdjksdxj)):
        if i > 0 and '年度' in s_qdjksdxj.index[i] and '1-9月' in s_qdjksdxj.index[i - 1] and s_qdjksdxj.index[i][:5] == \
                s_qdjksdxj.index[i - 1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i] - s_qdjksdxj[i - 1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5] + '10-12月')
        elif '1-9月' in s_qdjksdxj.index[i] and '1-6月' in s_qdjksdxj.index[i - 1] and s_qdjksdxj.index[i][:5] == \
                s_qdjksdxj.index[i - 1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i] - s_qdjksdxj[i - 1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5] + '7-9月')
        elif '1-6月' in s_qdjksdxj.index[i] and '1-3月' in s_qdjksdxj.index[i - 1] and s_qdjksdxj.index[i][:5] == \
                s_qdjksdxj.index[i - 1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i] - s_qdjksdxj[i - 1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5] + '4-6月')
        else:
            s_qdjksdxj_value.append(s_qdjksdxj[i])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i])
    s_qdjksdxj_new = pd.Series(s_qdjksdxj_value, index=s_qdjksdxj_index)
    s_qdjksdxj_new.name = s_qdjksdxj.name

    # 整理数据
    labels = list(s_xstzsdxj_new.index.values)
    data1 = list(s_xstzsdxj_new.values)  # 吸收投资收到的现金
    data2 = list(s_qdjksdxj_new.values)  # 吸收借款收到的现金

    return labels, data1, data2


def GetFundHolding(stockcode):  # 获取基金持股
    stockname = ssa.get_stockname(stockcode)
    df7 = pd.read_csv(os.getcwd() + '\\fund_holdings\\' + stockcode + stockname + '.csv', index_col=1).fillna(
        '0').applymap(ssa.str_to_float)  # 因尽量偷懒，df7延用复制代码
    df8 = df7.sort_index()
    s_cgjs = df8['持股基金家数']  # 持股家数
    labels = list(s_cgjs.index.values)  # x轴标签
    data = list(s_cgjs.values)  # 基金持股
    return labels, data


def GetFreeCashFlowSum(stockcode):  # 获取累计自由现金流
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial\\' + stockcode + stockname + 'cashflow.csv'
    df6 = pd.read_csv(file, index_col=0).fillna('0').applymap(ssa.str_to_float)  # 之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_tzxjje = df6.loc['购建固定资产、无形资产和其他长期资产支付的现金'] / 100000000  # 经营性投资现金支出
    # 以下换算成季度数据
    s_tzxjje_value = []
    s_tzxjje_index = []
    s_tzxjje_lj_value = []  # 计算累计额
    s_tzxjje_lj_index = []
    for i in range(len(s_tzxjje)):
        if i > 0 and '年度' in s_tzxjje.index[i] and '1-9月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-12-31')
        elif '1-9月' in s_tzxjje.index[i] and '1-6月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-09-30')
        elif '1-6月' in s_tzxjje.index[i] and '1-3月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                s_tzxjje.index[i - 1][:5]:
            s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-06-30')
        else:
            s_tzxjje_value.append(s_tzxjje[i])
            s_tzxjje_index.append(s_tzxjje.index[i][:4] + '-03-31')
        s_tzxjje_lj_value.append(sum(s_tzxjje_value))  # 计算累计额
        s_tzxjje_lj_index.append(s_tzxjje_index[i])
    s_tzxjje_new = pd.Series(s_tzxjje_value, index=s_tzxjje_index)
    s_tzxjje_new.name = s_tzxjje.name
    s_tzxjje_lj_new = pd.Series(s_tzxjje_lj_value, index=s_tzxjje_lj_index)
    s_tzxjje_lj_new.name = s_tzxjje.name


    s_jyxjje_0 = df6.loc['经营活动产生的现金流量净额'] / 100000000  # 未经年度换算的经营现金净额,因尽量偷懒，复制的ssa中的代码
    # 以下换算成季度数据
    s_jyxjje_0_value = []
    s_jyxjje_0_index = []
    s_jyxjje_0_lj_value = []  # 计算累计额
    s_jyxjje_0_lj_index = []

    for i in range(len(s_jyxjje_0)):
        if i > 0 and '年度' in s_jyxjje_0.index[i] and '1-9月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-12-31')
        elif '1-9月' in s_jyxjje_0.index[i] and '1-6月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-09-30')
        elif '1-6月' in s_jyxjje_0.index[i] and '1-3月' in s_jyxjje_0.index[i - 1] and s_jyxjje_0.index[i][:5] == \
                s_jyxjje_0.index[i - 1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i] - s_jyxjje_0[i - 1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-06-30')
        else:
            s_jyxjje_0_value.append(s_jyxjje_0[i])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4] + '-03-31')
        s_jyxjje_0_lj_value.append(sum(s_jyxjje_0_value))  # 计算累计额
        s_jyxjje_0_lj_index.append(s_jyxjje_0_index[i])

    s_jyxjje_0_new = pd.Series(s_jyxjje_0_value, index=s_jyxjje_0_index)
    s_jyxjje_0_new.name = s_jyxjje_0.name
    s_jyxjje_0_lj_new = pd.Series(s_jyxjje_0_lj_value, index=s_jyxjje_0_lj_index)
    s_jyxjje_0_lj_new.name = s_jyxjje_0.name

    s_zyxjl_lj=s_jyxjje_0_lj_new-s_tzxjje_lj_new #累计自由现金流

    # 整理数据以便输出
    labels = list(s_jyxjje_0_lj_new.index.values)  # x刻度
    data1 = list(s_jyxjje_0_lj_new.values)  # 累计经营性现金净额
    data2 = list(s_zyxjl_lj.values)  # 累计自由现金流

    return labels, data1, data2

def GetMarketCode(StockCode): #根据股票代码前三位，返回市场代码SH，或者SZ
    MarketCode = {'600': 'SH', '601': 'SH', '603': 'SH', '000': 'SZ', '002': 'SZ', '300': 'SZ'}
    return MarketCode[StockCode[:3]]

def GetAveragePE(StockCode): #根据股票代码到亿牛网获取过去10年的平均市盈率
    url='https://eniu.com/gu/'+GetMarketCode(StockCode)+StockCode
    try:
        dfs=pd.read_html(url)
        AveragePE=dfs[0]['平均'].mean()
        return AveragePE
    except:
        return 15

def GetProfitCAGR(StockCode): #获取历史净利润(归属于母公司所有者的净利润)复合增长率CAGR
    stockname = ssa.get_stockname(StockCode)
    df=pd.read_csv(os.getcwd()+'\\stock_financial\\'+StockCode+stockname+'incomestatements.csv',index_col=0)
    if '（一）归属于母公司所有者的净利润' in df.index.values:
        profits=df.loc['（一）归属于母公司所有者的净利润']
    else:
        profits=df.loc['归属于母公司所有者的净利润']
    profits=profits[profits.index.str[-2:]=='年度'].fillna('0').apply(ssa.str_to_float)

    for term in profits.index: #去除净利润为零或负数的初始年度
        if profits[term]<=0:
            profits=profits.drop(term)
        else:
            break
    n=len(profits)-1
    CAGR=(profits[-1]/profits[0])**(1/n)-1
    return CAGR

def GetEPS(StockCode): #获取最近一年度的每股收益
    stockname = ssa.get_stockname(StockCode)
    df=pd.read_csv(os.getcwd()+'\\stock_financial\\'+StockCode+stockname+'incomestatements.csv',index_col=0)
    if '（一）归属于母公司所有者的净利润' in df.index.values:
        profits=df.loc['（一）归属于母公司所有者的净利润']
    else:
        profits=df.loc['归属于母公司所有者的净利润']
    profits=profits[profits.index.str[-2:]=='年度'].fillna('0').apply(ssa.str_to_float)
    shares = se.GetShares(StockCode)
    EPS=profits[-1]/shares

    return EPS


def GetFutureROI(StockCode): #根据历史平均市盈率、历史净利润复合增长率、当前股价，测算将来10年投资复合收益率
    FutureEPS=GetEPS(StockCode)*(1+GetProfitCAGR(StockCode))**10
    FuturePrice=GetAveragePE(StockCode)*FutureEPS
    FutureROI=(FuturePrice/se.GetStockPrice(StockCode))**(1/10)-1

    return FutureROI


if __name__ == '__main__':
    stockcode = input('请输入股票代码:')
    print(GetProfitCAGR(stockcode))
