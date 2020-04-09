# -*- coding: utf-8 -*-
from __future__ import division  
from apscheduler.schedulers.background import BackgroundScheduler

from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from time import sleep, strftime, time
from functools import partial
from ib.ext.OrderState import OrderState
from ib.opt import messagetools
import requests
import math
from pandas.io.data import DataReader
# from datetime import datetime

import datetime
import urllib2
import urllib

import random
import logging
import os
import pandas as pd
import numpy as np
import subprocess
logging.getLogger("requests").setLevel(logging.WARNING)
import talib as ta

import jinja2
import smtplib    
from email.mime.text import MIMEText  

import ConfigParser
import json

#账户操作API
import api_real as api
#whl文件 apsschudle
import todaytrade as today
import updatetoday

#http://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
#global var

#手动操作的列表  不止损不止盈
# dobyhand=['UWTI','NFLX','F']

# dobyhand={'UWTI':'越低越卖，越高越卖','RUSL':'俄罗斯做多，看情形'}
# dobyhand={'UGL':3,'UWTI':-3}
# dobyhand={'UWTI':-3}
# dobyhand={'GRBK':-3}
dobyhand={}

#每天只能选出3个股票进行操作。手动操作的股票不超过2个
#每天只能选出3个股票进行操作。手动操作的股票不超过2个
#每天只能选出3个股票进行操作。手动操作的股票不超过2个

#2.26
# today_todolist={'TESS':4,'DGLY': 4,'VNCE': 3,'RWT': 4,'SPLK': 4,'MEET': 4,'CRHM': 4,'RMP': 4,'FEYE': 4,'CZR': 3,'KURA': 3,}
# today_todolist={'VNCE': 3,'RMP': 4,'CZR': 3,}

#2.29
# {'VNCE': 3, 'ELMD': 4, 'TWM': -3, 'QLIK': 4, 'ACW': 4, 'SPPP': -3, 'SPNC': 3, 'G
# NK': 4, 'DKL': 3, 'GIII': 4, 'RMP': 4, 'VSEC': 4, 'BWZ': -3, 'PODD': 4, 'CYTX':
# 4, 'VASC': 4, 'KBR': 4, 'ALRM': 4, 'NDRO': 4, 'REV': 4, 'FPT': -3, 'NAII': 4, 'S
# OXS': -3, 'QUAD': 4, 'EGAS': -3, 'NYMX': 4, 'SPMD': 3, 'RWT': 4, 'CZR': 3, 'WIN'
# : 4, 'WIFI': 4, 'WILN': 4, 'KW': 4, 'HUBS': 4, 'HLF': 3, 'TWOU': 4, 'SPLK': 4, '
# PALL': -3}
# 3.1
# {'GIMO': 4, 'STRZA': 4, 'HDP': 4, 'TSE': 4, 'PDVW': 4, 'CNSL': 4, 'RP': 4, 'AQMS
# ': 3, 'SBGL': 4, 'PODD': 4, 'AMSC': 4, 'TRT': 4, 'SEM': 4, 'BSFT': 4, 'UXJ': 4,
# 'BDCL': 4, 'KND': 3, 'AWRE': 4, 'SPMD': 3, 'TRCO': 4, 'NVEE': 4, 'QUAD': 4, 'TAS
# R': 4, 'KEM': 4, 'RLH': 3, 'HIMX': 4, 'ABDC': 4, 'LLNW': 4, 'NVE': 4, 'FRSH': 4,
#  'STRL': 4, 'HUBS': 4, 'PFX': 3}
# 'HDP': 4,'HIMX': 4,'HUBS': 4,
# 2016-03-02
# {'PGND': 4, 'TITN': 4, 'LTRPB': 4, 'GSV': 4, 'WK': 4, 'CKEC': 4, 'HAKK': 4, 'CYA
# D': 4, 'DRN': 3, 'TROVW': 4, 'TSU': 4, 'KATE': 4, 'JSM': 4, 'STRZA': 4, 'XTLY':
# 4, 'ASMB': -3, 'KWR': 4, 'SIEN': -3, 'AMUB': 4, 'UXJ': 4, 'AYI': 4, 'PURE': 4, '
# BDCL': 4, 'IMH': -3, 'NVGS': 4, 'MGLN': 4, 'BLDR': 4, 'GWGH': 3, 'SMTC': 4, 'FBR
# C': 4, 'SPMD': 3, 'HIMX': 4, 'FOXF': 4, 'LAZ': 4, 'HUBS': 4, 'GZT': 4, 'NRP': 3,
#  'ASNA': 4}
# 'TITN': 4,'WK': 4,'TSU': 4, 'KATE': 4,'JSM': 4,'XTLY':4,'SIEN': -3,'BLDR': 4,
# 3.3
# trade = {"DPST": 4, "CGEN": 4, "EMO": 4, "PCOM": 4, "BV": 4, "ERII": 4, "VISI": 4, "SEV": 4, "SSYS": 4, "IRWD": 4, "MBI": 4, "MOBL": 4, "FHCO": 4, "ITUB": 4, "TX": 4, "TVL": 4, "IMH": -3, "CYRX": 3, "SHOP": 4, "PBT": 4, "FOR": 4, "CCIH": 4, "PRTY": 4, "AMDA": 4, "BREW": 4, "VTEB": -3, "XTLY": 4, "UNG": -3, "CPPL": 4, "SNHY": 4, "IESC": 4, "TISA": 4, "SPMD": 3, "CSAL": 4, "ACRX": 4, "CAI": 4, "MBLY": 4, "RJA": -3, "JJG": -3, "BRE": 4, "QLYS": 4}
# "CGEN": 4,"PCOM": 4,"SSYS": 4, "FHCO": 4,"ITUB": 4, "TX": 4,"SHOP": 4, "MBLY": 4,
# "CGEN": 4,"PCOM": 4, "FHCO": 4,

