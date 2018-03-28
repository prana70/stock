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

def GetNetCashFlowSum(stockcode): #获取累计经营、投资和筹资累计现金流
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'cashflow.csv'
    df6=pd.read_csv(file,index_col=0).fillna('0').applymap(ssa.str_to_float) #之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用
    
    s_tzxjje=df6.loc['投资活动产生的现金流量净额']/100000000#投资现金净额
    #以下换算成季度数据
    s_tzxjje_value=[]
    s_tzxjje_index=[]
    s_tzxjje_lj_value=[]#计算累计额
    s_tzxjje_lj_index=[]
    for i in range(len(s_tzxjje)):
        if i>0 and  '年度' in s_tzxjje.index[i] and '1-9月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4]+'-12-31')
        elif '1-9月' in s_tzxjje.index[i] and '1-6月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4]+'-09-30')
        elif '1-6月' in s_tzxjje.index[i] and '1-3月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:4]+'-06-30')
        else:
            s_tzxjje_value.append(s_tzxjje[i])
            s_tzxjje_index.append(s_tzxjje.index[i][:4]+'-03-31')
        s_tzxjje_lj_value.append(sum(s_tzxjje_value))#计算累计额
        s_tzxjje_lj_index.append(s_tzxjje_index[i])
    s_tzxjje_new=pd.Series(s_tzxjje_value,index=s_tzxjje_index)
    s_tzxjje_new.name=s_tzxjje.name
    s_tzxjje_lj_new=pd.Series(s_tzxjje_lj_value,index=s_tzxjje_lj_index)
    s_tzxjje_lj_new.name=s_tzxjje.name

    s_czxjje=df6.loc['筹资活动产生的现金流量净额']/100000000#筹资现金净额
    #以下换算成季度数据
    s_czxjje_value=[]
    s_czxjje_index=[]
    s_czxjje_lj_value=[]#计算累计额
    s_czxjje_lj_index=[]
    for i in range(len(s_czxjje)):
        if i>0 and  '年度' in s_czxjje.index[i] and '1-9月' in s_czxjje.index[i-1] and s_czxjje.index[i][:5]==s_czxjje.index[i-1][:5]:
            s_czxjje_value.append(s_czxjje[i]-s_czxjje[i-1])
            s_czxjje_index.append(s_czxjje.index[i][:4]+'-12-31')
        elif '1-9月' in s_czxjje.index[i] and '1-6月' in s_czxjje.index[i-1] and s_czxjje.index[i][:5]==s_czxjje.index[i-1][:5]:
            s_czxjje_value.append(s_czxjje[i]-s_czxjje[i-1])
            s_czxjje_index.append(s_czxjje.index[i][:4]+'-09-30')
        elif '1-6月' in s_czxjje.index[i] and '1-3月' in s_czxjje.index[i-1] and s_czxjje.index[i][:5]==s_czxjje.index[i-1][:5]:
            s_czxjje_value.append(s_czxjje[i]-s_czxjje[i-1])
            s_czxjje_index.append(s_czxjje.index[i][:4]+'-06-30')
        else:
            s_czxjje_value.append(s_czxjje[i])
            s_czxjje_index.append(s_czxjje.index[i][:4]+'-03-31')
        s_czxjje_lj_value.append(sum(s_czxjje_value))#计算累计额
        s_czxjje_lj_index.append(s_czxjje_index[i])

    s_czxjje_new=pd.Series(s_czxjje_value,index=s_czxjje_index)
    s_czxjje_new.name=s_czxjje.name
    s_czxjje_lj_new=pd.Series(s_czxjje_lj_value,index=s_czxjje_lj_index)
    s_czxjje_lj_new.name=s_czxjje.name

    s_jyxjje_0=df6.loc['经营活动产生的现金流量净额']/100000000#未经年度换算的经营现金净额,因尽量偷懒，复制的ssa中的代码
    #以下换算成季度数据
    s_jyxjje_0_value=[]
    s_jyxjje_0_index=[]
    s_jyxjje_0_lj_value=[]#计算累计额
    s_jyxjje_0_lj_index=[]

    for i in range(len(s_jyxjje_0)):
        if i>0 and  '年度' in s_jyxjje_0.index[i] and '1-9月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4]+'-12-31')
        elif '1-9月' in s_jyxjje_0.index[i] and '1-6月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4]+'-09-30')
        elif '1-6月' in s_jyxjje_0.index[i] and '1-3月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4]+'-06-30')
        else:
            s_jyxjje_0_value.append(s_jyxjje_0[i])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:4]+'-03-31')
        s_jyxjje_0_lj_value.append(sum(s_jyxjje_0_value))#计算累计额
        s_jyxjje_0_lj_index.append(s_jyxjje_0_index[i])
            
    s_jyxjje_0_new=pd.Series(s_jyxjje_0_value,index=s_jyxjje_0_index)
    s_jyxjje_0_new.name=s_jyxjje_0.name
    s_jyxjje_0_lj_new=pd.Series(s_jyxjje_0_lj_value,index=s_jyxjje_0_lj_index)
    s_jyxjje_0_lj_new.name=s_jyxjje_0.name


    #整理数据以便输出
    labels=list(s_jyxjje_0_lj_new.index.values) #x刻度
    data1=list(s_jyxjje_0_lj_new.values) #经营性现金净额
    data2=list(s_czxjje_lj_new.values) #筹资性现金净额
    data3=list(s_tzxjje_lj_new.values) #投资性现金净额
    
    return labels,data1,data2,data3


