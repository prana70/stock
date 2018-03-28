#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import time,datetime
import os

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#从stock_type.txt中查询股票类型
def get_stock_type(stockcode):
    stock_type=''
    f0=open('stock_type.txt','r')
    for line in f0.readlines():
        if line[:6]==stockcode:
            stock_type=line[8:-1]
            break
    f0.close
    return stock_type

#从stocks.txt中查询股票简称
def get_stockname(stockcode):
    stockname=''
    f=open('stocks.txt','r')
    lines=f.readlines()
    for line in lines:
        if line[-8:-2]==stockcode:
            stockname=line[:-9].replace('*','')
            break
    f.close()
    return stockname



#用于将dataframe的数字型字符串转换成浮点数
def str_to_float(str):
    if type(str)==type('ok'):
        return float(str.replace(',',''))
    else:
        return str


#非金融类股票分析
def ordinary_stock_analyze(stockcode,stockname):

    #打开资产负债表
    #print(stockcode,stockname)
    df1=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'balancesheet.csv',index_col=0)

    #资产负债概况
    s_zzc=df1.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
    s_jzc=df1.loc['所有者权益(或股东权益)合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    pd.DataFrame({'总资产':s_zzc,'净资产':s_jzc}).plot(kind='bar',title='资产负债概况')
    fig0=plt.gcf()
    fig0.canvas.set_window_title(stockname+'--资产负债概况')
    plt.gca().yaxis.grid(True)
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left')
    plt.subplots_adjust(left=0.15,bottom=0.19)
    plt.show()


    #资产结构分析
    df2=df1.loc[['货币资金','交易性金融资产','应收票据','应收账款','预付款项',
                 '其他应收款','应收关联公司款','应收利息','应收股利','存货',
                 '一年内到期的非流动资产','其他流动资产','可供出售金融资产',
                 '长期应收款','长期股权投资','投资性房地产','固定资产','在建工程',
                 '工程物资','固定资产清理','生产性生物资产','无形资产','开发支出',
                 '商誉','长期待摊费用','递延所得税资产','其他非流动资产'],
                df1.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    fig1=plt.figure(1)
    fig1.canvas.set_window_title(stockname+'--资产结构')
    #ax1=plt.subplot(121)
    #df2.plot(kind='pie',title='资产结构',autopct='%1.1f%%', startangle=90, fontsize=9,shadow=True)
    #ax1.axis('equal')
    #ax2=plt.subplot(122)
    df2.plot(kind='barh',title='资产结构')
    plt.gca().xaxis.grid(True)
    plt.xlabel('（亿元）')
    plt.ylabel('（科目）')
    plt.subplots_adjust(left=0.29,bottom=0.19)
    plt.show()

    #负债及所有者权益分析
    df_fz=df1.loc[['短期借款','交易性金融负债','应付票据','应付账款','预收款项',
                 '应付职工薪酬','应交税费','应付利息','应付股利','其他应付款',
                 '应付关联公司款','一年内到期的非流动负债','其他流动负债',
                 '长期借款','应付债券','长期应付款','专项应付款','预计负债',
                 '递延所得税负债','其他非流动负债','实收资本(或股本)','资本公积','盈余公积',
                 '未分配利润','少数股东权益','外币报表折算价差','非正常经营项目收益调整'],
                df1.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000
    fig2=plt.figure(2)
    fig2.canvas.set_window_title(stockname+'--资产来源')
    #ax3=plt.subplot(121)
    '''
    try:
        df_fz.plot(kind='pie',title='资产来源（比例）',autopct='%1.1f%%', startangle=90, fontsize=9,shadow=True)
        ax3.axis('equal')
    except:
        pass
    '''
    #plt.subplot(122)
    df_fz.plot(kind='barh',title='资产来源',alpha=1)
    plt.gca().xaxis.grid(True)
    plt.xlabel('（亿元）')
    plt.ylabel('（科目）')
    plt.subplots_adjust(left=0.29,bottom=0.19)
    plt.show()


    #上下游关系分析

    df3=df1.loc[['应收票据','应收账款','预付款项',
                 '应付票据','应付账款','预收款项']].fillna('0')
    df4=df3.applymap(str_to_float)/100000000
    s_jyxzc=df4.loc['应收票据']+df4.loc['应收账款']+df4.loc['预付款项']#经营性资产
    s_jyxfz=df4.loc['应付票据']+df4.loc['应付账款']+df4.loc['预收款项']#经营性负债
    pd.DataFrame({'经营性资产':s_jyxzc,'经营性负债':s_jyxfz}).plot(kind='bar',title='上下游关系',alpha=1)
    plt.gca().yaxis.grid(True)
    plt.ylabel('（亿元）')
    fig3=plt.gcf()
    fig3.canvas.set_window_title(stockname+'--上下游关系')
    plt.subplots_adjust(left=0.15,bottom=0.19)
    plt.show()



    #打开利润表和现金流量表
    df5=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'incomestatements.csv',index_col=0).fillna('0').applymap(str_to_float)
    df6=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'cashflow.csv',index_col=0).fillna('0').applymap(str_to_float)

    #调整利润表，将季度数据转换成年度数据
    #print(df5.columns)
    #for column in df5.columns:
    #    print(column[:5])
    for column in df5.columns:
        if '1-3月' in column:
            df5[column]=df5[column]*4
        if '1-6月' in column:
            df5[column]=df5[column]/2*4
        if '1-9月' in column:
            df5[column]=df5[column]/3*4

    #提取经营性现金流，形成经营性现金流量表
    df_jyxxjl=df6.loc[['销售商品、提供劳务收到的现金','收到的税费返还','收到其他与经营活动有关的现金','经营活动现金流入小计','购买商品、接受劳务支付的现金','支付给职工以及为职工支付的现金','支付的各项税费','支付其他与经营活动有关的现金','经营活动现金流出小计','经营活动产生的现金流量净额']].fillna('0').applymap(str_to_float)

    #调整经营性现金流量表，将季度数据转换成年度数据
    for column in df_jyxxjl.columns:
        if '1-3月' in column:
            df_jyxxjl[column]=df_jyxxjl[column]*4
        if '1-6月' in column:
            df_jyxxjl[column]=df_jyxxjl[column]/2*4
        if '1-9月' in column:
            df_jyxxjl[column]=df_jyxxjl[column]/3*4

            
    s_yysr=df5.loc['一、营业收入']/100000000#营业收入
    s_yycb=df5.loc['减:营业成本']/100000000#营业成本
    s_yysj=df5.loc['营业税金及附加']/100000000#营业税金及附加
    s_xsfy=df5.loc['销售费用']/100000000#销售费用
    s_glfy=df5.loc['管理费用']/100000000#管理费用
    s_cwfy=df5.loc['财务费用']/100000000#财务费用
    s_jlr=df5.loc['四、净利润']/100000000#净利润


    #应收账款及存货
    s_ch=df1.loc['存货'].str.replace(',','').fillna('0').astype(float)/100000000#存货
    s_yszk=df4.loc['应收账款']#应收账款
    min_yrs=min(len(s_ch),len(s_yysr))
    fig4=plt.figure(4)
    s_yysr[-min_yrs:].plot(kind='line',color='blue',label='营业收入')
    s_yszk[-min_yrs:].plot(kind='line',color='red',label='应收账款')
    s_ch[-min_yrs:].plot(kind='line',title='应收账款-存货',grid=True,color='lightgreen')
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left',frameon=True)
    fig4.canvas.set_window_title(stockname+'--应收账款-存货')
    plt.show()


    #营业状况
    s_ml=s_yysr-s_yycb-s_yysj#毛利
    s_hxlr=s_yysr-s_yycb-s_yysj-s_xsfy-s_glfy-s_cwfy#核心利润
    fig5=plt.figure(5)
    s_yysr.plot(kind='line',color='blue',label='营业收入')
    s_ml.plot(kind='line',color='red',label='毛利')
    s_hxlr.plot(kind='line',title='营业收入-毛利-核心利润-净利润',color='green',label='核心利润')
    s_jlr.plot(kind='line',color='yellow',label='净利润',grid=True)
    #fig5=plt.gcf()
    fig5.canvas.set_window_title(stockname+'--营业收入-毛利-核心利润-净利润')
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left',frameon=True)
    plt.show()

    #营业收益率
    s_mll=s_ml/s_yysr*100#毛利率
    s_hxlrl=s_hxlr/s_yysr*100#核心利润率
    s_jlrl=s_jlr/s_yysr*100#净利润率
    fig6=plt.figure(6)
    s_mll.plot(kind='line',color='red',label='毛利率')
    s_hxlrl.plot(kind='line',title='毛利率-核心利润率-净利润率',label='核心利润率',color='blue')
    s_jlrl.plot(kind='line',label='净利润率',color='green',grid=True)
    #fig6=plt.gcf()
    fig6.canvas.set_window_title(stockname+'--毛利率-核心利润率-净利润率')
    plt.legend(loc='upper left',frameon=True)
    plt.ylabel('（%）')
    plt.show()


    #资产收益率
    min_yrs=min(len(s_jzc),len(s_jlr))
    s_zzc_1=s_zzc[-min_yrs:]
    s_jzc_1=s_jzc[-min_yrs:]
    s_jlr_1=pd.Series(s_jlr.values[-min_yrs:],index=s_jzc.index[-min_yrs:])#统一index
    s_zzcsyl=s_jlr_1/s_zzc_1*100#总资产收益率
    s_jzcsyl=s_jlr_1/s_jzc_1*100#净资产收益率
    fig91=plt.figure(91)
    s_zzcsyl.plot(kind='line',color='red',label='总资产收益率')
    s_jzcsyl.plot(kind='line',color='blue',label='净资产收益率',title='资产收益率',grid=True)
    fig91.canvas.set_window_title(stockname+'--资产收益率')
    plt.legend(loc='upper left',frameon=True)
    plt.ylabel('（%）')
    plt.show()

    #营业收入含金量
    s_yysdxj=df_jyxxjl.loc['销售商品、提供劳务收到的现金']/100000000#销售商品、提供劳务收到的现金
    fig14=plt.figure(14)
    s_yysr.plot(kind='line',label='营业收入',color='green')
    s_yysdxj.plot(kind='line',label='销售商品、提供劳务收到的现金',color='red',grid=True,title='营业收入含金量')
    fig14.canvas.set_window_title(stockname+'--营业收入含金量')
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left',frameon=True)
    plt.show()



    #核心利润含金量
    s_jyxjje=df_jyxxjl.loc['经营活动产生的现金流量净额']/100000000#经营现金净额
    s_hxlrhjl=s_jyxjje/s_hxlr*100#核心利润含金量
    fig7=plt.figure(7)
    s_jyxjje.plot(kind='line',color='red',label='经营活动产生的现金流量净额')
    s_hxlr.plot(kind='line',title='核心利润含金量',grid=True,label='核心利润',color='green')
    #fig7=plt.gcf()
    fig7.canvas.set_window_title(stockname+'--核心利润含金量')
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left',frameon=True)
    plt.show()

    #净利润含金量
    s_jytzxj=df6.loc['购建固定资产、无形资产和其他长期资产支付的现金']/100000000#经营投资现金
    s_FCF=s_jyxjje-s_jytzxj
    fig8=plt.figure(8)
    s_jlr.plot(kind='line',label='净利润',color='green')
    s_FCF.plot(kind='line',title='净利润含金量',grid=True,color='red',label='自由现金流')
    #fig8=plt.gcf()
    fig8.canvas.set_window_title(stockname+'--净利润含金量')
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left',frameon=True)
    plt.show()

    #现金流对比
    #print(df6.data)
    s_tzxjje=df6.loc['投资活动产生的现金流量净额']/100000000#投资现金净额
    #以下换算成季度数据
    s_tzxjje_value=[]
    s_tzxjje_index=[]
    s_tzxjje_lj_value=[]#计算累计额
    s_tzxjje_lj_index=[]
    for i in range(len(s_tzxjje)):
        if i>0 and  '年度' in s_tzxjje.index[i] and '1-9月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:5]+'10-12月')
        elif '1-9月' in s_tzxjje.index[i] and '1-6月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:5]+'7-9月')
        elif '1-6月' in s_tzxjje.index[i] and '1-3月' in s_tzxjje.index[i-1] and s_tzxjje.index[i][:5]==s_tzxjje.index[i-1][:5]:
            s_tzxjje_value.append(s_tzxjje[i]-s_tzxjje[i-1])
            s_tzxjje_index.append(s_tzxjje.index[i][:5]+'4-6月')
        else:
            s_tzxjje_value.append(s_tzxjje[i])
            s_tzxjje_index.append(s_tzxjje.index[i])
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
            s_czxjje_index.append(s_czxjje.index[i][:5]+'10-12月')
        elif '1-9月' in s_czxjje.index[i] and '1-6月' in s_czxjje.index[i-1] and s_czxjje.index[i][:5]==s_czxjje.index[i-1][:5]:
            s_czxjje_value.append(s_czxjje[i]-s_czxjje[i-1])
            s_czxjje_index.append(s_czxjje.index[i][:5]+'7-9月')
        elif '1-6月' in s_czxjje.index[i] and '1-3月' in s_czxjje.index[i-1] and s_czxjje.index[i][:5]==s_czxjje.index[i-1][:5]:
            s_czxjje_value.append(s_czxjje[i]-s_czxjje[i-1])
            s_czxjje_index.append(s_czxjje.index[i][:5]+'4-6月')
        else:
            s_czxjje_value.append(s_czxjje[i])
            s_czxjje_index.append(s_czxjje.index[i])
        s_czxjje_lj_value.append(sum(s_czxjje_value))#计算累计额
        s_czxjje_lj_index.append(s_czxjje_index[i])

    s_czxjje_new=pd.Series(s_czxjje_value,index=s_czxjje_index)
    s_czxjje_new.name=s_czxjje.name
    s_czxjje_lj_new=pd.Series(s_czxjje_lj_value,index=s_czxjje_lj_index)
    s_czxjje_lj_new.name=s_czxjje.name


    s_jyxjje_0=df6.loc['经营活动产生的现金流量净额']/100000000#未经年度换算的经营现金净额
    #以下换算成季度数据
    s_jyxjje_0_value=[]
    s_jyxjje_0_index=[]
    s_jyxjje_0_lj_value=[]#计算累计额
    s_jyxjje_0_lj_index=[]

    for i in range(len(s_jyxjje_0)):
        if i>0 and  '年度' in s_jyxjje_0.index[i] and '1-9月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:5]+'10-12月')
        elif '1-9月' in s_jyxjje_0.index[i] and '1-6月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:5]+'7-9月')
        elif '1-6月' in s_jyxjje_0.index[i] and '1-3月' in s_jyxjje_0.index[i-1] and s_jyxjje_0.index[i][:5]==s_jyxjje_0.index[i-1][:5]:
            s_jyxjje_0_value.append(s_jyxjje_0[i]-s_jyxjje_0[i-1])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i][:5]+'4-6月')
        else:
            s_jyxjje_0_value.append(s_jyxjje_0[i])
            s_jyxjje_0_index.append(s_jyxjje_0.index[i])
        s_jyxjje_0_lj_value.append(sum(s_jyxjje_0_value))#计算累计额
        s_jyxjje_0_lj_index.append(s_jyxjje_0_index[i])
            
    s_jyxjje_0_new=pd.Series(s_jyxjje_0_value,index=s_jyxjje_0_index)
    s_jyxjje_0_new.name=s_jyxjje_0.name
    s_jyxjje_0_lj_new=pd.Series(s_jyxjje_0_lj_value,index=s_jyxjje_0_lj_index)
    s_jyxjje_0_lj_new.name=s_jyxjje_0.name



    df_xjje=pd.DataFrame([s_jyxjje_0_lj_new,s_tzxjje_lj_new,s_czxjje_lj_new]).T
    #fig9=plt.figure(9)
    df_xjje.plot(kind='bar',title='现金流对比（累计）',grid=True,color=['red','blue','green'])
    fig9=plt.gcf()
    fig9.canvas.set_window_title(stockname+'--现金流对比（累计）')
    plt.legend(loc='upper left',frameon=True)
    plt.ylabel('（亿元）')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    #投资活动
    s_tzzfxj=df6.loc['投资支付的现金']/100000000#投资支付的现金
    #投资支付的现金换算成季度数据
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

    #经营投资现金换算成季度数据
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


    df_tzxj=pd.DataFrame([s_jytzxj_new,s_tzzfxj_new]).T
    df_tzxj.plot(kind='bar',title='投资活动',grid=True)
    plt.gcf().canvas.set_window_title(stockname+'--投资活动')
    plt.legend(loc='upper left',frameon=True)
    plt.ylabel('（亿元）')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    #筹资活动
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


    df_czxj=pd.DataFrame([s_xstzsdxj_new,s_qdjksdxj_new]).T
    df_czxj.plot(kind='bar',title='筹资活动',grid=True)
    plt.gcf().canvas.set_window_title(stockname+'--筹资活动')
    plt.legend(loc='upper left',frameon=True)
    plt.ylabel('（亿元）')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    #综合现金净额
    s_zhxjje=s_jyxjje_0+s_tzxjje+s_czxjje#综合现金净额
    #综合现金净额换算成季度数据
    s_zhxjje_value=[]
    s_zhxjje_index=[]
    s_zhxjje_lj_value=[]#累计计算
    s_zhxjje_lj_index=[]
    for i in range(len(s_zhxjje)):
        if i>0 and  '年度' in s_zhxjje.index[i] and '1-9月' in s_zhxjje.index[i-1] and s_zhxjje.index[i][:5]==s_zhxjje.index[i-1][:5]:
            s_zhxjje_value.append(s_zhxjje[i]-s_zhxjje[i-1])
            s_zhxjje_index.append(s_zhxjje.index[i][:5]+'10-12月')
        elif '1-9月' in s_zhxjje.index[i] and '1-6月' in s_zhxjje.index[i-1] and s_zhxjje.index[i][:5]==s_zhxjje.index[i-1][:5]:
            s_zhxjje_value.append(s_zhxjje[i]-s_zhxjje[i-1])
            s_zhxjje_index.append(s_zhxjje.index[i][:5]+'7-9月')
        elif '1-6月' in s_zhxjje.index[i] and '1-3月' in s_zhxjje.index[i-1] and s_zhxjje.index[i][:5]==s_zhxjje.index[i-1][:5]:
            s_zhxjje_value.append(s_zhxjje[i]-s_zhxjje[i-1])
            s_zhxjje_index.append(s_zhxjje.index[i][:5]+'4-6月')
        else:
            s_zhxjje_value.append(s_zhxjje[i])
            s_zhxjje_index.append(s_zhxjje.index[i])
        s_zhxjje_lj_value.append(sum(s_zhxjje_value))#累计计算
        s_zhxjje_lj_index.append(s_zhxjje_index[i])
        
    s_zhxjje_new=pd.Series(s_zhxjje_value,index=s_zhxjje_index)
    s_zhxjje_new.name=s_zhxjje.name

    s_zhxjje_lj_new=pd.Series(s_zhxjje_lj_value,index=s_zhxjje_lj_index)
    s_zhxjje_lj_new.name=s_zhxjje.name

    fig10=plt.figure(10)
    s_zhxjje_lj_new.T.plot(kind='bar',title='综合现金净额（累计）',grid=True)
    #fig10=plt.gcf()
    fig10.canvas.set_window_title(stockname+'--综合现金净额（累计）')
    plt.ylabel('（亿元）')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    #打开基金持仓表
    df7=pd.read_csv(os.getcwd()+'\\fund_holdings\\'+stockcode+stockname+'.csv',index_col=1).fillna('0').applymap(str_to_float)
    df8=df7.sort_index()


    s_cgsz=df8['持股市值']/10000#持股市值
    fig11=plt.figure(11)
    s_cgsz.plot(kind='bar',title='基金持股市值',grid=True)
    #fig11=plt.gcf()
    fig11.canvas.set_window_title(stockname+'--基金持股市值')
    plt.ylabel('（亿元）')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    s_cgjjjs=df8['持股基金家数']#持股基金家数
    fig12=plt.figure(12)
    s_cgjjjs.plot(kind='bar',title='持股基金家数',grid=True)
    #fig12=plt.gcf()
    fig12.canvas.set_window_title(stockname+'--持股基金家数')
    plt.ylabel('(家)')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

    s_zggltszbl=df8['占该股流通市值比例']#基金持股占流通市值比例
    fig13=plt.figure(13)
    s_zggltszbl.plot(kind='line',title='基金持股占流通市值比例',grid=True)
    #fig13=plt.gcf()
    fig13.canvas.set_window_title(stockname+'--基金持股占流通市值比例')
    plt.ylabel('（%）')
    plt.show()

