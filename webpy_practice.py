#coding:utf-8

import web
import stockeval as se
import ssa
import ssa_new as sn
import sys
type=sys.getdefaultencoding()


urls=(
    '/showassets/(.*)','ShowAssets',
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
        
        return render.stockeval(stockcode,title,labels,data,legend,info0,info1,info2,info3,info4,info5,menu1)

class ShowAssets: #显示资产情况
    def GET(self,stockcode):
        labels,data1,data2=sn.GetAssets(stockcode)
        title=ssa.get_stockname(stockcode)+'（%s）'%stockcode+'-资产负债情况'
        legend1='总资产'
        legend2='净资产'
        yAxesLabel='亿元'
        render=web.template.render('templates')
        return render.showassets(title,labels,data1,data2,legend1,legend2,yAxesLabel)
        

if __name__=='__main__':
    print(type)
    app.run()
