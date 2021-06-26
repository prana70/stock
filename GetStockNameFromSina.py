#coding:utf8

import requests as rq
from bs4 import BeautifulSoup as bs


def GetStockNameFromSina(stock_code):
    url='http://money.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/ndbg.phtml'%stock_code
    header_string='''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: SINAGLOBAL=223.87.206.16_1562114457.622019; U_TRS1=00000010.7dd32ec75.5d1bf99a.93b25189; vjuids=-107c09220.16bcce450f0.0.decafdd774db8; vjlast=1562510643; SGUID=1562510648574_45952354; lxlrttp=1578733570; SCF=AvgysSyB5iE0EOBhbTWVSE87yhrGIkl3rwfEjuKUzJouvg47bIqcQ-uam3l-ch1CFNg3mCqgf1-QpF2BjgiJZwc.; sso_info=v02m6alo5qztKWRk5iljpSMpY6DpKWRk5iljoOQpY6UmK2LkpWFjZKUuJGClYKMspWFjZKUuJGilLmMkpm1mpaQvY2jiLSNk5i5jLOgt4yAwMA=; _ga=GA1.3.1062711943.1592923555; UOR=,,; UM_distinctid=173ddeaca9e118-060f8eb1e3b82e-3323765-144000-173ddeaca9fb76; __gads=ID=5e6cbbb21b1fc024-2228e9ba7ac4006e:T=1604123205:RT=1604123205:S=ALNI_MZNZPunGtPOy0rRzMFJ-br_vdCYiQ; SR_SEL=1_511; visited_uss=gb_xiacy%7Cgb_mcd%7Cgb_cost%7Cgb_fb%7Cgb_twtr%7Cgb_brk.a%7Cgb_tsla%7Cgb_goog%7Cgb_aapl%7Cgb_jd%7Cgb_baba%7Cgb_xpev%7Cgb_nio%7Cgb_kc%7Cgb_snow; hk_visited_stocks=03690%7C03888%7C01810; FIN_ALL_VISITED=sh600867%2C03690%2C03888%2C01810%2Csh601360%2Cxiacy%2Cmcd%2Ccost%2Cfb%2Ctwtr%2Cbrk.a%2Ctsla%2Cgoog%2Caapl%2Cjd%2Cbaba%2Cxpev%2Cnio%2Ckc%2Csnow; ULV=1611239201069:140:26:9::1611194028519; MONEY-FINANCE-SINA-COM-CN-WEB5=; FINA_V_S_2=sz000858,sh601360,sh600260,sz000338,sh600867,sh601318,sh603393,sz000895,sz300146,sz003027,sz002002,sh600875,sz002555,sz300770,sz002001,sz300498,sz002714,sz000661,sz002195,sz002294; Apache=183.220.95.225_1611408078.347627
Host: money.finance.sina.com.cn
If-Modified-Since: Sat, 23 Jan 2021 13:21:17 GMT
Referer: https://xueqiu.com/S/SZ000858
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36
'''

    headers={}
    for ele in header_string.strip().split('\n'):
        split_no=ele.find(':',1)
        headers[ele[:split_no]]=ele[split_no+1:].strip()

    resp=rq.get(url,headers=headers)
    soup=bs(resp.text,'lxml')

    stock_name=[x for x in soup.select('#stockName')[0].strings][0]

    return stock_name

if __name__=='__main__':
    stock_code=input('请输入股票代码：')

    print(GetStockNameFromSina(stock_code))
