#coding:utf-8
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


#test history
# st='aapl'
# datestr='2016-01-04'

# if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
# 	# print st
# 	stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
# 	stock=stock.sort(columns='Date')
# 	print stock
# 	todayindex=list(stock['Date']).index(datestr)
# 	stockk=stock[:todayindex+1]
# 	# stockk=stockk.sort(columns='Date')
# 	# print stock
# 	print stockk
# 	search.load(st,stockk).price(500,1000)
#test history


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


print(period)

for p in period:
	print(p)
	lastday=p
	# res=ag.run(p)
	# iwanttodo=[]
	iwanttodo={}
	for st in allstock:
		if os.path.exists("tickets/"+st+".csv"):
			# print st
			stock = pd.read_table("tickets/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			stock=stock.sort(columns='Date')

			# print stock
			datestr=str(lastday) #'2016-02-01'
			# datestr='2015-10-01'
			# todayindex=list(stock['Date']).index(datestr)

			#9月1号的数据计算 9月2号的数据来验证


			# # print len(stock)
			# calcustr='cacuer'
			# cacuer=search.load(st,stock).volume(27000*3).price(1,500) #.adx().show()
			# #res=cacuer.adx().effection(7,0.5).show() 0.565679574791
			# #res=cacuer.adx().recent(0.05,1,4).effection(7,0.5).show() 0.533333333333
			# #######begin#######
			# # calcustr=calcustr+'.daysofpotential(120,0.90)'
			# # calcustr=calcustr+'.recent(0.05,0.2,7)'
			# calcustr=calcustr+'.effection(4,0.4)'
			# # calcustr=calcustr+'.adx()'
			# calcustr=calcustr+'.cci()'
			# calcustr=calcustr+'.macd()'
			# calcustr=calcustr+'.price(1,50)'
			# calcustr=calcustr+'.band(20,2,2)'
			# calcustr=calcustr+'.ema(8,15)'
			# # calcustr=calcustr+'.volumeeffect(5,0.3)'
			# ########over########
			# calcustr=calcustr+'.show()'
			# exec('res='+calcustr)
			# print res.do
			# # print res.dotype
			#过滤器
			# fil=filtercontrol.load(st,stock).volume(27000*3).price(5,200).effection(5,0.4).show()
			# print fil.do

			# res=search.load(st,stock).show()
			
			# res=search.run(st,stock)
			# print res.do
			# print res.dotype


			try:
				todayindex=list(stock['Date']).index(datestr)
				# print datestr
				# print todayindex
				# print stock
				# print stock['Open'][:todayindex+1]
				# print len(stock['Open'][:todayindex+1])
				#第2天再看结果
				didays=3
				tomorow=np.array(stock[:todayindex+didays]['Close'])
				stockk=stock[:todayindex+1]
				# print stockk
				# print stockk['Close'][-1]
				# print tomorow['Close'][-1]


				# res=search.load(st,stockk).show()
				res=search.run(st,stockk)

				# # search.load(st,stock)
				# # print len(stock)
				# calcustr='cacuer'
				# cacuer=search.load(st,stockk) #.adx().show()
				# # exec('res=cacuer.'+'.'.join(strgy)+'.show()')
				# # res=cacuer.show()

				# #res=cacuer.adx().effection(7,0.5).show() 0.565679574791
				# #res=cacuer.adx().recent(0.05,1,4).effection(7,0.5).show() 0.533333333333
				
				# #记分器
				# #######begin#######
				# # calcustr=calcustr+'.daysofpotential(300,0.50)'
				# # calcustr=calcustr+'.recent(0.05,0.2,7)'
				# # calcustr=calcustr+'.effection(5,0.4)'
				# # calcustr=calcustr+'.adx()'
				# # calcustr=calcustr+'.cci()'
				# # calcustr=calcustr+'.rsi()'
				# # calcustr=calcustr+'.macd()'
				# # calcustr=calcustr+'.price(5,50)'
				# calcustr=calcustr+'.band(30,2,2)'
				# # calcustr=calcustr+'.sar(0,0)'
				# # calcustr=calcustr+'.ema(35,6)'
				# # calcustr=calcustr+'.volumeeffect(4,0.5)'
				# ########over########

				# #过滤器
				# fil=filtercontrol.load(st,stockk).volume(27000*3).price(5,150).show()
				# # print fil.do





				# calcustr=calcustr+'.show()'
				# exec('res='+calcustr)



				# print res
				# print res.do
				# if search.load(st,stockk).volume(27000*3).daysofpotential(60,0.15).recent(0.05,1,4).effection(7,0.5).price(2,1000).adx().show():
				# and fil.do
				if res.do:
				# if search.load(st,stockk).volume(27000*3).price(2,1000).show():
					print(st)
					# iwanttodo.append(st)
					iwanttodo[st]=res.dotype
					print(res.dotype)
					# print '-----------------reslut:'
					# print tomorow[-2]
					# print tomorow[-1]
					# print '--------------------reslut'

					#胜率计算
					if res.dotype>=1:
						if tomorow[-1]-tomorow[-didays]>0:
							# print 'right'
							rcout=rcout+1
						else:
							# print 'wrong'
							wcout=wcout+1
					else:
						if tomorow[-1]-tomorow[-didays]<0:
							# print 'right'
							rcout=rcout+1
						else:
							# print 'wrong'
							wcout=wcout+1
					
				else:
					# print 'BAD'
					# wcout=1
					pass
			except Exception as e:
				pass
				# print 'not find date'
				# todayindex= list(stock['Date']).index('2016-02-01')
	print(iwanttodo)


print(rcout)
print(wcout)

if rcout==0 and wcout==0:
	wcout=1
print('win rate:')
print(int(rcout)/(int(wcout)+int(rcout)))


