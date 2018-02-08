#coding:utf8

from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd

#url='http://quote.eastmoney.com/sz000301.html'
base_url='http://quote.eastmoney.com/'
url=''
brs=wd.PhantomJS()#创建浏览器对象
f0=open('stock_code.txt','r')#打开股票代码文件stock_code.txt
f1=open('stock_price.txt','w')#创建股票价格文件stock_code.txt
stkcds=f0.readlines()
for stkcd in stkcds:
    if stkcd[0:2]=='60':
        url=base_url+'sh'+stkcd[0:6]+'.html'
    if stkcd[0:2]=='00' or stkcd[0:2]=='30':
        url=base_url+'sz'+stkcd[0:6]+'.html'
    print(url)
    brs.get(url)#用浏览器对象调取网页
    text=brs.page_source
    soup=bs(text,'html.parser')#解析网页
    if soup.find('b',class_="header-title-c fl",id="code").string==None or soup.find('h2',class_='header-title-h2 fl' ,id='name').string==None or soup.find('span',id='day').string==None or soup.find('strong',id='price9',class_='xp1').string==None:
        pass
    else:
        stk_code=soup.find('b',class_="header-title-c fl",id="code").string
        stk_name=soup.find('h2',class_='header-title-h2 fl' ,id='name').string
        dt=soup.find('span',id='day').string[1:11]
        stk_price=soup.find('strong',id='price9',class_='xp1').string
#        print(soup.find('b',class_="header-title-c fl",id="code").string)
#        print(soup.find('h2',class_='header-title-h2 fl' ,id='name').string)
#        print(soup.find('span',id='day').string[1:11])
#        print(soup.find('strong',id='price9',class_='xp1').string)
        f1.write(stk_code+','+stk_name+','+dt+','+stk_price+'\n')
        print('写入 OK!')
f1.close()
f0.close()
brs.quit()#关闭浏览器对象

#<strong id="price9" class="xp1" style="">5.11</strong>
#<span id="day">（2017-02-09 星期四 15:41:00）</span>
#<b class="header-title-c fl" id="code">000301</b>

