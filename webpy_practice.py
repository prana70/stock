# coding:utf-8
import pandas as pd
import os
import web
import stockeval as se
import ssa
import ssa_new as sn
import sys
import InstitutionalPerspective as ip
import HkStockAnalysis as hsa

type = sys.getdefaultencoding()

urls = (
    '/showassets/(.*)', 'ShowAssets',
    '/showassetsstructure/(.*)', 'ShowAssetsStructure',
    '/showassetssource/(.*)', 'ShowAssetsSource',
    '/showposition/(.*)', 'ShowPosition',
    '/showreceivablesrate/(.*)', 'ShowReceivablesRate',
    '/showinventoryrate/(.*)', 'ShowInventoryRate',
    '/showincomeprofit/(.*)', 'ShowIncomeProfit',
    '/showroe/(.*)', 'ShowROE',
    '/shownetcashflowsum/(.*)', 'ShowNetCashFlowSum',
    '/showfreecashflowsum/(.*)', 'ShowFreeCashFlowSum',
    '/showinvestmentcash/(.*)', 'ShowInvestmentCash',
    '/showraisecash/(.*)', 'ShowRaiseCash',
    '/showfundholding/(.*)', 'ShowFundHolding',
    '/showinstitutionalperspective/(.*)', 'ShowInstitutionalPerspective',
    '/', 'index',
    '/hk/', 'HkIndex',
)

app = web.application(urls, globals())


# 国内股票分析首页
class index:
    def GET(self):  # 首页
        render = web.template.render('templates')
        title = '数简财经'
        tip = '请输入股票代码：'
        button_value = '获取评估'
        return render.index(title, tip, button_value)

    def POST(self):  # 评估总览页
        # stockcode=web.input().get('stockcode')
        render = web.template.render('templates')
        stockcode, stockname, SecurityLevel, GrowthLevel, IncomeLevel, CashLevel, TradePositionLevel = se.GetTotalLevel(
            web.input().get('stockcode'))
        title = stockname + '（' + stockcode + '）-评估总览'
        labels = ['营收增长', '利润成长', '安全边际', '运营现金', '供应链地位']
        data = [IncomeLevel, GrowthLevel, SecurityLevel, CashLevel, TradePositionLevel]
        legend = '评分'

        StockPrice = se.GetStockPrice(stockcode)
        info0 = '股价：' + str('{:.2f}'.format(StockPrice)) + '元'
        shares = se.GetShares(stockcode)
        info1 = '总股本：' + str('{:.2f}'.format(shares / 100000000)) + '亿'
        NetProfit = se.GetNetProfit(stockcode)
        EPS = NetProfit / shares
        info2 = '每股收益：' + str('{:.2f}'.format(EPS)) + '元'
        NetProfitGrowth = se.GetNetProfitGrowth(stockcode)
        info3 = '净利润增长率：' + str('{:.2f}'.format(NetProfitGrowth * 100)) + '%'
        IncomeGrowth = se.GetIncomeGrowth(stockcode)
        info4 = '营业收入增长率：' + str('{:.2f}'.format(IncomeGrowth * 100)) + '%'
        InterValue = se.iv(NetProfitGrowth, EPS, 0.07, 15)
        info5 = '估值：' + str('{:.2f}'.format(InterValue)) + '元'
        FutureROI=sn.GetFutureROI(stockcode)
        info6='预期复合投资收益率：'+str('{:.2f}'.format(FutureROI * 100)) + '%'
        info7 = '业务：' + se.GetBusiness(stockcode)

        menu1 = '资产负债情况'
        menu2 = '资产结构'
        menu3 = '资产来源'
        menu4 = '供应链地位'
        menu5 = '应收账款比率'
        menu6 = '存货比率'
        menu7 = '营收情况'
        menu8 = '资产收益与负债成本'
        menu9 = '现金流对比'
        menu10 = '投资活动'
        menu11 = '融资活动'
        menu12 = '基金持股'
        menu13 = '机构评分'
        menu14='自由现金流对比'

        return render.stockeval(stockcode, title, labels, data, legend,
                                info0, info1, info2, info3, info4, info5, info6,info7,
                                menu1, menu2, menu3, menu4, menu5, menu6, menu7, menu8, menu9, menu10, menu11, menu12,
                                menu13,menu14)


