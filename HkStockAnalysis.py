import pandas as pd
import os


def GetHkStockFinancial(StockCode):
    FilePath = os.getcwd() + '\\HkStockFinancial\\'
    if os.path.exists(FilePath + StockCode + 'Balance.csv') and os.path.exists(
            FilePath + StockCode + 'Cashflow.csv') and os.path.exists(FilePath + StockCode + 'Income.csv'):
        # 将港股的三大财务报表合成一个表，并将列的顺序调整为升序。
        df1 = pd.read_csv(FilePath + StockCode + 'Balance.csv', index_col=0)
        df2 = pd.read_csv(FilePath + StockCode + 'Cashflow.csv', index_col=0)
        df3 = pd.read_csv(FilePath + StockCode + 'Income.csv', index_col=0)
        df4 = pd.concat([df1, df2, df3])
        df = df4.reindex_axis(sorted(df4.columns), axis=1)

        # 提取报表日期、总资产、净资产
        Terms = list(df.columns)
        TotalAsset = list(df.loc['总资产'].fillna('0').astype(float) / 100)
        if '净资产/(负债)' in df.index.values:
            NetAsset = list(df.loc['净资产/(负债)'].fillna('0').astype(float) / 100)
        elif '资本来源合计' in df.index.values:
            NetAsset = list(df.loc['资本来源合计'].fillna('0').astype(float) / 100)
        else:
            NetAsset = 0

        # 提取最近一期资产数据作为资产结构的数据源
        df_Asset = df.loc[['无形资产(非流动资产)', '物业、厂房及设备(非流动资产)', '附属公司权益(非流动资产)', '联营公司权益 (非流动资产)', '其他投资(非流动资产)',
                           '应收账款(流动资产)',
                           '存货(流动资产)', '现金及银行结存(流动资产)']].fillna('0').replace('--', '0').astype(float) / 100
        ##通过求和判断一期数据是否有效，从而获取最近一期Term.
        i = len(df_Asset.columns) - 1
        while i >= 0:
            # print(df_Asset.columns[i],df_Asset.ix[:,i].sum())
            if df_Asset.ix[:, i].sum() != 0:
                CurrentTerm = df_Asset.columns[i]
                break
            i -= 1
        ##获取最近一期的资产结构数据后，修改其索引，去掉(非流动资产)和((流动资产)
        s_Asset = df_Asset[CurrentTerm]
        NewIndex = []
        for item in s_Asset.index.values:
            NewIndex.append(item.replace('(非流动资产)', '').replace('(流动资产)', ''))
        s_Asset.index = NewIndex
        AssetItem = list(s_Asset.index)
        AssetData = list(s_Asset)

        # 提取最近一期的负债数据作为负债结构的数据源
        df_Debt = df.loc[['应付帐款(流动负债)', '银行贷款(流动负债)', '非流动银行贷款']].fillna('0').replace('--', '0').astype(float) / 100
        ##通过求和判断一期数据是否有效，从而获取最近一期Term.
        i = len(df_Debt.columns) - 1
        while i >= 0:
            # print(df_Asset.columns[i],df_Asset.ix[:,i].sum())
            if df_Debt.ix[:, i].sum() != 0:
                CurrentTerm = df_Debt.columns[i]
                break
            i -= 1
        ##获取最近一期的负债结构数据后，修改其索引，去掉((流动负债)
        s_Debt = df_Debt[CurrentTerm]
        NewIndex = []
        for item in s_Debt.index.values:
            NewIndex.append(item.replace('(流动负债)', ''))
        s_Debt.index = NewIndex
        DebtItem = list(s_Debt.index)
        DebtData = list(s_Debt)

        # 获取应收账款和应付账款，评估供应链地位
        s_Receivables = df.loc['应收账款(流动资产)'].fillna('0').replace('--', '0').astype(float) / 100
        s_Payables = df.loc['应付帐款(流动负债)'].fillna('0').replace('--', '0').astype(float) / 100
        Receivables = list(s_Receivables)
        Payables = list(s_Payables)

        # 获取营业额、经营盈利和除税后盈利/（亏损）并统一将季度数据换算成年度数据
        s_Incomes = df.loc['营业额'].fillna('0').replace('--', '0').astype(float) / 100
        for term in s_Incomes.index:
            if term[-5:] == '03-31':
                s_Incomes[term] = s_Incomes[term] * 4
            elif term[-5:] == '06-30':
                s_Incomes[term] = s_Incomes[term] * 2
            elif term[-5:] == '09-30':
                s_Incomes[term] = s_Incomes[term] * 4 / 3
            else:
                pass
        s_OperatingProfit = df.loc['经营盈利'].fillna('0').replace('--', '0').astype(float) / 100
        for term in s_OperatingProfit.index:
            if term[-5:] == '03-31':
                s_OperatingProfit[term] = s_OperatingProfit[term] * 4
            elif term[-5:] == '06-30':
                s_OperatingProfit[term] = s_OperatingProfit[term] * 2
            elif term[-5:] == '09-30':
                s_OperatingProfit[term] = s_OperatingProfit[term] * 4 / 3
            else:
                pass
        s_NetProfit = df.loc['除税后盈利/(亏损)'].fillna('0').replace('--', '0').astype(float) / 100
        for term in s_NetProfit.index:
            if term[-5:] == '03-31':
                s_NetProfit[term] = s_NetProfit[term] * 4
            elif term[-5:] == '06-30':
                s_NetProfit[term] = s_NetProfit[term] * 2
            elif term[-5:] == '09-30':
                s_NetProfit[term] = s_NetProfit[term] * 4 / 3
            else:
                pass
        Incomes = list(s_Incomes)
        OperatingProfit = list(s_OperatingProfit)
        NetProfit = list(s_NetProfit)

        # 获取经营、投资、融资现金净额
        df_CashFlow = df.loc[['经营业务所得之现金流入净额', '投资活动之现金流入净额', '融资活动之现金流入净额']].fillna('0').replace('--', '0').astype(
            float) / 100
        ##通过判断列的sum()值，册除无用的列
        for term in df_CashFlow.columns:
            if df_CashFlow[term].sum() == 0:
                df_CashFlow.drop(term, axis=1, inplace=True)
        ##计算每期增量现金流净额
        i = 0
        for i in range(len(df_CashFlow.columns)):
            if i > 0 and df_CashFlow.columns[i][-5:] == '12-31':
                df_CashFlow.ix[:, i] = df_CashFlow.ix[:, i] - df_CashFlow.ix[:, i - 1]
            i += 1
        ##计算每期累计现金流净额
        i = 0
        for i in range(len(df_CashFlow.columns)):
            if i > 0:
                df_CashFlow.ix[:, i] = df_CashFlow.ix[:, i] + df_CashFlow.ix[:, i - 1]
            i += 1
        CashFlowTerms = list(df_CashFlow.columns)
        OperatingCashFlowSum = list(df_CashFlow.loc['经营业务所得之现金流入净额'])
        InvestingCashFlowSum = list(df_CashFlow.loc['投资活动之现金流入净额'])
        RaisingCashFlowSum = list(df_CashFlow.loc['融资活动之现金流入净额'])
        return df, Terms, TotalAsset, NetAsset, AssetItem, AssetData, DebtItem, DebtData, Receivables, Payables, Incomes, OperatingProfit, NetProfit, CashFlowTerms, OperatingCashFlowSum, InvestingCashFlowSum, RaisingCashFlowSum
    else:
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None


if __name__ == '__main__':
    StockCode = '01751'  # input('请输入港股代码：')
    GetHkStockFinancial(StockCode)