# 2016-03-04
# {'ILF': 4, 'ALCO': 4, 'TTP': 4, 'HOMX': 4, 'CIE': 4, 'COP': 4, 'SLAB': 4, 'CPA':
#  4, 'EMO': 4, 'JMLP': 4, 'SKY': 4, 'HMLP': 4, 'HOML': 4, 'CAI': 4, 'QLIK': 4, 'E
# GL': 4, 'IGOI': 4, 'SNHY': 4, 'BELFA': 4, 'PRFT': 4, 'CPN': 4, 'ROKA': 3, 'ANDE'
# : 4, 'CEN': 4, 'WHFBL': -3, 'LLEX': 4, 'AMD': 4, 'IESC': 4, 'XME': 4, 'RAS': 4,
# 'BKS': 4, 'SCHN': 4, 'PKOH': 4, 'GORO': 4, 'JMF': 4, 'GRBK': 4, 'WETF': 4, 'GREK
# ': 4, 'PBT': 4, 'IEZ': 4, 'SMTC': 3, 'LARE': 4, 'GML': 4, 'CCIH': 4, 'PRTY': 4,
# 'SPMD': 3, 'ATRO': 4, 'WOR': 4, 'GALE': 4, 'CDTI': 4, 'BHP': 4, 'CMF': -3, 'NDP'
# : 4, 'BLDP': 4, 'IBMJ': -3, 'RGLD': 3, 'GMT': 4, 'MLPO': 4, 'SVBL': 4, 'NPO': 4,
#  'UGP': 4, 'CSAL': 4, 'SDR': 4, 'BRAZ': 4, 'SQ': 4, 'CLDN': 4, 'REGI': 4, 'CNFR'
# : 4, 'LLNW': 4, 'WPZ': 4, 'FLTX': -3, 'FBZ': 4, 'GTT': 4, 'BRF': 4, 'GFA': 4, 'L
# AQ': 4}
# 'TTP': 4,'CIE': 4,'QLIK': 4,'XME': 4,'GRBK': 4, 
# {'QLIK': 4,'XME': 4,'GRBK': 4}

#3.8
# 'MWW': 4,'USAC': 4,'IDI': 4,'USO': 4,'MTSI': 4,
# 'EGN': 4,'TBPH': 4,'SPNE': 4,'TGP': 4,'NSM': 4,
#  'NATR': 4,'XOMA': 4,'GEF': 4,'ARRY': 4,'UTI': 4,
#  'TLYS': 4,'ENBL': 4,'TK': 4,'LOCO': 4,'YMLP': 4,
#  'RPD': 4,'MRC': 4,'SDR': 4, 'KTOS': 4,'KS': 4,
#  'RDCM': 4,'NOV': 4,'IMMU': 4,'MEOH': 4

# 'MWW': 4,'MTSI': 4,'TGP': 4,'XOMA': 4,'TLYS': 4,'TK': 4,'SDR': 4,'KTOS': 4,'KS': 4,'MEOH': 4
# 'MWW': 4,'TGP': 4,'TK': 4,'KS': 4
# 3.9
# today_todolist={'MWW': 4,'TGP': 4,'TK': 4,'KS': 4}
# 3.10