class ShowAssets:  # 显示资产负债情况
    def GET(self, stockcode):
        labels, data1, data2 = sn.GetAssets(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-资产负债情况'
        legend1 = '总资产'
        legend2 = '净资产'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.showassets(title, labels, data1, data2, legend1, legend2, yAxesLabel)


class ShowAssetsStructure:  # 显示资产结构
    def GET(self, stockcode):
        labels, data = sn.GetAssetsStructure(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-资产结构'
        print(labels, data)
        # legend=''
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowAssetsStructure(title, labels, data, yAxesLabel)


class ShowAssetsSource:  # 显示资产来源
    def GET(self, stockcode):
        labels, data = sn.GetAssetsSource(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-资产来源'
        print(labels, data)
        # legend=''
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowAssetsSource(title, labels, data, yAxesLabel)


class ShowPosition:  # 显示供应链地位
    def GET(self, stockcode):
        labels, data1, data2 = sn.GetPosition(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-供应链地位'
        legend1 = '经营性资产'
        legend2 = '经营性负债'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowPosition(title, labels, data1, data2, legend1, legend2, yAxesLabel)


class ShowReceivablesRate:  # 显示应收账款比率
    def GET(self, stockcode):
        labels, data = sn.GetReceivablesRate(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-应收账款比率'
        # print(labels,data)
        # legend=''
        yAxesLabel = '（%）'
        render = web.template.render('templates')
        return render.ShowReceivablesRate(title, labels, data, yAxesLabel)


class ShowInventoryRate:  # 显示存货比率
    def GET(self, stockcode):
        labels, data = sn.GetInventoryRate(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-存货比率'
        # print(labels,data)
        # legend=''
        yAxesLabel = '（%）'
        render = web.template.render('templates')
        if labels == None:
            return '金融类企业，无法计算存货比率!'
        else:
            return render.ShowInventoryRate(title, labels, data, yAxesLabel)


class ShowIncomeProfit:  # 显示营收情况
    def GET(self, stockcode):
        labels, data1, data2, data3 = sn.GetIncomeProfit(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-营收情况'
        legend1 = '营业收入'
        legend2 = '核心利润'
        legend3 = '净利润'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowIncomeProfit(title, labels, data1, data2, data3, legend1, legend2, legend3, yAxesLabel)


class ShowROE:  # 显示资产收益率
    def GET(self, stockcode):
        labels, data1, data2, data3 = sn.GetROE(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-资产收益与负债成本'
        legend1 = '息税前资产收益率'
        legend2 = '净资产收益率'
        legend3 = '有息负债利率'
        yAxesLabel = '（%）'
        render = web.template.render('templates')
        return render.ShowROE(title, labels, data1, data2, data3, legend1, legend2, legend3, yAxesLabel)


class ShowNetCashFlowSum:  # 显示现金流对比
    def GET(self, stockcode):
        labels, data1, data2, data3 = sn.GetNetCashFlowSum(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-现金流对比'
        legend1 = '累积经营性现金净额'
        legend2 = '累积筹资性现金净额'
        legend3 = '累积投资性现金净额'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowNetCashFlowSum(title, labels, data1, data2, data3, legend1, legend2, legend3, yAxesLabel)

class ShowFreeCashFlowSum:  # 显示自由现金流对比
    def GET(self, stockcode):
        labels, data1, data2 = sn.GetFreeCashFlowSum(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-自由现金流对比'
        legend1 = '累积经营性现金净额'
        legend2 = '累积自由现金流'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowFreeCashFlowSum(title, labels, data1, data2, legend1, legend2, yAxesLabel)


class ShowInvestmentCash:  # 显示投资活动
    def GET(self, stockcode):
        labels, data1, data2 = sn.GetInvestmentCash(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-投资活动'
        legend1 = '投资支付的现金'
        legend2 = '购建固定资产、无形资产和其他长期资产支付的现金'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowInvestmentCash(title, labels, data1, data2, legend1, legend2, yAxesLabel)


class ShowRaiseCash:  # 显示融资活动
    def GET(self, stockcode):
        labels, data1, data2 = sn.GetRaiseCash(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-融资活动'
        legend1 = '吸收投资收到的现金'
        legend2 = '吸收借款收到的现金'
        yAxesLabel = '（亿元）'
        render = web.template.render('templates')
        return render.ShowRaiseCash(title, labels, data1, data2, legend1, legend2, yAxesLabel)


class ShowFundHolding:  # 显示基金持股
    def GET(self, stockcode):
        labels, data = sn.GetFundHolding(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-基金持股'
        yAxesLabel = '（家数）'
        render = web.template.render('templates')
        return render.ShowFundHolding(title, labels, data, yAxesLabel)


class ShowInstitutionalPerspective:  # 显示月度机构对股票的评分
    def GET(self, stockcode):
        labels, data = ip.GetInstitutionalPerspective(stockcode)
        title = ssa.get_stockname(stockcode) + '（%s）' % stockcode + '-机构评分'
        yAxesLabel = '（得分）'
        render = web.template.render('templates')
        return render.ShowInstitutionalPerspective(title, labels, data, yAxesLabel)


# 香港股票分析首页
class HkIndex:
    def GetHkStockName(self, StockCode):
        df = pd.read_csv(os.getcwd() + '\\market_data\\HkStockList.csv', index_col=0)
        if StockCode in list(df.index.values):
            return df.loc[StockCode]['股票名称']
        else:
            return 'it not work!'

    def GET(self):
        render = web.template.render('templates')
        title = '数简财经-港股'
        tip = '请输入股票代码：'
        button_value = '获取评估'
        return render.index(title, tip, button_value)

    def POST(self):
        StockCode = web.input().get('stockcode')
        df, Terms, TotalAsset, NetAsset = hsa.GetHkStockFinancial(StockCode)
        if Terms != None:
            StockName= self.GetHkStockName(StockCode)
            title = StockName+'('+StockCode + ')-分析'
            legend1 = '总资产'
            legend2 = '净资产'
            yAxesLabel = '（亿元）'
            labels = Terms
            data1 = TotalAsset
            data2 = NetAsset
            render = web.template.render('templates')
            return render.hkstockanalysis(title, labels, data1, data2, legend1, legend2, yAxesLabel)
        else:
            return 'stock data not exist!'


if __name__ == '__main__':
    print(type)
    app.run()
