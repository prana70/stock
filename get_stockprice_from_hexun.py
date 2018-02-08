#coding:utf8


from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd

def GetAllPrice():
    #url='http://quote.hexun.com/stock/stock.aspx?type=2&market=0'
    url='http://quote.tool.hexun.com/hqzx/quote.aspx?type=2&market=0&sorttype=3&updown=down&page=1&count=4000&time=235904'
    #brs=wd.Firefox()#创建浏览器对象
    brs=wd.PhantomJS()
    brs.get(url)#用浏览器对象调取网页
    text=brs.page_source
    soup=bs(text,'html.parser')#解析网页
    body=soup.find('body')
    string=body.string[13:-58].replace("'",'')
    pricelines=string.split("],\n[")
    f=open('stock_price.csv','w',encoding='utf8')
    f.write('股票代码,名称,最新价,涨跌幅,昨收,今开,最高,最低,成交量,成交额,换手,振幅,量比\n')
    i=0
    for priceline in pricelines:
        f.write(priceline+'\n')
        print(str(i)+':'+priceline[0:6]+'写入 OK！')
        i=i+1
        if i>10000:
            break
    
    f.close()
    print('congratulation!全部写入完成，文件保存完毕！')
    brs.quit()
    return

if __name__=='__main__':
    GetAllPrice()
