#coding:utf8

import os
import datetime
import pandas as pd
#import append_stock_financial_from_cninfo as asf
#import append_stock_financial_from_sina as asffs
import get_financial_data

def update_financial_data(stockcode):
    file=os.getcwd()+r'\stock_financial_sina\%sbalancesheet.csv'%stockcode
    if os.path.exists(file): #判断是该股票是否有数据文件。因为数据添加一般都会三个文件，因此，此处只需要判断资产负债表即可。

        #取数据文件的表头，存入一个list，以便以后判断。
        df=pd.read_csv(file,index_col=0)
        report_dates=list(df.columns)

        #取当前日期和年份
        current_date=datetime.datetime.today().date()
        current_year=datetime.datetime.today().year

        #判断当前日期是否在一季度报告期期间，并决定是否添加数据
        q1_startDate=datetime.date(current_year,4,1)
        q1_endDate=datetime.date(current_year,6,30)
        if (current_date>=q1_startDate and current_date<=q1_endDate):
            report_date_string=str(current_year)+'-03-31'
            if report_date_string not in report_dates:
                print('添加数据'+report_date_string)
                #asf.append_stock_financial_by_stockcode(stockcode)#原巨潮信息数据添加，实限已不可用。
                #asffs.get_balancesheet(stockcode)
                #asffs.get_profitstatement(stockcode)
                #asffs.get_cashflow(stockcode)
                get_financial_data.get_financial_data_from_sina(stockcode)

        

        #判断当前日期是否在二季度报告期期间，并决定是否添加数据
        q2_startDate=datetime.date(current_year,7,1)
        q2_endDate=datetime.date(current_year,9,30)
        if (current_date>=q2_startDate and current_date<=q2_endDate):
            report_date_string=str(current_year)+'-06-30'
            if report_date_string not in report_dates:
                print('添加数据'+report_date_string)
                #asf.append_stock_financial_by_stockcode(stockcode)#原巨潮信息数据添加，实限已不可用。
                #asffs.get_balancesheet(stockcode)
                #asffs.get_profitstatement(stockcode)
                #asffs.get_cashflow(stockcode)
                get_financial_data.get_financial_data_from_sina(stockcode)


        #判断当前日期是否在三季度报告期期间，并决定是否添加数据
        q3_startDate=datetime.date(current_year,10,1)
        q3_endDate=datetime.date(current_year,12,31)
        if (current_date>=q3_startDate and current_date<=q3_endDate):
            report_date_string=str(current_year)+'-09-30'
            if report_date_string not in report_dates:
                print('添加数据'+report_date_string)
                #asf.append_stock_financial_by_stockcode(stockcode)#原巨潮信息数据添加，实限已不可用。
                #asffs.get_balancesheet(stockcode)
                #asffs.get_profitstatement(stockcode)
                #asffs.get_cashflow(stockcode)
                get_financial_data.get_financial_data_from_sina(stockcode)


        #判断当前日期是否在四季度报告期期间，并决定是否添加数据
        q4_startDate=datetime.date(current_year,1,1)
        q4_endDate=datetime.date(current_year,4,30)
        if (current_date>=q4_startDate and current_date<=q4_endDate):
            report_date_string=str(current_year-1)+'-12-31'
            if report_date_string not in report_dates:
                print('添加数据'+report_date_string)
                #asf.append_stock_financial_by_stockcode(stockcode)#原巨潮信息数据添加，实限已不可用。
                #asffs.get_balancesheet(stockcode)
                #asffs.get_profitstatement(stockcode)
                #asffs.get_cashflow(stockcode)
                get_financial_data.get_financial_data_from_sina(stockcode)

        
        
    else:
        print('添加全部数据')
        #asf.append_stock_financial_by_stockcode(stockcode)#原巨潮信息数据添加，实限已不可用。
        #asffs.get_balancesheet(stockcode)
        #asffs.get_profitstatement(stockcode)
        #asffs.get_cashflow(stockcode)
        get_financial_data.get_financial_data_from_sina(stockcode)


if __name__=='__main__':
    print('本程序仅用于函数调用，不提供直接运行！')
