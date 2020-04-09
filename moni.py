#coding:utf-8
# 本文件根据账户信息和提交的单子进行模拟清算
from __future__ import division  
# import tushare as ts
import pandas as pd
import numpy as np
import random
import os
import talib as ta
# import agsim as ag
import datetime
import allstocks as stocklib
# import engine as engine
from engine import Engine 
# from engine import Filter 

#账户操作API
import api_sim as api

# 本文件根据账户信息和信号来执行单子

allstock=stocklib.getstocks()
search = Engine()
# filtercontrol = Filter()
# print search

rcout=0;
wcout=0;
period=[]

#generate date list
#days to need
simdays=1


for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2014,8,15)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2014,9,26)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2014,11,2)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2015,1,7)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2015,4,13)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2015,7,15)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2015,9,25)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2015,12,20)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2016,1,7)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2016,1,15)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))
for daycount in range(0,simdays):
    day_lastmonth=datetime.date(2016,2,3)
    day_offset=datetime.timedelta(days=daycount)
    startday=day_lastmonth+day_offset
    period.append(str(startday))


print period

for p in period:
	print p
	lastday=p

	#要跟todaytrade里面的逻辑一样 以后可以引用同一个文件 写在一起
	#获取API账户信息
	conn=api.getcon(4001,1929)
    sleep(10*1)
    myaccount=api.getmyaccount()
    print myaccount

	#通过api返回的数据，计算当天的账户余额


	#这一块今后会与todaytrade文件里面的gettodaylist合并，因为有共同的步骤，只是日期不一样
    # print today.gettodaylist()
	
	iwanttodo={}
	for st in allstock:
		if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
			# print st
			stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			stock=stock.sort(columns='Date')
			datestr=str(lastday) #'2016-02-01'
			try:
				todayindex=list(stock['Date']).index(datestr)
				#第2天再看结果
				didays=3
				tomorow=np.array(stock[:todayindex+didays]['Close'])
				stockk=stock[:todayindex+1]
				res=search.run(st,stockk)
				if res.do:
					print st
					iwanttodo[st]=res.dotype
					print res.dotype
					#胜率计算
				else:
					pass
			except Exception, e:
				pass
				# print 'not find date'
	print iwanttodo

	#后面的逻辑就和auto-ib-new的逻辑相似了。需要好好调试

	#操作今日手动筛选的股票
	#操作今日自动筛选的股票
	today_buylist=iwanttodo
	for st in today_buylist:
        if not(st in myaccount.position) and myaccount.istrade:
        # if True:
            snum=len(today_buylist)
            if snum==0:
                snum=1
            else:
                everystockbuy=float(myaccount.buyingpower)/snum/2
                print '\n'
                print 'find a buy stock '+st
                print 'put in money:'+str(everystockbuy)
                # spr=
                stockdata = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
                stockdata=stockdata.sort(columns='Date')

                oldspr=np.array(stockdata['Close'])[-1]
                print oldspr
                spr=int(everystockbuy/oldspr)
                print 'buy price:'+str(oldspr)
                print 'buy volume:'+str(spr)
                print '\n'
                api.trade(conn,st,'BUY',spr)                
    #账户信息
    # myaccount=api.getmyaccount()
    #止损止盈
    positionmanager(myaccount)


