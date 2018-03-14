#coding:utf8

import pandas as pd
import time,datetime
import os
import ssa


def GetAssets(stockcode): #获取历年总资产与净资产
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    #print (file)
    df=pd.read_csv(file,index_col=0)
    if '现金及存放同业款项' in df.index.values: #略有文字不一致，导致对金融类和非金融类要作区分
        s_zzc=df.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
        s_jzc=df.loc['所有者权益（或股东权益）合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    else:    
        s_zzc=df.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
        s_jzc=df.loc['所有者权益(或股东权益)合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    l_index=list(s_zzc.index.values) #报告期列表
    l_zzc=list(s_zzc.values) #总资产列表
    l_jzc=list(s_jzc.values) #净资产列表
    return l_index,l_zzc,l_jzc


def GetAssetsStructure(stockcode): #获取最近一期的资产结构
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    print (file)
    df=pd.read_csv(file,index_col=0)
    if '现金及存放同业款项' in df.index.values: #对金融类和非金融类要作区分
        df2=df.loc[['现金及存放同业款项',
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
            '其他资产'], df.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    else:
        df2=df.loc[['货币资金','交易性金融资产','应收票据','应收账款','预付款项',
             '其他应收款','应收关联公司款','应收利息','应收股利','存货',
             '一年内到期的非流动资产','其他流动资产','可供出售金融资产',
             '长期应收款','长期股权投资','投资性房地产','固定资产','在建工程',
             '工程物资','固定资产清理','生产性生物资产','无形资产','开发支出',
             '商誉','长期待摊费用','递延所得税资产','其他非流动资产'],
            df.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    return list(df2.index.values),list(df2.values)

def GetAssetsSource(stockcode): #获取最近一期的资产来源
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    print (file)
    df=pd.read_csv(file,index_col=0)
    if '现金及存放同业款项' in df.index.values: #对金融类和非金融类要作区分
        df2=df.loc[['向中央银行借款',
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
        '非正常经营项目收益调整'], df.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    else:
        df2=df.loc[['短期借款','交易性金融负债','应付票据','应付账款','预收款项',
                 '应付职工薪酬','应交税费','应付利息','应付股利','其他应付款',
                 '应付关联公司款','一年内到期的非流动负债','其他流动负债',
                 '长期借款','应付债券','长期应付款','专项应付款','预计负债',
                 '递延所得税负债','其他非流动负债','实收资本(或股本)','资本公积','盈余公积',
                 '未分配利润','少数股东权益','外币报表折算价差','非正常经营项目收益调整'],
            df.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    return list(df2.index.values),list(df2.values)
    
def GetPosition(stockcode): #获取供应链地位
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    print (file)
    df=pd.read_csv(file,index_col=0)
    if '现金及存放同业款项' in df.index.values: #对金融类和非金融类要作区分
        df2=df.loc[['吸收存款','发放贷款及垫款']].fillna('0').applymap(ssa.str_to_float)/100000000
        s_jyxzc=df2.loc['发放贷款及垫款'] #经营性资产
        s_jyxfz=df2.loc['吸收存款'] #经营性负债
    else:
        df2=df.loc[['应收票据','应收账款','预付款项',
                 '应付票据','应付账款','预收款项']].fillna('0').applymap(ssa.str_to_float)/100000000
        s_jyxzc=df2.loc['应收票据']+df2.loc['应收账款']+df2.loc['预付款项']#经营性资产
        s_jyxfz=df2.loc['应付票据']+df2.loc['应付账款']+df2.loc['预收款项']#经营性负债
    labels=list(s_jyxzc.index.values) #报告期
    data1=list(s_jyxzc.values) #经营性资产
    data2=list(s_jyxfz.values) #经营性负债
    return labels,data1,data2

def GetReceivablesRate(stockcode): #获取应收账款比率
    stockname=ssa.get_stockname(stockcode)
    file1=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    file2=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'

    df1=pd.read_csv(file1,index_col=0)
    df2=pd.read_csv(file2,index_col=0)

    if '现金及存放同业款项' in df1.index.values: #对金融类和非金融类要作区分,计算应收账款
        df3=df1.loc[['应收利息','应收保费','应收代位追偿款','应收分保帐款','应收分保未到期责任准备金','应收分保未决赔款准备金',
                     '应收分保寿险责任准备金','应收分保长期健康险责任准备金','应收款项']].fillna('0').applymap(ssa.str_to_float)/100000000
        s_yszk=df3.loc['应收利息']+df3.loc['应收保费']+df3.loc['应收代位追偿款']+df3.loc['应收分保帐款']+ \
                df3.loc['应收分保未到期责任准备金']+df3.loc['应收分保未决赔款准备金']+df3.loc['应收分保寿险责任准备金']+ \
                df3.loc['应收分保长期健康险责任准备金']+df3.loc['应收款项']
    else:
        s_yszk=df1.loc['应收账款'].str.replace(',','').fillna('0').astype(float)/100000000

    s_yysr=df2.loc['一、营业收入'].str.replace(',','').fillna('0').astype(float)/100000000 #获取营业收入
    s_yysr_new_index=[]
    for index in s_yysr.index.values: #将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index]=s_yysr[index]*4
            s_yysr_new_index.append(index[0:4]+'-03-31')
        if '1-6月' in index:
            s_yysr[index]=s_yysr[index]/2*4
            s_yysr_new_index.append(index[0:4]+'-06-30')
        if '1-9月' in index:
            s_yysr[index]=s_yysr[index]/3*4
            s_yysr_new_index.append(index[0:4]+'-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4]+'-12-31')
    s_yysr=pd.Series(s_yysr.values,index=s_yysr_new_index)
    ReceivableRate=s_yszk/s_yysr*100
    labels=list(ReceivableRate.index.values)
    data=list(ReceivableRate.values)
    #print(labels,data)
    return labels,data
 
def GetInventoryRate(stockcode): #获取存货比率
    stockname=ssa.get_stockname(stockcode)
    file1=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    file2=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'

    df1=pd.read_csv(file1,index_col=0)
    df2=pd.read_csv(file2,index_col=0)

    if '现金及存放同业款项'  in df1.index.values: #若是金融企业，没有存货，返回none
        return None,None

    s_ch=df1.loc['存货'].str.replace(',','').fillna('0').astype(float)/100000000
    s_yysr=df2.loc['一、营业收入'].str.replace(',','').fillna('0').astype(float)/100000000 #获取营业收入
    s_yysr_new_index=[]
    for index in s_yysr.index.values: #将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index]=s_yysr[index]*4
            s_yysr_new_index.append(index[0:4]+'-03-31')
        if '1-6月' in index:
            s_yysr[index]=s_yysr[index]/2*4
            s_yysr_new_index.append(index[0:4]+'-06-30')
        if '1-9月' in index:
            s_yysr[index]=s_yysr[index]/3*4
            s_yysr_new_index.append(index[0:4]+'-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4]+'-12-31')
    s_yysr=pd.Series(s_yysr.values,index=s_yysr_new_index)
    InventoryRate=s_ch/s_yysr*100
    labels=list(InventoryRate.index.values)
    data=list(InventoryRate.values)
    #print(labels,data)
    return labels,data

def GetIncomeProfit(stockcode): #获取营业状况
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'
    df=pd.read_csv(file,index_col=0)

    s_yysr=df.loc['一、营业收入'].str.replace(',','').fillna('0').astype(float)/100000000 #获取营业收入
    s_yysr_new_index=[]
    for index in s_yysr.index.values: #将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_yysr[index]=s_yysr[index]*4
            s_yysr_new_index.append(index[0:4]+'-03-31')
        if '1-6月' in index:
            s_yysr[index]=s_yysr[index]/2*4
            s_yysr_new_index.append(index[0:4]+'-06-30')
        if '1-9月' in index:
            s_yysr[index]=s_yysr[index]/3*4
            s_yysr_new_index.append(index[0:4]+'-09-30')
        if '年度' in index:
            s_yysr_new_index.append(index[0:4]+'-12-31')
    s_yysr=pd.Series(s_yysr.values,index=s_yysr_new_index)

    if '五、净利润'  in df.index.values: #金融企业与非金融企业，净利润的项目序号不一样，应区别获取
        s_jlr=df.loc['五、净利润'].str.replace(',','').fillna('0').astype(float)/100000000
    else:
        s_jlr=df.loc['四、净利润'].str.replace(',','').fillna('0').astype(float)/100000000

    for index in s_jlr.index.values: #将季度营业收入转变为年度营业收入
        if '1-3月' in index:
            s_jlr[index]=s_jlr[index]*4
        if '1-6月' in index:
            s_jlr[index]=s_jlr[index]/2*4
        if '1-9月' in index:
            s_jlr[index]=s_jlr[index]/3*4
        
    labels=list(s_yysr.index.values)
    data1=list(s_yysr.values)
    data2=list(s_jlr.values)
    return labels,data1,data2

def GetROE(stockcode): #获取资产收益率
    stockname=ssa.get_stockname(stockcode)
    file1=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'balancesheet.csv'
    file2=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'incomestatements.csv'

    df1=pd.read_csv(file1,index_col=0)
    df2=pd.read_csv(file2,index_col=0)

    if '现金及存放同业款项' in df1.index.values: #略有文字不一致，导致对金融类和非金融类要作区分
        s_zzc=df1.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
        s_jzc=df1.loc['所有者权益（或股东权益）合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    else:    
        s_zzc=df1.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
        s_jzc=df1.loc['所有者权益(或股东权益)合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产

    if '五、净利润'  in df2.index.values: #金融企业与非金融企业，净利润的项目序号不一样，应区别获取
        s_jlr=df2.loc['五、净利润'].str.replace(',','').fillna('0').astype(float)/100000000
    else:
        s_jlr=df2.loc['四、净利润'].str.replace(',','').fillna('0').astype(float)/100000000

    s_jlr_new_index=[]
    for index in s_jlr.index.values: #将季度净利润转变为年度净利润
        if '1-3月' in index:
            s_jlr[index]=s_jlr[index]*4
            s_jlr_new_index.append(index[0:4]+'-03-31')
        if '1-6月' in index:
            s_jlr[index]=s_jlr[index]/2*4
            s_jlr_new_index.append(index[0:4]+'-06-30')
        if '1-9月' in index:
            s_jlr[index]=s_jlr[index]/3*4
            s_jlr_new_index.append(index[0:4]+'-09-30')
        if '年度' in index:
            s_jlr_new_index.append(index[0:4]+'-12-31')
    s_jlr=pd.Series(s_jlr.values,index=s_jlr_new_index)

    ROA=s_jlr/s_zzc*100 #总资产收益率
    ROE=s_jlr/s_jzc*100 #净资产收益率

    labels=list(ROA.index.values)
    data1=list(ROA.values)
    data2=list(ROE.values)
    return labels,data1,data2

    
if __name__=='__main__':
    stockcode=input('请输入股票代码:')
    print(GetROE(stockcode))
