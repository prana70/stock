#coding:utf8

import requests as rq
from bs4 import BeautifulSoup as bs

#下载网页
def url_downloader(url,hd,fname):
    try:
        resp=rq.get(url,headers=hd)
        f2=open('stock_data\\'+fname+'.html','w')
        f2.write(resp.text)
        f2.close()
        print(fname+' is ok!')
    except:
        f3=open('url_downloader.log','ra')
        f3.write(fname+' fail!\n')
        f3.close


urls=['http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode=','http://www.cninfo.com.cn/information/stock/incomestatements_.jsp?stockCode=','http://www.cninfo.com.cn/information/stock/cashflow_.jsp?stockCode=']
#url='http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode=600001'

#url='http://www.cninfo.com.cn/information/stock/incomestatements_.jsp?stockCode=300315'
#url='http://www.cninfo.com.cn/information/stock/cashflow_.jsp?stockCode=300315'
hd={'User-Agent':'Mozilla/5.0'}

f1=open('stock_code.txt','r')
for line in f1.readlines():
    for url in urls:
        fullurl=url+line[0:6]
        fname=line[0:6]+url[43:49]
        url_downloader(fullurl,hd,fname)
 
      




'''
#解析网页
#soup=bs(resp.text,'html.parser')


#获取网页中的表格
listtables=soup.find_all('table')
#print(type(listtables))


fn={}
#从第0个表格中提取股票简称和代码
table0=listtables[0]
strings=list(table0.stripped_strings)
i=0
for string in strings:
    if i%2==0:
        fn[string.strip().replace('：','')]=strings[i+1].strip()
    i=i+1

    



#从第2个表格中提取数据
table2=listtables[2]
listtrs=table2.contents
dts=[]
#print(type(listtrs))
#print(listtrs)
for tr in listtrs:
    if tr!='\n':
        #print(type(tr))
        #print(tr)
        listtds=tr.contents
        for td in listtds:
            if td!='\n':
                #print(td)
                listdvs=td.contents
                for dv in listdvs:
                    if dv!='\n':
                        #print(dv.string)
                        dts.append(dv.string)
#print(dts)
i=0
for dt in dts:
    if i%2==0:
        if dts[i].strip()=='科目':
            fn['报告期']=dts[i+1].strip()
        else:
            fn[dts[i].strip()]=dts[i+1].strip()
    i=i+1

for fdt in fn:
    if fdt=='报告期' or fdt=='股票代码' or fdt=='股票简称':
        pass
    else:
        if fn[fdt]=='':
            fn[fdt]=float('0')
        else:
            fn[fdt]=float(fn[fdt].replace(',',''))
    print(fdt+':'+str(fn[fdt]))
powr=(fn['应付票据']+fn['应付账款']+fn['预收款项'])/(fn['应收票据']+fn['应收账款']+fn['预付款项'])
print(fn['股票简称']+'_'+fn['股票代码']+'_'+fn['报告期']+'的经营能力：'+'%.2f'%powr)
'''

                        
            
  
    