def financial_stock_analyze(stockcode,stockname):
    #打开资产负债表
    df1=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'balancesheet.csv',index_col=0)

    #资产负债概况
    s_zzc=df1.loc['资产总计'].str.replace(',','').fillna('0').astype(float)/100000000#总资产
    s_jzc=df1.loc['所有者权益（或股东权益）合计'].str.replace(',','').fillna('0').astype(float)/100000000#净资产
    pd.DataFrame({'总资产':s_zzc,'净资产':s_jzc}).plot(kind='bar',title='资产负债概况')
    fig0=plt.gcf()
    fig0.canvas.set_window_title(stockname+'--资产负债概况')
    plt.gca().yaxis.grid(True)
    plt.ylabel('（亿元）')
    plt.legend(loc='upper left')
    plt.subplots_adjust(left=0.15,bottom=0.19)
    plt.show()

    #资产结构分析
    df2=df1.loc[['现金及存放同业款项',
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
        '其他资产'], df1.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000

    fig1=plt.figure(1)
    fig1.canvas.set_window_title(stockname+'--资产结构')
    #ax1=plt.subplot(121)
    #df2.plot(kind='pie',title='资产结构',autopct='%1.1f%%', startangle=90, fontsize=9,shadow=True)
    #ax1.axis('equal')
    #ax2=plt.subplot(122)
    df2.plot(kind='barh',title='资产结构')
    plt.gca().xaxis.grid(True)
    plt.xlabel('（亿元）')
    plt.ylabel('（科目）')
    plt.subplots_adjust(left=0.29,bottom=0.19)
    plt.show()

    #负债及所有者权益分析
    df_fz=df1.loc[['向中央银行借款',
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
        '非正常经营项目收益调整'],df1.columns[-1]].str.replace(',','').fillna('0').astype(float)/100000000

    fig2=plt.figure(2)
    fig2.canvas.set_window_title(stockname+'--资产来源')
    #ax3=plt.subplot(121)
    '''
    try:
        df_fz.plot(kind='pie',title='资产来源（比例）',autopct='%1.1f%%', startangle=90, fontsize=9,shadow=True)
        ax3.axis('equal')
    except:
        pass
    '''
    #plt.subplot(122)
    df_fz.plot(kind='barh',title='资产来源',alpha=1)
    plt.gca().xaxis.grid(True)
    plt.xlabel('（亿元）')
    plt.ylabel('（科目）')
    plt.subplots_adjust(left=0.29,bottom=0.19)
    plt.show()


    #打开利润表
    df5=pd.read_csv(os.getcwd()+'\stock_financial\\'+stockcode+stockname+'incomestatements.csv',index_col=0).fillna('0').applymap(str_to_float)

    #调整利润表，将季度数据转换成年度数据
    for column in df5.columns:
        if '1-3月' in column:
            df5[column]=df5[column]*4
        if '1-6月' in column:
            df5[column]=df5[column]/2*4
        if '1-9月' in column:
            df5[column]=df5[column]/3*4


    #营业收入分析
    s_yysr=df5.loc['一、营业收入']/100000000#换算成（亿元）
    s_yysr.name='营业收入'
    s_yylr=df5.loc['三、营业利润']/100000000#换算成（亿元）
    s_yylr.name='营业利润'
    s_lrze=df5.loc['四、利润总额']/100000000#换算成（亿元）
    s_lrze.name='利润总额'
    s_jlr=df5.loc['五、净利润']/100000000#换算成（亿元）
    s_jlr.name='净利润'
    s_yysr.plot(kind='line')
    s_yylr.plot(kind='line')
    s_lrze.plot(kind='line')
    s_jlr.plot(kind='line',grid=True,title='营业收入-利润')
    plt.gcf().canvas.set_window_title(stockname+'--营业收入-利润')
    plt.legend(loc='upper left')
    #plt.gca().set_xticklabels(s_yysr.index,rotation=90)
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()

 
    #分类收入分析
    df_flsr=df5.loc[['利息净收入',
         '手续费及佣金净收入',
        '证券承销业务净收入',
        '委托客户管理资产业务净收入',
        '已赚保费',
        '提取未到期责任准备金',
        '投资收益',
        '公允价值变动收益',
        '汇兑收益',
        '其他业务收入']]/100000000#换算成亿元
    df_flsr.T.plot(kind='line',title='分类收入分析',alpha=1)
    #print(df_flsr.T)
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    plt.ylabel('（亿元）')
    plt.gcf().canvas.set_window_title(stockname+'--分类收入分析')
    plt.subplots_adjust(left=0.19,bottom=0.19)
    plt.show()
    


 
if __name__=="__main__":

    stockcode=input('请输入股票代码：')
    stock_type=get_stock_type(stockcode)
    if stock_type=='普通类':
        stockname=get_stockname(stockcode)
        ordinary_stock_analyze(stockcode,stockname)
    elif stock_type=='金融类':
        stockname=get_stockname(stockcode)
        financial_stock_analyze(stockcode,stockname)
    elif stock_type=='财务数据文件不存在！':
        print('财务数据文件不存在，请运行财务数据爬取程序！')
    else:
        print('股票不存在，请更新stocks.txt和stock_type.txt文件！')