# today_todolist={'XNCR': 4,'JONE': 4,'CRDC': -3}
today_todolist={'XNCR': 4,'JONE': 4,'CRDC': -3}



#config

#global functions

# import urllib2
def get_realtime_price(symbol):
    dataurl='http://download.finance.yahoo.com/d/quotes.csv?s='+symbol+'&f=l1p2&e=.csv'
    # tests=pd.read_csv("E:/python/ibpy/trade/yahoo-nodejs/old/YAHOO-singleday/stocks/"+st+".csv",sep=",",encoding='utf-8',names=['Date','Open','High','Low','Close','Volume'])
    stock_download_url_rq = urllib2.Request(dataurl)
    stock_download = urllib2.urlopen(stock_download_url_rq).read()
    # print stock_download
    return stock_download.split(',')[0]
    # print stock_download.split(',')[1]
# get_realtime_price('aapl')
#获取账户购买力函数
#手动自动分别占比30%和70%
def getmybuyingpower(myaccount,forwho):
    buyingpower=float(myaccount.buyingpower)/2
    if forwho=='hand':
        return buyingpower*0.8
    elif forwho=='auto' :
        return buyingpower*0.2

def getnowstockprice(st):
    stockdata = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
    stockdata=stockdata.sort(columns='Date')
    #当前的价格
    oldspr=np.array(stockdata['Close'])[-1]
    return oldspr
#如果从最高点跌下来，就平仓
def if_lossing_from_highpoint(position,x):
    ifstop=True
    if os.path.exists("yahoo-nodejs/old/stocks/"+x+".csv"):
        hstock = pd.read_table("yahoo-nodejs/old/stocks/"+x+".csv",sep=",",encoding='utf-8',dtype={'code':str})
        hstock=hstock.sort(columns='Date')
        hsarray=np.array(hstock[-5:]['Close'])

        if position[x]['position']>0:
            if (np.max(hsarray)-hsarray[-1])/np.max(hsarray) >=0.05:
                ifstop=True
            else:
                ifstop=False
        else:
            if (hsarray[-1]-np.min(hsarray))/np.min(hsarray) >=0.05:
                ifstop=True
            else:
                ifstop=False

#平仓函数
def cut_position(conn,position,x):
    if position[x]['position']>0:
        # print 'find a sell stock '+x
        api.trade(conn,x,'SELL',abs(position[x]['position']))
    elif position[x]['position']<0:
        # print 'find a buy stock '+x
        #没有加abs()导致买单变成卖单
        api.trade(conn,x,'BUY',abs(position[x]['position']))
def buy(conn,st,spr):
    # print 'find a buy stock '+st
    # print 'buy price:'+str(oldspr)
    # print 'put in money:'+str(everystockbuy)
    # print 'buy volume:'+str(spr)
    api.trade(conn,st,'BUY',abs(spr))
def sell(conn,st,spr):
    # print 'find a sell stock '+st
    # print 'sell price:'+str(oldspr)
    # print 'put in money:'+str(everystockbuy)
    # print 'sell volume:'+str(spr)
    api.trade(conn,st,'SELL',abs(spr))

def accountinfo(myaccount):
    # print myaccount
    # print type(myaccount)
    # print '\n'
    print 'daytradesremaining:'+str(myaccount['daytradesremaining'])
    print 'daytradesremainingt1:'+str(myaccount['daytradesremainingt1'])
    print '\n'
    print 'my level : '+str(myaccount['mylevel'])
    print 'currentamount:'+str(myaccount['currentamount'])
    print 'unrealized:'+str(myaccount['unrealized'])
    print 'buyingpower:'+str(myaccount['buyingpower'])
    print 'stockvalue:'+str(myaccount['stockvalue'])
    print 'cashbalance:'+str(myaccount['cashbalance'])

    # print '\n'
