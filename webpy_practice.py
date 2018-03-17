#coding:utf-8

import web
import stockeval as se
import ssa
import ssa_new as sn
import sys
type=sys.getdefaultencoding()


urls=(
    '/showassets/(.*)','ShowAssets',
    '/showassetsstructure/(.*)','ShowAssetsStructure',
    '/showassetssource/(.*)','ShowAssetsSource',
    '/showposition/(.*)','ShowPosition',
    '/showreceivablesrate/(.*)','ShowReceivablesRate',
    '/showinventoryrate/(.*)','ShowInventoryRate',
    '/showincomeprofit/(.*)','ShowIncomeProfit',
    '/showroe/(.*)','ShowROE',
    '/shownetcashflowsum/(.*)','ShowNetCashFlowSum',
    '/','index',
    )

app=web.application(urls,globals())

class index: 
    def GET(self): #首页
        render=web.template.render('templates')
        title='数简财经'
        tip='请输入股票代码：'
        button_value='获取评估'
        return render.index(title,tip,button_value)
    
    def POST(self): #评估总览页
        #stockcode=web.input().get('stockcode')
        render=web.template.render('templates')
        stockcode,stockname,SecurityLevel,GrowthLevel,IncomeLevel,CashLevel,TradePositionLevel=se.GetTotalLevel(web.input().get('stockcode'))
        title=stockname+'（'+stockcode+'）-评估总览'
        labels=['营收增长','利润成长','股价安全度','运营现金','供应链地位']
        data=[IncomeLevel,GrowthLevel,SecurityLevel,CashLevel,TradePositionLevel]
        legend='评分'

        StockPrice=se.GetStockPrice(stockcode)
        info0='股价：'+str('{:.2f}'.format(StockPrice))+'元'
        shares=se.GetShares(stockcode)
        info1='总股本：'+str('{:.2f}'.format(shares/100000000))+'亿'
        NetProfit=se.GetNetProfit(stockcode)
        EPS=NetProfit/shares
        info2='每股收益：'+str('{:.2f}'.format(EPS))+'元'
        NetProfitGrowth=se.GetNetProfitGrowth(stockcode)
        info3='净利润增长率：'+str('{:.2f}'.format(NetProfitGrowth*100))+'%'
        IncomeGrowth=se.GetIncomeGrowth(stockcode)
        info4='营业收入增长率：'+str('{:.2f}'.format(IncomeGrowth*100))+'%'
        InterValue=se.iv(NetProfitGrowth,EPS,0.07,15)
        info5='估值：'+str('{:.2f}'.format(InterValue))+'元'

        menu1='资产负债情况'
        menu2='资产结构'
        menu3='资产来源'
        menu4='供应链地位'
        menu5='应收账款比率'
        menu6='存货比率'
        menu7='营收情况'
        menu8='资产收益率'
        menu9='现金流对比'
        
        return render.stockeval(stockcode,title,labels,data,legend,
                                info0,info1,info2,info3,info4,info5,
                                menu1,menu2,menu3,menu4,menu5,menu6,menu7,menu8,menu9)

class ShowAssets: #显示资产负债情况
    def GET(self,stockcode):
        labels,data1,data2=sn.GetAssets(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产负债情况'
        legend1='总资产'
        legend2='净资产'
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.showassets(title,labels,data1,data2,legend1,legend2,yAxesLabel)
        

class ShowAssetsStructure: #显示资产结构
    def GET(self,stockcode):
        labels,data=sn.GetAssetsStructure(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产结构'
        print(labels,data)
        #legend=''
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.ShowAssetsStructure(title,labels,data,yAxesLabel)
        
class ShowAssetsSource: #显示资产来源
    def GET(self,stockcode):
        labels,data=sn.GetAssetsSource(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产来源'
        print(labels,data)
        #legend=''
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.ShowAssetsSource(title,labels,data,yAxesLabel)

class ShowPosition: #显示供应链地位
    def GET(self,stockcode):
        labels,data1,data2=sn.GetPosition(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-供应链地位'
        legend1='经营性资产'
        legend2='经营性负债'
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.ShowPosition(title,labels,data1,data2,legend1,legend2,yAxesLabel)

class ShowReceivablesRate: #显示应收账款比率
    def GET(self,stockcode):
        labels,data=sn.GetReceivablesRate(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-应收账款比率'
        #print(labels,data)
        #legend=''
        yAxesLabel='（%）'
        render=web.template.render('templates')
        return render.ShowReceivablesRate(title,labels,data,yAxesLabel)

class ShowInventoryRate: #显示存货比率
    def GET(self,stockcode):
        labels,data=sn.GetInventoryRate(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-存货比率'
        #print(labels,data)
        #legend=''
        yAxesLabel='（%）'
        render=web.template.render('templates')
        if labels==None:
            return '金融类企业，无法计算存货比率!'
        else:
            return render.ShowInventoryRate(title,labels,data,yAxesLabel)

class ShowIncomeProfit: #显示营收情况
    def GET(self,stockcode):
        labels,data1,data2=sn.GetIncomeProfit(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-营收情况'
        legend1='营业收入'
        legend2='净利润'
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.ShowIncomeProfit(title,labels,data1,data2,legend1,legend2,yAxesLabel)

class ShowROE: #显示资产收益率
    def GET(self,stockcode):
        labels,data1,data2=sn.GetROE(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产收益率'
        legend1='总资产收益率'
        legend2='净资产收益率'
        yAxesLabel='（%）'
        render=web.template.render('templates')
        return render.ShowROE(title,labels,data1,data2,legend1,legend2,yAxesLabel)


class ShowNetCashFlowSum: #显示现金流对比
    def GET(self,stockcode):
        labels,data1,data2,data3=sn.GetNetCashFlowSum(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产收益率'
        legend1='经营性现金净额'
        legend2='筹资性现金净额'
        legend3='投资性现金净额'
        yAxesLabel='（亿元）'
        render=web.template.render('templates')
        return render.ShowNetCashFlowSum(title,labels,data1,data2,data3,legend1,legend2,legend3,yAxesLabel)
       
if __name__=='__main__':
    print(type)
    app.run()
