#coding:utf-8
# import tushare as ts
from __future__ import division  
import pandas as pd
import numpy as np
import random
import os
import talib as ta

# import agsim as ag
import datetime

import allstocks as stocklib
# import engine as engine
# from engine import Engine 
from lib import Engine 
from lib import Filter 

from itertools import combinations

# def querystockbydate(parray,datestr):
# 	index=1
# 	for x in parray["Date"]:
# 		if x==datestr :
# 		 	# print(parray["Date"].index(datestr)
# 		 	# print(index
# 		 	return index
# 		index=index+1

# stocks=ts.get_stock_basics()
# stocks=""


allstock=stocklib.getstocks()
# search = engine.Engine()
search = Engine()
filtercontrol = Filter()

# print(allstock
# print(search



# st='aapl'
# datestr='2016-01-04'

# if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
# 	# print(st
# 	stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
# 	stock=stock.sort(columns='Date')
# 	print(stock
# 	todayindex=list(stock['Date']).index(datestr)
# 	stockk=stock[:todayindex+1]
# 	# stockk=stockk.sort(columns='Date')
# 	# print(stock
# 	print(stockk
# 	search.load(st,stockk).price(500,1000)



# rcout=1;
# wcout=1;

goodlist=[]

#generate date list
#days to need

period=[]

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


print(period)

strategy=['volumeeffect(4,0.5)','ema(3,6)','band(20,2,2)','ad()','mfi()','rsi()','kdj()','macd()','adx()','cci()','daysofpotential(60,0.15)','recent(0.05,1,4)','effection(7,0.5)']

strategylist=[]

# #不定数目
# # #list(combinations(list(strategy),t))
# for t in xrange(2,len(strategy)+1):
# 	strategylist.extend(list(combinations(list(strategy),t)))

#2个
strategylist=list(combinations(list(strategy),5))

print(strategylist)

for strgy in strategylist:
	rcout=1;
	wcout=1;
	print('res=cacuer.'+'.'.join(strgy)+'.show()')
	for p in period:
		# print(p
		lastday=p
		# res=ag.run(p)
		# iwanttodo=[]
		iwanttodo={}

		for st in allstock:
			if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
				# print(st
				# st='UWTI'
				stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
				stock=stock.sort(columns='Date')


		# st='AAPL'
		# stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding="utf-8",dtype={"code":str})
		# stock=stock.sort(columns='Date')
				# print(stock
				datestr=str(lastday) #'2016-02-01'
				# datestr='2015-10-01'
				# todayindex=list(stock['Date']).index(datestr)

				#9月1号的数据计算 9月2号的数据来验证

				
				# calcustr='cacuer'
				# cacuer=search.load(st,stock) #.adx().show()

				#记分器
				#######begin#######
				# calcustr=calcustr+'.daysofpotential(120,0.90)'
				# calcustr=calcustr+'.recent(0.05,0.2,7)'
				# calcustr=calcustr+'.effection(4,0.4)'
				# calcustr=calcustr+'.adx()'
				# calcustr=calcustr+'.cci()'
				# # calcustr=calcustr+'.obv()'
				# calcustr=calcustr+'.macd()'
				# calcustr=calcustr+'.price(1,50)'
				# calcustr=calcustr+'.band(20,2,2)'
				# calcustr=calcustr+'.ema(8,15)'
				# calcustr=calcustr+'.volumeeffect(5,0.3)'
				# ########over########
				#过滤器
				# fil=filtercontrol.load(st,stock).volume(27000*3).price(5,150).show()
				# print(fil.do

				# calcustr=calcustr+'.show()'
				# exec('res='+calcustr)
				# print(res.do
				# print(res.dotype

				try:
					todayindex=list(stock['Date']).index(datestr)
					# print(todayindex
					# print(stock
					# print(stock['Open'][:todayindex+1]
					# print(len(stock['Open'][:todayindex+1])
					#第2天再看结果
					didays=2
					tomorow=np.array(stock[:todayindex+didays]['Close'])
					stockk=stock[:todayindex+1]
					# print(type(stockk)
					# print(stockk['Close'][-1]
					# print(tomorow['Close'][-1]

					# search.load(st,stock)
					# print(len(stock)
					# if search.load(st,stock).volume(27000*3).daysofpotential(60,0.15).recent(0.05,1,4).effection(7,0.5).price(2,1000).adx().show():
					cacuer=search.load(st,stockk) #.adx().show()
					#记分器
					#######begin#######
					exec('res=cacuer.'+'.'.join(strgy)+'.show()')
					# ########over########
					#过滤器
					fil=filtercontrol.load(st,stockk).volume(27000*3).price(5,150).show()
					# print(fil.do
					# print(res
					if res.do  and (res.dotype>=1 or res.dotype<=-1) and fil.do:
						# print(st
						iwanttodo[st]=res.dotype
						# print('-----------------reslut:'
						# print(tomorow[-2]
						# print(tomorow[-1]
						# print('--------------------reslut'
						
						#胜率计算
						if res.dotype>=1:
							if tomorow[-1]-tomorow[-didays]>0:
								# print('right'
								rcout=rcout+1
							else:
								# print('wrong'
								wcout=wcout+1
						else:
							if tomorow[-1]-tomorow[-didays]<0:
								# print('right'
								rcout=rcout+1
							else:
								# print('wrong'
								wcout=wcout+1
						
					else:
						# print('BAD'
						# wcout=1
						pass
				except Exception as e:
					pass
					# print('not find date'
					# todayindex= list(stock['Date']).index('2016-02-01')
		# print(iwanttodo
	print(int(rcout)/(int(wcout)+int(rcout)))
	if int(rcout)/(int(wcout)+int(rcout))>0.5:
		print('good found')
		goodlist.append({"sg":strgy,"win":int(rcout)/(int(wcout)+int(rcout))})
		# print(rcout
		# print(wcout
		print(int(rcout)/(int(wcout)+int(rcout)))
			# for s in iwanttodo:
			# 	print(s
			# 	print(stock['Close'][todayindex+2]