#仓位管理系统  止损止盈
def positionmanager(myaccount):
    # print 'position'
    position=myaccount.position

    positionstr='stockvalue:'+str(myaccount['stockvalue'])+'<br>'
    positionstr=positionstr+'my level : '+str(myaccount['mylevel'])+'<br>'
    positionstr=positionstr+'daytradesremainingt1:'+str(myaccount['daytradesremainingt1'])+'<br>'
    positionstr=positionstr+'buyingpower:'+str(myaccount['buyingpower'])+'<br>'
    positionstr=positionstr+'<br>'+'<br>'+'<br>'
    moneystr=str(myaccount['currentamount'])


    niuqi_unrealized=myaccount['unrealized']
    niuqi_position=json.dumps(myaccount.position)
    niuqi_stockvalue=myaccount['stockvalue']
    niuqi_daytradesremainingt1=myaccount['daytradesremainingt1']
    niuqi_buyingpower=myaccount['buyingpower']
    niuqi_mylevel=myaccount['mylevel']
    # niuqi_buyingpower
    # niuqi_buyingpower

    #自动操作股票止损止盈策略
    #要么日内交易次数大于3，可以交易当日买的
    #要么日内交易次数不够，就不能对当日的进行止损止盈
    #除非当日亏损8%以上，而且日内交易次数等于2
    for x in myaccount['position']:
        # print x
        thisstockstr= x +'  '+ str(myaccount['position'][x]['position']) +'  '+str(round(myaccount['position'][x]['position']*myaccount['position'][x]['marketprice'],2))  +'  '+ str(round(myaccount['position'][x]['banlence'],2))+'  '+ str(myaccount['position'][x]['unrealized'])
        # print thisstockstr
        positionstr=positionstr+thisstockstr+'<br>'
        # print (x not in today_todolist.keys() and x not in dobyhand.keys())
        # print (myaccount.istrade and x in today_todolist.keys() )
        if (x not in today_todolist.keys() and x not in dobyhand.keys()) or (myaccount.istrade and x in today_todolist.keys() ):
            #1.5%止损线 #0.015
            if myaccount['position'][x]['banlence']<-0.015:
                cut_position(conn,position,x)
            #8%止赢线
            if myaccount['position'][x]['banlence']>0.08:
                cut_position(conn,position,x)
        elif myaccount.daytradesremainingt1 >=2 and x in today_todolist.keys() and myaccount['position'][x]['banlence']<-0.15:
            cut_position(conn,position,x)
    #手动操作股票止损止盈策略
    #必须有日内操作次数情况下
    #如果涨10% 或者 跌5% 就要平仓
    for x in myaccount['position']:
        if x in dobyhand.keys() and myaccount.istrade:
            #5%止损线  #应该是动态止损线 以后研究 转化为均线动态止损方式
            if myaccount['position'][x]['banlence']<-0.09:
                cut_position(conn,position,x)
            #10%止赢线
            #或者
            #比最高点下降5%就止损
            #思考：固定止盈，万一将来继续涨怎么办  不固定，跌下来，已有的利润将会丢失
            islosing=if_lossing_from_highpoint(myaccount['position'],x)
            if myaccount['position'][x]['banlence']>0.15 or (islosing and myaccount['position'][x]['banlence']>0.10):
                cut_position(conn,position,x)
    #如果不是今天操作的，也不是昨天操作的股票，
    # 没有盈利，或者盈利但是不增长了，就可以卖掉了
    #config
    conf=ConfigParser.RawConfigParser()
    conf.read('logs/todaytrade.logs')

    # print datetime.datetime.now().weekday()
    # print type(datetime.datetime.now().weekday())
    #昨天的筛选
    if datetime.datetime.now().weekday() == 0:
        #周一 0,1,2,3,4,5,6
        todaystr=str(datetime.date.today()-datetime.timedelta(days=3))
    else:
        #工作日
        todaystr=str(datetime.date.today()-datetime.timedelta(days=1))
    # print todaystr
    yest={}
    if conf.has_section(todaystr):
        #单双引号的问题
        # print conf.get(todaystr,'trade')
        yest= json.loads(conf.get(todaystr,'trade'))
    # print yest
    #今天的筛选
    for x in myaccount['position']:
        #是否可能造成日内交易中招？需要研究下  不在这些列表里面，不一定就没有日内操作
        # 必须要看当天的操作记录才行？
        if not yest.has_key(x) and x not in dobyhand.keys() and x not in today_todolist.keys():
            # print x
            if myaccount['position'][x]['banlence']<0.06:
                #平仓
                cut_position(conn,position,x)
            elif myaccount['position'][x]['banlence']>0.13:
                #平仓
                cut_position(conn,position,x)
    # print '\n'


    #更新账户数据
    # print positionstr
    #112.74.128.176:3344/account/update?currentmoney=8670&position='xxxxxxxx'&stockvalue=18670&daytradesremainingt1=3&buyingpower=6000&mylevel=1.2
    
    try:
        param={'currentmoney':moneystr,'position':positionstr}
        urlofgetdownload = "http://www.yunkongbao.com/accountapi.php?"+urllib.urlencode(param)
        rqtanzi_download = urllib2.Request(urlofgetdownload)
        tanzi_downloadd = urllib2.urlopen(rqtanzi_download).read()

        #同步到牛气
        # niuqi_unrealized
        # niuqi_position
        # niuqi_stockvalue
        # niuqi_daytradesremainingt1
        # niuqi_buyingpower
        # niuqi_mylevel
        # niuqi_buyingpower
        # niuqi_buyingpower
        param={'currentmoney':moneystr,'position':niuqi_position,'stockvalue':niuqi_stockvalue,'daytradesremainingt1':niuqi_daytradesremainingt1,'buyingpower':niuqi_buyingpower,'mylevel':niuqi_mylevel,'unrealized':niuqi_unrealized,}
        urlofgetdownload = "http://112.74.128.176:3344/account/update?"+urllib.urlencode(param)
        rqtanzi_download = urllib2.Request(urlofgetdownload)
        tanzi_downloadd = urllib2.urlopen(rqtanzi_download).read()
        #112.74.128.176:3344/account/update?currentmoney=8670&position='xxxxxxxx'&stockvalue=18670&daytradesremainingt1=3&buyingpower=6000&mylevel=1.2

        #http://127.0.0.1:3344/account/update?currentmoney=8670&position=%27xxxxxxxx%27&stockvalue=18670&daytradesremainingt1=3&buyingpower=6000&mylevel=1.2


    except Exception, e:
        print str(e)