def GetInvestmentCash(stockcode): #获取投资、经营性投资支付的现金
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'cashflow.csv'
    df6=pd.read_csv(file,index_col=0).fillna('0').applymap(ssa.str_to_float) #之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_tzzfxj=df6.loc['投资支付的现金']/100000000#投资现金净额
    #投资现金净额换算成季度数据
    s_tzzfxj_value=[]
    s_tzzfxj_index=[]
    for i in range(len(s_tzzfxj)):
        if i>0 and  '年度' in s_tzzfxj.index[i] and '1-9月' in s_tzzfxj.index[i-1] and s_tzzfxj.index[i][:5]==s_tzzfxj.index[i-1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i]-s_tzzfxj[i-1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5]+'10-12月')
        elif '1-9月' in s_tzzfxj.index[i] and '1-6月' in s_tzzfxj.index[i-1] and s_tzzfxj.index[i][:5]==s_tzzfxj.index[i-1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i]-s_tzzfxj[i-1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5]+'7-9月')
        elif '1-6月' in s_tzzfxj.index[i] and '1-3月' in s_tzzfxj.index[i-1] and s_tzzfxj.index[i][:5]==s_tzzfxj.index[i-1][:5]:
            s_tzzfxj_value.append(s_tzzfxj[i]-s_tzzfxj[i-1])
            s_tzzfxj_index.append(s_tzzfxj.index[i][:5]+'4-6月')
        else:
            s_tzzfxj_value.append(s_tzzfxj[i])
            s_tzzfxj_index.append(s_tzzfxj.index[i])
    s_tzzfxj_new=pd.Series(s_tzzfxj_value,index=s_tzzfxj_index)
    s_tzzfxj_new.name=s_tzzfxj.name

    s_jytzxj=df6.loc['购建固定资产、无形资产和其他长期资产支付的现金']/100000000#经营投资现金
    s_jytzxj_value=[]
    s_jytzxj_index=[]
    for i in range(len(s_jytzxj)):
        if i>0 and  '年度' in s_jytzxj.index[i] and '1-9月' in s_jytzxj.index[i-1] and s_jytzxj.index[i][:5]==s_jytzxj.index[i-1][:5]:
            s_jytzxj_value.append(s_jytzxj[i]-s_jytzxj[i-1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5]+'10-12月')
        elif '1-9月' in s_jytzxj.index[i] and '1-6月' in s_jytzxj.index[i-1] and s_jytzxj.index[i][:5]==s_jytzxj.index[i-1][:5]:
            s_jytzxj_value.append(s_jytzxj[i]-s_jytzxj[i-1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5]+'7-9月')
        elif '1-6月' in s_jytzxj.index[i] and '1-3月' in s_jytzxj.index[i-1] and s_jytzxj.index[i][:5]==s_jytzxj.index[i-1][:5]:
            s_jytzxj_value.append(s_jytzxj[i]-s_jytzxj[i-1])
            s_jytzxj_index.append(s_jytzxj.index[i][:5]+'4-6月')
        else:
            s_jytzxj_value.append(s_jytzxj[i])
            s_jytzxj_index.append(s_jytzxj.index[i])
    s_jytzxj_new=pd.Series(s_jytzxj_value,index=s_jytzxj_index)
    s_jytzxj_new.name=s_jytzxj.name

    #数据整理
    labels=list(s_jytzxj_new.index.values) #x轴标签
    data1=list(s_tzzfxj_new.values) #投资支付的现金
    data2=list(s_jytzxj_new.values) #购建固定资产、无形资产和其他长期资产支付的现金
    
    return labels,data1,data2
    

