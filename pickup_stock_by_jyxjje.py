#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import time,datetime
import os
import scipy as sp

import matplotlib as mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['font.serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#将dataframe的数字型字符串转换成浮点数
def str_to_float(str):
    if type(str)==type('ok'):
        return float(str.replace(',',''))
    else:
        return str
    
def error(f,x,y):
    return sp.sum((f(x)-y)**2)

def jyxjje_analyze(file):
    try:
        df=pd.read_csv(os.getcwd()+'\\stock_financial\\'+file,index_col=0).fillna('0').applymap(str_to_float)/100000000
        s_jyxjje=df.loc['经营活动产生的现金流量净额']
        if len(s_jyxjje)<5:
            return None,None

        s_jyxjje_value=[]
        s_jyxjje_index=[]
        s_jyxjje_lj_value=[]#计算累计额
        s_jyxjje_lj_index=[]

        for i in range(len(s_jyxjje)):
            if i>0 and  '年度' in s_jyxjje.index[i] and '1-9月' in s_jyxjje.index[i-1] and s_jyxjje.index[i][:5]==s_jyxjje.index[i-1][:5]:
                s_jyxjje_value.append(s_jyxjje[i]-s_jyxjje[i-1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5]+'10-12月')
            elif '1-9月' in s_jyxjje.index[i] and '1-6月' in s_jyxjje.index[i-1] and s_jyxjje.index[i][:5]==s_jyxjje.index[i-1][:5]:
                s_jyxjje_value.append(s_jyxjje[i]-s_jyxjje[i-1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5]+'7-9月')
            elif '1-6月' in s_jyxjje.index[i] and '1-3月' in s_jyxjje.index[i-1] and s_jyxjje.index[i][:5]==s_jyxjje.index[i-1][:5]:
                s_jyxjje_value.append(s_jyxjje[i]-s_jyxjje[i-1])
                s_jyxjje_index.append(s_jyxjje.index[i][:5]+'4-6月')
            else:
                s_jyxjje_value.append(s_jyxjje[i])
                s_jyxjje_index.append(s_jyxjje.index[i])
            s_jyxjje_lj_value.append(sum(s_jyxjje_value))#计算累计额
            s_jyxjje_lj_index.append(s_jyxjje_index[i])
                
        s_jyxjje_new=pd.Series(s_jyxjje_value,index=s_jyxjje_index)
        s_jyxjje_new.name=s_jyxjje.name
        s_jyxjje_lj_new=pd.Series(s_jyxjje_lj_value,index=s_jyxjje_lj_index)
        s_jyxjje_lj_new.name=s_jyxjje.name

        #print(s_jyxjje_lj_new/max(s_jyxjje_lj_new))


        x=[a for a in range(len(s_jyxjje_lj_new))]
        #y=[b for b in s_jyxjje_lj_new]
        y=s_jyxjje_lj_new/max(abs(s_jyxjje_lj_new))*100

        #plt.scatter(x,y)

        fp1,residuals,rank,sv,rcond=sp.polyfit(x,y,1,full=True)
        #print('Model parameters: %s'%fp1)
        f1=sp.poly1d(fp1)
        #print(error(f1,x,y))

        #fx=sp.linspace(0,x[-1],1000)
        #plt.plot(fx,f1(fx))

        #plt.show()
        return fp1[0],error(f1,x,y)
    except:
        return None,None

if __name__=='__main__':
    filelist=os.listdir(os.getcwd()+'\\stock_financial')
    #print(filelist)
    f=open('pickup_stock_by_jyxjje.csv','w')
    f.write('股票代码,股票简称,现金成长系数,误差\n')
    i=0
    for file in filelist:
        if 'cashflow' in file:
            stockcode=file[:6]
            stockname=file[6:-12]
            xl,error_=jyxjje_analyze(file)
            print(i,stockcode,stockname,xl,error_)
            print('*'*50)
            if xl!=None: # and xl>=2.5 and error_<=5100:
                f.write(str(stockcode)+','+stockname+','+str(xl)+','+str(error_)+'\n')
            i+=1
        if i>100000:
            break
    f.close()