# 这个不准确，万一操作没成功怎么办
#记录当日操作，再次操作则拒绝操作   定时清空内容 today.conf ? V  
# 这个不准确，万一操作没成功怎么办
# 这个导致一个问题：重复提交订单，本来是平仓，结果变成反做了 风险加大了！！！！


#手动操作的想平仓怎么办 V
#非要跌了才能平仓么
#如何保住这些浮盈
#订单不能重复提交 V
#仓位里面的股票要知道都是什么时候买的， X
# 要在固定额时间，比如快收盘的时候，卖掉 ?conf   X
#以上需求可以替换成  如果不是今天操作的，也不是昨天操作的股票，
# 没有盈利，或者盈利但是不增长了，就可以卖掉了
#比如 前天的，如果赚了5%就卖掉  如果赚了15%也基本要卖掉，或者在计算下趋势
#log里面要记录真实的操作记录  记录为什么买卖  原因  哪个程序逻辑
#止损止盈  结合 量能指标 SAR
#如果人工干预了自动票，则几天内不操作这个股票 V
#仓位配比根据人工股票的个数来动态调整
#快收盘的时候，熟悉的股票 跌的太凶就买，涨的太凶就空
#定时收盘前抓取数据合并，计算指标并记录可能的操作
#过了12点，就变成第二天了。。。怎么搞  可以设置本机时间？  
# 或者专门设置一个函数，获取今天的日期 通过股票数据  spy比如

# 仓位管理等程序应该也属于算法一部分，应该放置于daytrade里面一个函数里面，通过对engine的调用，进而对交易员算法的调用 
# 最终仓位管理应该放在交易员的算法库里面
# 如何在线查询账户余额和仓位，不需要登陆
#多窗口系统  重点股票预测和计算 用于手动分析和操作
# 目录需要重新设计一下，路径应该在一个配置文件里面写死
#卖完以后再买
#利用soket推送，进行交易操作推送     本机->  服务器  <-操作软件  这样的模式
#每天定时重启？免得还要关机，为时间不对

def del_today_conf():
    todayconf=ConfigParser.RawConfigParser()
    todayconf.read('conf/today.conf')
    todayconf.remove_section("did")
    with open('conf/today.conf','w') as todaytradeconfile:
        todayconf.write(todaytradeconfile)
def autogettoday():
    t=today.gettodaylist()
    print 'today at last :'
    print t
def show_account_info():
    myaccount=api.getmyaccount()
    #打印账户信息
    accountinfo(myaccount)
def watchthelist():
    #[买入，卖出]
    #还要改，加上百分比之类的
    # listt={'UWTI':[1.7,2.1]}
    listt={}
    for s in listt:
        try:
            if get_realtime_price(s)<listt[s][0]:
                #买入
                print 'watchthelist: BUY ' + s
            elif get_realtime_price(s)>listt[s][1]:
                #卖出
                print 'watchthelist: SELL ' + s
        except Exception, e:
            # raise e
            pass
        
        