def GetRaiseCash(stockcode): #获取筹资、借款收到的现金
    stockname=ssa.get_stockname(stockcode)
    file=os.getcwd()+'\\stock_financial\\'+stockcode+stockname+'cashflow.csv'
    df6=pd.read_csv(file,index_col=0).fillna('0').applymap(ssa.str_to_float) #之所以是df6,是因为从ssa中复制的代码，为尽量偷懒，故延用

    s_xstzsdxj=df6.loc['吸收投资收到的现金']/100000000#吸收投资收到的现金
    #吸收投资收到的现金换算成季度数据
    s_xstzsdxj_value=[]
    s_xstzsdxj_index=[]
    for i in range(len(s_xstzsdxj)):
        if i>0 and  '年度' in s_xstzsdxj.index[i] and '1-9月' in s_xstzsdxj.index[i-1] and s_xstzsdxj.index[i][:5]==s_xstzsdxj.index[i-1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i]-s_xstzsdxj[i-1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5]+'10-12月')
        elif '1-9月' in s_xstzsdxj.index[i] and '1-6月' in s_xstzsdxj.index[i-1] and s_xstzsdxj.index[i][:5]==s_xstzsdxj.index[i-1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i]-s_xstzsdxj[i-1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5]+'7-9月')
        elif '1-6月' in s_xstzsdxj.index[i] and '1-3月' in s_xstzsdxj.index[i-1] and s_xstzsdxj.index[i][:5]==s_xstzsdxj.index[i-1][:5]:
            s_xstzsdxj_value.append(s_xstzsdxj[i]-s_xstzsdxj[i-1])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i][:5]+'4-6月')
        else:
            s_xstzsdxj_value.append(s_xstzsdxj[i])
            s_xstzsdxj_index.append(s_xstzsdxj.index[i])
    s_xstzsdxj_new=pd.Series(s_xstzsdxj_value,index=s_xstzsdxj_index)
    s_xstzsdxj_new.name=s_xstzsdxj.name

    s_qdjksdxj=df6.loc['取得借款收到的现金']/100000000#吸收借款收到的现金
    #吸收借款收到的现金换算成季度数据
    s_qdjksdxj_value=[]
    s_qdjksdxj_index=[]
    for i in range(len(s_qdjksdxj)):
        if i>0 and  '年度' in s_qdjksdxj.index[i] and '1-9月' in s_qdjksdxj.index[i-1] and s_qdjksdxj.index[i][:5]==s_qdjksdxj.index[i-1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i]-s_qdjksdxj[i-1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5]+'10-12月')
        elif '1-9月' in s_qdjksdxj.index[i] and '1-6月' in s_qdjksdxj.index[i-1] and s_qdjksdxj.index[i][:5]==s_qdjksdxj.index[i-1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i]-s_qdjksdxj[i-1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5]+'7-9月')
        elif '1-6月' in s_qdjksdxj.index[i] and '1-3月' in s_qdjksdxj.index[i-1] and s_qdjksdxj.index[i][:5]==s_qdjksdxj.index[i-1][:5]:
            s_qdjksdxj_value.append(s_qdjksdxj[i]-s_qdjksdxj[i-1])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i][:5]+'4-6月')
        else:
            s_qdjksdxj_value.append(s_qdjksdxj[i])
            s_qdjksdxj_index.append(s_qdjksdxj.index[i])
    s_qdjksdxj_new=pd.Series(s_qdjksdxj_value,index=s_qdjksdxj_index)
    s_qdjksdxj_new.name=s_qdjksdxj.name

    #整理数据
    labels=list(s_xstzsdxj_new.index.values)
    data1=list(s_xstzsdxj_new.values) #吸收投资收到的现金
    data2=list(s_qdjksdxj_new.values) #吸收借款收到的现金
    
    return labels,data1,data2


def GetFundHolding(stockcode): #获取基金持股
    stockname=ssa.get_stockname(stockcode)
    df7=pd.read_csv(os.getcwd()+'\\fund_holdings\\'+stockcode+stockname+'.csv',index_col=1).fillna('0').applymap(ssa.str_to_float) #因尽量偷懒，df7延用复制代码
    df8=df7.sort_index()
    s_cgjs=df8['持股基金家数'] #持股家数
    labels=list(s_cgjs.index.values) #x轴标签
    data=list(s_cgjs.values) #基金持股
    return labels,data


    
if __name__=='__main__':
    stockcode=input('请输入股票代码:')
    print(GetFundHolding(stockcode))
