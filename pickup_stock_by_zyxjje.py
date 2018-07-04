# coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import time, datetime
import os
import scipy as sp

import stockeval as se

import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


# 将dataframe的数字型字符串转换成浮点数
def str_to_float(str):
    if type(str) == type('ok'):
        return float(str.replace(',', ''))
    else:
        return str


def error(f, x, y):
    return sp.sum((f(x) - y) ** 2)


def jyxjje_analyze(file):
    try:
        df = pd.read_csv(os.getcwd() + '\\stock_financial\\' + file, index_col=0).fillna('0').applymap(
            str_to_float) / 100000000

        # 计算累计经营现金净额
        s_jyxjje = df.loc['经营活动产生的现金流量净额']
        if len(s_jyxjje) < 5:
            return None, None

        s_jyxjje_value = []
        s_jyxjje_index = []
        s_jyxjje_lj_value = []  # 计算累计额
        s_jyxjje_lj_index = []

        for i in range(len(s_jyxjje)):
            if i > 0 and '年度' in s_jyxjje.index[i] and '1-9月' in s_jyxjje.index[i - 1] and s_jyxjje.index[i][:5] == \
                    s_jyxjje.index[i - 1][:5]:
                s_jyxjje_value.append(s_jyxjje[i] - s_jyxjje[i - 1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5] + '10-12月')
            elif '1-9月' in s_jyxjje.index[i] and '1-6月' in s_jyxjje.index[i - 1] and s_jyxjje.index[i][:5] == \
                    s_jyxjje.index[i - 1][:5]:
                s_jyxjje_value.append(s_jyxjje[i] - s_jyxjje[i - 1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5] + '7-9月')
            elif '1-6月' in s_jyxjje.index[i] and '1-3月' in s_jyxjje.index[i - 1] and s_jyxjje.index[i][:5] == \
                    s_jyxjje.index[i - 1][:5]:
                s_jyxjje_value.append(s_jyxjje[i] - s_jyxjje[i - 1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5] + '4-6月')
            else:
                s_jyxjje_value.append(s_jyxjje[i])
                s_jyxjje_index.append(s_jyxjje.index[i])
            s_jyxjje_lj_value.append(sum(s_jyxjje_value))  # 计算累计额
            s_jyxjje_lj_index.append(s_jyxjje_index[i])

        s_jyxjje_new = pd.Series(s_jyxjje_value, index=s_jyxjje_index)
        s_jyxjje_new.name = s_jyxjje.name
        s_jyxjje_lj_new = pd.Series(s_jyxjje_lj_value, index=s_jyxjje_lj_index)
        s_jyxjje_lj_new.name = s_jyxjje.name
        # print(s_jyxjje_lj_new[-1])

        # 计算累计经营性投资现金净额
        s_tzxjje = df.loc['购建固定资产、无形资产和其他长期资产支付的现金']
        if len(s_tzxjje) < 5:
            return None, None

        s_tzxjje_value = []
        s_tzxjje_index = []
        s_tzxjje_lj_value = []  # 计算累计额
        s_tzxjje_lj_index = []

        for i in range(len(s_tzxjje)):
            if i > 0 and '年度' in s_tzxjje.index[i] and '1-9月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                    s_tzxjje.index[i - 1][:5]:
                s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
                s_tzxjje_index.append(s_tzxjje.index[i][:5] + '10-12月')
            elif '1-9月' in s_tzxjje.index[i] and '1-6月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                    s_tzxjje.index[i - 1][:5]:
                s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
                s_tzxjje_index.append(s_tzxjje.index[i][:5] + '7-9月')
            elif '1-6月' in s_tzxjje.index[i] and '1-3月' in s_tzxjje.index[i - 1] and s_tzxjje.index[i][:5] == \
                    s_tzxjje.index[i - 1][:5]:
                s_tzxjje_value.append(s_tzxjje[i] - s_tzxjje[i - 1])
                s_tzxjje_index.append(s_tzxjje.index[i][:5] + '4-6月')
            else:
                s_tzxjje_value.append(s_tzxjje[i])
                s_tzxjje_index.append(s_tzxjje.index[i])
            s_tzxjje_lj_value.append(sum(s_tzxjje_value))  # 计算累计额
            s_tzxjje_lj_index.append(s_tzxjje_index[i])

        s_tzxjje_new = pd.Series(s_tzxjje_value, index=s_tzxjje_index)
        s_tzxjje_new.name = s_tzxjje.name
        s_tzxjje_lj_new = pd.Series(s_tzxjje_lj_value, index=s_tzxjje_lj_index)
        s_tzxjje_lj_new.name = s_tzxjje.name

        # 计算累计自由现金净额
        s_zyxjje_lj = s_jyxjje_lj_new - s_tzxjje_lj_new

        # 分析累计自由现金净额

        x = [a for a in range(len(s_zyxjje_lj))]
        # y=[b for b in s_jyxjje_lj_new]
        y = s_zyxjje_lj / max(abs(s_zyxjje_lj)) * 100

        # plt.scatter(x,y)

        fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
        # print('Model parameters: %s'%fp1)
        f1 = sp.poly1d(fp1)
        # print(error(f1,x,y))

        # fx=sp.linspace(0,x[-1],1000)
        # plt.plot(fx,f1(fx))

        # plt.show()
        return fp1[0], error(f1, x, y)
    except:
        return None, None


if __name__ == '__main__':
    filelist = os.listdir(os.getcwd() + '\\stock_financial')
    # print(filelist)
    f = open(os.getcwd() + '\\stock_pickup\\pickup_stock_by_zyxjje.csv', 'w')
    f.write('股票代码,股票简称,现金成长系数,误差,股价安全水平\n')
    i = 0
    for file in filelist:
        if 'cashflow' in file:
            stockcode = file[:6]
            stockname = file[6:-12]
            xl, error_ = jyxjje_analyze(file)
            print(i, stockcode, stockname, xl, error_)
            print('*' * 50)
            if xl != None:
                if xl > 2:
                    stockcode, stockname, SecurityLevel, GrowthLevel, IncomeLevel, CashLevel, TradePositionLevel = se.GetTotalLevel(
                        stockcode)  # 取得股价安全水平，超过4为安全
                    if SecurityLevel!=None:
                        if SecurityLevel > 4:
                            f.write(str(stockcode) + ',' + stockname + ',' + str(xl) + ',' + str(error_) + ',' + str(SecurityLevel) + '\n')
            i += 1
        if i > 10000:
            break
    f.close()
