# -*- coding: utf-8 -*-
"""
Created on Thu May 10 17:56:12 2018

@author: hp
"""
import threading
import requests
from bs4 import BeautifulSoup
import re
import random
import pandas
import time
import datetime
import json
import pymysql
from lxml import etree
def testip(myids,proxy):
    global ips
    if len(ips)<10:
        url = "http://ip.chinaz.com/getip.aspx"
        try:
            res = requests.get(url,proxies=proxy)
            so=BeautifulSoup(res.text,'lxml')
            if myids not in so.text and '{ip:' in so.text:
                
                if proxy not in ips:
                    ips.append(proxy)
                    print(so.get_text())
        except:
            pass
def getip():
    headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWYwNDBiMjNlZDNkMWU5MTMzZTllODhiYTcxZWZmMDQ4BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUMraTBQclNKN0VjTXNUVnBIQmhFV09sNk1MUWFlWU5Qb1NzS3JOd2oxaXM9BjsARg%3D%3D--03cfdc3029f7ab0bfdddc79973642fe22c7f746b",
"Host":"www.xicidaili.com",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
            }
    proxys=[]
    global ips
    ips=[]
    n=1
    url = "http://ip.chinaz.com/getip.aspx"
    res = requests.get(url)
    myid=BeautifulSoup(res.text,'lxml')
    idm=re.findall("\d+",myid.text)
    myids='.'.join(idm)
    while(n<5):
        url = 'http://www.xicidaili.com/nn/'+str(n)
        shtml=requests.get(url,headers=headers)
        Soup=BeautifulSoup(shtml.text,'lxml')
        if 'block' in Soup:
            print('fuck')
        theurl=Soup.find_all('tr',class_="odd")
        for ur in theurl:
            proxys.append({ur.find_all('td')[5].get_text().lower(): "http://"+ur.find_all('td')[1].get_text()+":"+ur.find_all('td')[2].get_text()})
        url = "http://ip.chinaz.com/getip.aspx"
        for proxy in proxys:
            t=threading.Thread(target=testip,args=(myids,proxy,))
            t.setDaemon(False)
            t.start()
        print(n)
        n+=1
def gettable():
    getip()
    headers = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Cookie":"JSESSIONID=D4597F35B8E6080786778A2FDE85934A; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1557725450.24610.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2018-05-11; _jc_save_toDate=2018-05-10; _jc_save_wfdc_flag=dc",
    "Host":"kyfw.12306.cn",
    "If-Modified-Since":"0",
    "Referer":"https://kyfw.12306.cn/otn/leftTicket/init",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
    
            }
    locurl='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9053'
    loc=requests.get(url=locurl,headers=headers)
    kss=loc.text
    ksp=kss.split('@')[1:]
    lodic={}
    for sp in ksp:
        ps=sp.split('|')
        lodic[ps[1]]=ps[2]
    stco=lodic[stloc]
    arco=lodic[arloc]
    urls='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+stco+'&leftTicketDTO.to_station='+arco+'&purpose_codes=ADULT'
    q=requests.get(url=urls,headers=headers)
    inf=q.json()
    tinf=inf['data']['result']
    return tinf
