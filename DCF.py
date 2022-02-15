#coding:utf8

import ssa
import os
import pandas as pd
import stockeval

def GetAnnualFreeCashFlow(stockcode):  # 获取年度自由现金流
    stockname = ssa.get_stockname(stockcode)
    file = os.getcwd() + '\\stock_financial_sina\\' + stockcode + 'cashflow.csv'
    df = pd.read_csv(file, index_col=0)  # 之所以是df,是因为从ssa中复制的代码，为尽量偷懒，故延用

    df=df.filter(regex='12-31',axis=1) #筛选年度数据

    if '预计负债' in df.index: # 普通类
        s_tzxj = df.loc['购建固定资产、无形资产和其他长期资产所支付的现金'] / 10000  # 经营性投资现金支出
    else: # 金融类
        s_tzxj = df.loc['购建固定资产、无形资产和其他长期资产支付的现金'] / 10000  # 经营性投资现金支出



    s_jyxjje = df.loc['经营活动产生的现金流量净额'] / 10000  # 未经年度换算的经营现金净额,因尽量偷懒，复制的ssa中的代码
    print(s_jyxjje)

    #计算自由现金
    s_zyxj=s_jyxjje-s_tzxj
    s_zyxj.name='自由现金流'
    print(s_zyxj)

    return s_zyxj


def DCF(stock_code):
    series_of_free_cashflow=GetAnnualFreeCashFlow(stock_code)#获取年度自由现金流列表

    
    cashflow_of_the_end=series_of_free_cashflow[len(series_of_free_cashflow)-1]
    print('自由现金流：',format(cashflow_of_the_end,',.2f'),'亿元')

    cashflow_of_the_begin=0
    for ele in series_of_free_cashflow:
        if ele>0:
            cashflow_of_the_begin=ele
            break

        
    shares=stockeval.GetShares(stock_code)/10**8

    cashflow_of_per_share=cashflow_of_the_end/shares

    print('每股自由现金流：',format(cashflow_of_per_share,',.2f'),'元')

    #计算10年快速现金增长率
    years=int(series_of_free_cashflow.index[len(series_of_free_cashflow)-1][0:4])-int(series_of_free_cashflow.index[0][:4])
    growth_rate_of_free_cashflow=(cashflow_of_the_end/cashflow_of_the_begin)**(1/years)-1
    print('10年快速增长率：%s'%format(growth_rate_of_free_cashflow,'.2%'))

    '''
    #计算10年快速现金增长率（历年加权平均法）
    print('10年现金流列表：')
    print(series_of_free_cashflow)
    sum_of_weight_cashflow=0 #历年现金流加权之和
    sum_of_weight=0 #历年现金流权重之和，年代越远，权重越小
    for j in range(len(series_of_free_cashflow)-1):
        sum_of_weight_cashflow=sum_of_weight_cashflow+(series_of_free_cashflow[j+1]/series_of_free_cashflow[j]-1)*(j+1)
        sum_of_weight=sum_of_weight+(j+1)
    growth_rate_of_cashflow1=sum_of_weight_cashflow/sum_of_weight
    print('10年快速增长率（加权平均）：%s'%format(growth_rate_of_cashflow1,'.2%'))
    '''

    #10年后永续现金增长率
    growth_rate_of_free_cashflow_forever=0.01

    #折现率
    discount_rate=0.07

    value_of_the_year=0
    value_of_ten_years=0
    for i in range(10):
        i+=1
        value_of_the_year=(1+growth_rate_of_free_cashflow)**i/(1+discount_rate)**i
        value_of_ten_years+=value_of_the_year
    value_of_ten_years=value_of_ten_years*cashflow_of_per_share
    
    value_after_ten_years=(cashflow_of_per_share*(1+growth_rate_of_free_cashflow)**10)*(1+growth_rate_of_free_cashflow_forever)/(discount_rate-growth_rate_of_free_cashflow_forever)/(1+discount_rate)**10

    print('10年快速增长现值：%s元'%format(value_of_ten_years,',.2f'))
    print('10年永续增长现值：%s元'%format(value_after_ten_years,',.2f'))

    value_of_total=value_of_ten_years+value_after_ten_years

    return value_of_total,cashflow_of_per_share,growth_rate_of_free_cashflow

if __name__=='__main__':
    
    stock_code=input('请输入A股代码：')
    stock_name=ssa.get_stockname(stock_code)
    stock_price=stockeval.GetStockPrice(stock_code)
    stock_earning=stockeval.GetNetProfit(stock_code)/stockeval.GetShares(stock_code)
    print(stock_name)
    print('股价：',format(stock_price,',.2f'),'元')
    print('每股收益：',format(stock_earning,',.2f'),'元')
    print('-'*50)

    inter_value=DCF(stock_code)
    print('每股估值：',format(inter_value[0],',.2f'),'元')