scheduler = BackgroundScheduler()
#定时清除today.conf 里面的日内交易记录
# scheduler.add_job(del_today_conf,'cron',minute='*/5',second='*/30', hour='*/4',day='*')
scheduler.add_job(del_today_conf,'cron',minute='*/56',second='*/30', hour='*/23',day='*')
#定时合并当天数据
scheduler.add_job(updatetoday.update_data,'cron',minute='*/37',second='*/30', hour='*/21',day='*')
#定时计算新的股票数据，随机出3个买入
scheduler.add_job(autogettoday,'cron',minute='*/51',second='*/30', hour='*/21',day='*')
#定时计算关注列表的股票，是否产生交易机会： 收盘时候 超跌  超涨 的
scheduler.add_job(watchthelist,'cron',minute='*/45',second='*/30', hour='*/21',day='*')
#定时显示仓位
scheduler.add_job(show_account_info,'cron',hour='*/2',day='*')


scheduler.start()

#找回各种账号密码啊。。。
#http://www.yunkongbao.com/accountapi.php?currentmoney=1000&position=xxxxxxxxxxxxxxxxxxxxxxxxxxxx%3Cbr%3Exxxxxxxxxxxxxxxxxxxxxxxxxxxx%3Cbr%3Exxxxxxxxxxxxxxxxxxxxxxxxxxxx
#http://www.yunkongbao.com/accountinfo.php


#主程序
if __name__ == '__main__':
    try:
        conn=api.getcon(4001,1929)
        #获取信息中，不延时将取不到数据
        sleep(30*1) 
        

        myaccount=api.getmyaccount()
        # print myaccount
        #打印账户信息
        accountinfo(myaccount)


        #主要是获取账户信息和止损止盈之类的
        trun=True
        while trun:
            #好像没用 
            # td=datetime.date.today()
            # if td.hour>2 and td.hour<10:
            #     trun=False
            #操作今日手动筛选的股票
            for st in dobyhand.keys():
                if not(st in myaccount.position) and myaccount.istrade:
                    #操作的股票个数
                    snum=len(dobyhand.keys())
                    if snum==0:
                        snum=1
                    else:
                        #根据买的个数，均分购买力
                        everystockbuy=getmybuyingpower(myaccount,'hand')/snum
                        #当前的价格
                        oldspr=getnowstockprice(st)
                        #计算买的量
                        spr=int(everystockbuy/oldspr)
                        #根据筛选的股票结果，根据正负来决定买卖
                        #还要根据操作的类型来操作，比如是越跌越买还是越涨越卖
                        #现在先根据正负来定  0就是要平仓
                        if dobyhand[st]>0:
                            buy(conn,st,spr)
                        elif dobyhand[st]<0:
                            sell(conn,st,spr)
                        elif dobyhand[st] == 0:
                            cut_position(conn,myaccount.position,st)

            #操作今日自动筛选的股票
            for st in today_todolist.keys():
                if not(st in myaccount.position) and myaccount.istrade:
                    #操作的股票个数
                    snum=len(today_todolist.keys())
                    if snum==0:
                        snum=1
                    else:
                        #根据买的个数，均分购买力
                        everystockbuy=getmybuyingpower(myaccount,'auto')/snum
                        #当前的价格
                        oldspr=getnowstockprice(st)
                        #计算买的量
                        spr=int(everystockbuy/oldspr)
                        #根据筛选的股票结果，根据正负来决定买卖
                        if today_todolist[st]>0:
                            buy(conn,st,spr)
                        elif today_todolist[st]<0:
                            sell(conn,st,spr)
                elif st in myaccount.position and myaccount.istrade:
                    #注意！！！！！这里会造成死循环！！！！！
                    #股票操作以后，重启系统，就会走入这个逻辑
                    #自动筛选的股票已经在账户有了，则需要看是否需要平仓
                    #相乘得负数  说明方向不对，需要平仓 或者 买卖
                    # if today_todolist[st]*myaccount['position'][st]['position']<0:
                        # cut_position(myaccount['position'],st)
                    pass
            #获取账户信息
            myaccount=api.getmyaccount()
            #打印账户信息
            # accountinfo(myaccount)
            #止损止盈
            positionmanager(myaccount)
            #每隔5秒判断一次
            sleep(20*1)
            # sleep(60*1*60*2)
    except (KeyboardInterrupt, ):
        print('\nKeyboard interrupt.\n')