def getinfo(ti):
        headers={
    #    "Accept":" */*",
    #"Accept-Encoding":"gzip, deflate, br",
    #"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    #"Cache-Control":"no-cache",
    "Connection":"keep-alive",
    #"Cookie":"JSESSIONID=B378AB9C2A6DB62313DB09B3F2B96B08; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1557725450.24610.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_toDate=2018-05-10; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2018-05-11",
    "Host":"kyfw.12306.cn",
    #"If-Modified-Since":"0",
    "Referer":"https://kyfw.12306.cn/otn/leftTicket/init",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
        }
        global ips
        ipp=ips[random.randint(0,len(ips)-1)]
        try:    
            uu=re.search('预订.*',ti).group().split('|')
        except:
            uu=re.search('时间.*',ti).group().split('|')
        dic={}
        dic['startT']=uu[7]
        dic['arriT']=uu[8]
        dic['spendT']=uu[9]
        if uu[10]=='Y':
            dic['Aday']=False
        else:
            dic['Aday']=True
        dic['day']=uu[12]
        dic['二等']={'num':uu[29]}
        dic['一等']={'num':uu[30]}
        dic['特等']={'num':uu[31]}
        dic['高级软卧']={'num':uu[20]}
        dic['软卧']={'num':uu[26]}
        dic['动卧']={'num':uu[32]}
        dic['硬卧']={'num':uu[27]}
        dic['硬座']={'num':uu[28]}
        dic['无座']={'num':uu[25]}
        for i in dic:
            if type(dic[i])==dict:
                if dic[i]['num']=='':
                    dic[i]['num']='-'
                elif dic[i]['num']=='无':
                    dic[i]['num']=0
                elif dic[i]['num']=='有':
                    dic[i]['num']='99+'
        tid=uu[1]
        tst=uu[15]
        tar=uu[16]
        tss=uu[34]
        purlfl='https://kyfw.12306.cn/otn/leftTicket/queryTicketPriceFL?train_no='+tid+'&from_station_no='+tst+'&to_station_no='+tar+'&seat_types='+tss+'&train_date='+date
        purl='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no='+tid+'&from_station_no='+tst+'&to_station_no='+tar+'&seat_types='+tss+'&train_date='+date
        getconnect=False
        while not getconnect:
            try:
                print('we are try1')
                ipp=ips[random.randint(0,len(ips)-1)]
                pg=requests.get(url=purlfl,headers=headers,proxies=ipp)
                pg=requests.get(url=purl,headers=headers,proxies=ipp)
                getconnect=True
            except:
                pass
        slt=2
        while('html' in pg.text):
            time.sleep(slt)
            getconnect=False
            while not getconnect:
                try:
                    print('we are try2')
                    ipp=ips[random.randint(0,len(ips)-1)]
                    pg=requests.get(url=purl,headers=headers,proxies=ipp)
                    getconnect=True
                except:
                    pass
            print(uu[2])
            slt+=1
        pj=pg.json()['data']
        dic['无座']['price']=pj['WZ']
        if 'A4' in pj:
            dic['软卧']['price']=pj['A4']
        if 'A1' in pj:
            dic['硬座']['price']=pj['A1']
        if 'O' in pj:
            dic['二等']['price']=pj['O']
        if 'A9' in pj:
            dic['特等']['price']=pj['A9']
        if 'M' in pj:
            dic['一等']['price']=pj['M']
        if 'F' in pj:
            dic['动卧']['price']=pj['F']
        if 'A3' in pj:
            dic['硬卧']['price']=pj['A3']
        if 'A6' in pj:
            dic['高级软卧']['price']=pj['A6']
        pgs.append(pg)
        print('ok!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        trains[uu[2]]=dic
def get_parameter(stid,arid,date):
    '''获取重要的参数
    date:日期，格式示例：2016-05-13
    '''
    h2={
#    'authority': 'flights.ctrip.com',
'Host':"flights.ctrip.com",
#'method': 'GET',
#'path':'/domesticsearch/search/SearchFirstRouteFlights?DCity1=JJN&ACity1=SHA&SearchType=S&DDate1=2018-05-25&IsNearAirportRecommond=0&LogToken=6f1c8706e46d4e5893becd13e8e08c5c&rk=1.8339127513657894180819&CK=AE3490D50165E667BE33817556C4C7D4&r=0.03146561908281429026319',
#'scheme': 'https',
#    "accept":" */*",
#"accept-encoding":" gzip, deflate, br",
#"accept-language":" zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
#"cookie":' Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _abtest_userid=93de7b7a-2b35-4cb0-857e-91e041f9a316; traceExt=campaign=CHNbaidu81&adid=index; MKT_Pagesource=PC; _RF1=110.83.75.175; _RSG=D8aLz73oc36bkW6Cxxdw49; _RDG=280fa67de40993282801467f09d5fdc582; _RGUID=60e6c831-fd56-420d-913a-9fbecc1a0ba5; FD_SearchHistorty={"type":"S","data":"S%24%u4E0A%u6D77%28SHA%29%24SHA%242018-05-24%24%u5317%u4EAC%28BJS%29%24BJS%24%24%24"}; appFloatCnt=1; _bfa=1.1526108798638.3f43tf.1.1526108798638.1526113558815.2.15; _bfs=1.5; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1526113650295%7D%5D; _jzqco=%7C%7C%7C%7C%7C1.1795227762.1526108806356.1526113641617.1526113650316.1526113641617.1526113650316.0.0.0.10.10; __zpspc=9.2.1526113641.1526113650.2%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfi=p1%3D101027%26p2%3D101027%26v1%3D12%26v2%3D11',
"referer":"https://flights.ctrip.com/booking/JJN-SHA-day-1.html?DDate1=2018-05-25",
"user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",

    }
    url='https://flights.ctrip.com/booking/%s-%s-day-1.html?DDate1=%s'%(stid,arid,date)
    res=requests.get(url,headers=h2)
    tree=etree.HTML(res.text)
    pp=tree.xpath('''//body/script[1]/text()''')[0].split()
    pt=tree.xpath('/html/body/script[5]/text()')[0]
    log=re.search('(?<=LogToken...)\w+',pt).group()
    CK_original=pp[3][-34:-2]
    CK=CK_original[0:5]+CK_original[13]+CK_original[5:13]+CK_original[14:]

    rk=pp[-1][18:24]
    num=random.random()*10
    num_str="%.15f"%num
    rk=num_str+rk
    r=pp[-1][27:len(pp[-1])-3]

    return rk,CK,r,log
def getflight():
    locurl='http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js'
    headers={
    "Referer":"http://www.ctrip.com/?utm_source=baidu&utm_medium=cpc&utm_campaign=baidu81&campaign=CHNbaidu81&adid=index&gclid=&isctrip=T",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
            }
    req=requests.get(url=locurl,headers=headers)
    rd=re.findall('(?<=data:")\w+\|\w+.\w+',req.text)
    locdic={}
    for i in rd:
        dsp=i.split('|')[1].split('(')
        locdic[dsp[0]]=dsp[1]
    stid=locdic[stloc]
    arid=locdic[arloc]
    rk,CK,r,log=get_parameter(stid,arid,date)
    global flyurl
    flyurl='https://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=%s&ACity1=%s&SearchType=S&DDate1=%s&IsNearAirportRecommond=0&LogToken=f93113bbbd0b40a38628984fb7d75a43&rk=1.3960476962972312162930&CK=FBF2E2CBFEA824A8A00CC44F5D5C5EC9&r=0.3539114670694109081010'%(stid,arid,date)
    #flyurl='https://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=%s&ACity1=%s&SearchType=S&DDate1=%s&IsNearAirportRecommond=03&LogToken=%s&rk=%s&CK=%s&r=%s'%(stid,arid,date,log,rk,CK,r)
    
    h2={
    #    'authority': 'flights.ctrip.com',
    'Host':"flights.ctrip.com",
    #'method': 'GET',
    #'path':'/domesticsearch/search/SearchFirstRouteFlights?DCity1=JJN&ACity1=SHA&SearchType=S&DDate1=2018-05-25&IsNearAirportRecommond=0&LogToken=6f1c8706e46d4e5893becd13e8e08c5c&rk=1.8339127513657894180819&CK=AE3490D50165E667BE33817556C4C7D4&r=0.03146561908281429026319',
    #'scheme': 'https',
    #    "accept":" */*",
    #"accept-encoding":" gzip, deflate, br",
    #"accept-language":" zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    #"cookie":' Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _abtest_userid=93de7b7a-2b35-4cb0-857e-91e041f9a316; traceExt=campaign=CHNbaidu81&adid=index; MKT_Pagesource=PC; _RF1=110.83.75.175; _RSG=D8aLz73oc36bkW6Cxxdw49; _RDG=280fa67de40993282801467f09d5fdc582; _RGUID=60e6c831-fd56-420d-913a-9fbecc1a0ba5; FD_SearchHistorty={"type":"S","data":"S%24%u4E0A%u6D77%28SHA%29%24SHA%242018-05-24%24%u5317%u4EAC%28BJS%29%24BJS%24%24%24"}; appFloatCnt=1; _bfa=1.1526108798638.3f43tf.1.1526108798638.1526113558815.2.15; _bfs=1.5; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1526113650295%7D%5D; _jzqco=%7C%7C%7C%7C%7C1.1795227762.1526108806356.1526113641617.1526113650316.1526113641617.1526113650316.0.0.0.10.10; __zpspc=9.2.1526113641.1526113650.2%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfi=p1%3D101027%26p2%3D101027%26v1%3D12%26v2%3D11',
    "referer":"https://flights.ctrip.com/booking/JJN-SHA-day-1.html?DDate1=2018-05-25",
    "user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    
        }
    flyreq=requests.get(url=flyurl,headers=h2)
    fj=flyreq.json()
    finfo=fj['fis']
    flydic={}
    for fin in finfo:
        flydic[fin['fn']]=[fin['dt'],fin['lp'],fin['at']]
    flydf=pandas.DataFrame(flydic)
    flydf=flydf.T
    nineurl='http://flights.ctrip.com/domestic/ajax/Get90DaysLowestPrice?dcity=%s&acity=%s&ddate=%s&searchType=S&r=%s'%(stid,arid,date,r)
    ninereq=requests.get(url=nineurl,headers=h2)
    nj=ninereq.json()
    njpd=pandas.DataFrame(nj)
    return njpd,flydf
def tinsert(fi):
    db = pymysql.connect("127.0.0.1", "tickets", "123", "tickets", charset='utf8' )
    cursor = db.cursor()#0--flight  1--train
    for i in fi:
        tf=stloc
        tt=arloc
        tda=date
        global sql
        sql="select tid from ticketinfo info where tid='"+i+"' and tdate='"+tda+"' limit 1"
        kc=cursor.execute(sql)
        if kc==0:
            sql="insert into ticketinfo value('"+i+"',1,'"+tda+"','"+fi[i]['startT']+"','"+fi[i]['spendT']+"','"+tf+"','"+tt+"')"
            cursor.execute(sql)
            sql="insert into tticket value('"+i+"'"
            ql=''
            qls=''
            lp=12580
            for k in fi[i].keys():
                if type(fi[i][k])==dict:
                    if(fi[i][k]['num']!='-'):
                        if float(fi[i][k]['price'].strip('¥'))<lp:
                            lp=float(fi[i][k]['price'].strip('¥'))
                        ql+=","+fi[i][k]['price'].strip('¥')
                        qls+=","+k+"="+fi[i][k]['price'].strip('¥')
                    else:
                        ql+=",null"
                        qls+=","+k+"=null"
            ql+=","+str(lp)
            qls+=",lowestp="+str(lp)
            sql+=ql+")ON DUPLICATE KEY UPDATE "+qls.replace(',','',1)
            cursor.execute(sql)
    db.commit()
    db.close()
    print('train insert over')
def finsert(fi):
    db = pymysql.connect("127.0.0.1", "tickets", "123", "tickets", charset='utf8' )
    cursor = db.cursor()#0--flight  1--train
    for i in fi:
        tf=stloc
        tt=arloc
        tda=date
        sql="select tid from ticketinfo info where tid='"+i+"' and tdate='"+tda+"' limit 1"
        k=cursor.execute(sql)
        if k==0:
            sql="insert into ticketinfo value('"+i+"',0,'"+tda+"','"+fi[i][0].split(' ')[1]+"','"+str(datetime.datetime.strptime(fi[i][2],'%Y-%m-%d %H:%M:%S')-datetime.datetime.strptime(fi[i][0],'%Y-%m-%d %H:%M:%S'))+"','"+tf+"','"+tt+"')"
            cursor.execute(sql)
        sql="insert into fticket value('"+i+"','"+str(datetime.datetime.now())+"',"+str(fi[i][1])+")"
        cursor.execute(sql)
    db.commit()
    db.close()
    print('flight insert over')
def builddb():
    db = pymysql.connect("127.0.0.1", "tickets", "123", "tickets", charset='utf8' )
    cursor = db.cursor()#0--flight  1--train
    a='create table tticket(tid varchar(15) primary key,一等 float,二等 float,动卧 float,无座 float,特等 float,硬卧 float,硬座 float,软卧 float,高级软卧 float,lowestp float,foreign key(tid) references ticketinfo(tid))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    b='create table fticket(tid varchar(15),nowday datetime,nowprice float,foreign key(tid) references ticketinfo(tid),primary key(tid,nowday))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    c='create table ticketinfo(tid varchar(15),type tinyint not null,tdate date,ttime time,sptime time,tfrom varchar(20) not null,tto varchar(20) not null,primary key(tid,tdate))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    cursor.execute(c)
    cursor.execute(b)
    cursor.execute(a)
    db.commit()
    db.close()
if __name__ == '__main__':
    qqq=datetime.timedelta(minutes = 5)
    sss=datetime.timedelta(days = 1)
    nd=datetime.datetime.now()
    sdt=datetime.datetime.now()
    while(True):
        starttime = datetime.datetime.now()
        if starttime>sdt:
            today=str(starttime).split(' ')[0]
            tds=today.split('-')
            tds[2]=str(int(tds[2])+5)
            date='-'.join(tds)
            stloc='北京'
            arloc='上海'
            njpd,flydf=getflight()
            ts=[]
            if nd<starttime:
                tinf=gettable()
                trains={}
                pgs=[]
                slt=2
                for tss in tinf:
                    #getinfo(tss)
                    t=threading.Thread(target=getinfo,args=(tss,))
                    t.setDaemon(False)
                    t.start()
                    ts.append(t)
            t=threading.Thread(target=finsert,args=(flydf.T,))
            t.setDaemon(False)
            t.start()
            for qq in ts:
                qq.join()
            print('Threading overrrrrrrrrrrrrrrrrrrrrrrrr')
            if nd<starttime:
                dd=pandas.DataFrame(trains)
                tinsert(dd)
                nd+=sss
            t.join()
            sdt=sdt+qqq
            endtime = datetime.datetime.now()
            print(endtime - starttime)