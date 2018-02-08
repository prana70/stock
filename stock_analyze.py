#coding:utf8

#import os
from bs4 import BeautifulSoup as bs

#获取stock_data目录下的html文件列表
#listhtmls=os.listdir('stock_data\\')

#打开stock_code.txt提取股票代码
ff=open('stocks.txt','r')
stkcds=ff.readlines()
ff.close()

#根据目的解析html文件并提取相应数据
f0=open('stock_powr.csv','w')
f0.write('股票代码,股票简称,报告期,上下游关系比率,现金比率,核心利润率%,核心利润含金量\n')
print('写入数据表头 OK!')
#m=0
for stkcd in stkcds:
    try:
#        m=m+1
#        if m==10:
#            break
        fn={}
        fn['股票简称']=stkcd[0:-9]#获取股票代码及价格
        fn['股票代码']=stkcd[-8:-2]
        f2=open('stock_price.txt','r')#获取股票价格
        fn['股价']=''
        for line in f2.readlines():
            els=line.split(',')
            if els[0]==stkcd[-8:-2]:
                fn['股价']=els[2]
                break
        fl_names=[stkcd[-8:-2]+'balanc',stkcd[-8:-2]+'income',stkcd[-8:-2]+'cashfl']#获取三大财务报表数据
        for fl_name in fl_names:
            f1=open('stock_data\\'+fl_name+'.html','r')
            text=f1.read()
            f1.close()
            soup=bs(text,'html.parser')#解析网页
            listtables=soup.find_all('table')#获取网页中的表格
            if len(listtables)<3:
                pass
            else:
                table2=listtables[2]#从第2个表格中提取数据写入dts[]
                listtrs=table2.contents
                dts=[]
                for tr in listtrs:
                    if tr!='\n':
                        listtds=tr.contents
                        for td in listtds:
                            if td!='\n':
                                listdvs=td.contents
                                for dv in listdvs:
                                    if dv!='\n':
                                        dts.append(dv.string)
                i=0
                for dt in dts: #将dts[]中的数据转化为字典fn
                    if i%2==0:
                        if dts[i].strip()=='科目':
                            fn[fl_name[-6:]+'报告期']=dts[i+1].strip()
                        else:
                            fn[dts[i].strip()]=dts[i+1].strip()
                    i=i+1
    #分析开墚
        stock_name=''#获取股票代码及价格
        stock_code=''
        balanc_report_period=''
        f_debt=0  #定义经营性负债
        f_asset=0 #定义经营性资产
        operating_leverage=0#定义经营性杠杆比率
        shares=0#定义股本
        cash=0#定义货币资金
        stock_price=0#定义股票价格
        cash_per_share=0#定义每股现金
        cash_ratio=0#定义现金比率

        income=0#定义营业收入
        expense=0#定义支出
        operating_net_cash_flow=0#定义经营性现金净流
        core_earnings=0#定义核心利润
        core_earnings_rate=0#定义核心利润率
        core_earnings_value=0


        
        for fdt in fn:
            if '报告期' in fdt or fdt=='股票代码' or fdt=='股票简称':
                if fdt=='balanc报告期':
                    balanc_report_period=fn[fdt]
                if fdt=='股票代码':
                    stock_code=fn[fdt]
                if fdt=='股票简称':
                    stock_name=fn[fdt]
            else:
                if fn[fdt]=='':
                    fn[fdt]=float('0')
                else:
                    fn[fdt]=float(fn[fdt].replace(',',''))
            #print(fdt+':'+str(fn[fdt]))
            if fdt in ['应付票据','应付账款','应付帐款','应付款项','预收款项','预收账款','预收帐款']:#累加经营性负债
                f_debt=f_debt+fn[fdt]
            if fdt in ['应收票据','应收账款','应收帐款','应收款项','预付款项','预付账款','预收付款']:#累加经营性资产
                f_asset=f_asset+fn[fdt]
            if '股本' in fdt:#获取股本
                shares=fn[fdt]
            if '货币资金' in fdt:#获取货币资金
                cash=fn[fdt]
            stock_price=fn['股价']#获取股价

            if '营业收入' in fdt:#获取营业收入
                income=fn[fdt]
            if fdt in ['营业税金及附加','业务及管理费','销售费用','管理费用','财务费用'] or '营业支出' in fdt or '营业成本' in fdt:#计算支出
                expense=expense+fn[fdt]
            if '经营活动产生的现金流量净额' in fdt:#获取经营净现金流
                operating_net_cash_flow=fn[fdt]

        core_earnings=income-expense#计算核心利润
        core_earnings_rate=core_earnings/income*100 #计算核心利润率
        core_earnings_value=operating_net_cash_flow/core_earnings#计算核心利润含金量
        

            
        if f_asset==0:#计算经营性杠杆比率
            f_asset=1
        operating_leverage=f_debt/f_asset
        if shares!=0:#计算每股现金
            cash_per_share=cash/shares
        if stock_price!=0:
            cash_ratio=cash_per_share/stock_price
            
        f0.write(stock_code+','+stock_name+','+balanc_report_period+','+'%.2f'%operating_leverage+','+'%.2f'%cash_ratio+','+'%.2f'%core_earnings_rate+','+'%.2f'%core_earnings_value+'\n')
        print(stock_code+' 写入数据 ok！')
    except:
        print('写入失败！')
f0.close()
print('写入完成！！！！')
