#coding:utf-8

import pandas as pd
import talib as ta
import numpy as np
import os
import matplotlib.pyplot as plt
import allstocks as stocklib
import random
import logging
import ConfigParser
import datetime
import json

from engine import Engine 
# from engine import Filter 

stockprice=[]
stockpricema1=[]
stockpricema2=[]
# ta={}
allstock=stocklib.getstocks()
search = Engine()
# filtercontrol = Filter()


#config
conf=ConfigParser.RawConfigParser()
conf.read('logs/todaytrade.logs')




# search.load(st,np.array(stock['Close'])).band("Li Lei").ema(15).show()

# def diff(stock):
# 	res=[0]
# 	for x in range(len(stock)-1):
# 		diffvalue=stock[x+1]-stock[x]
# 		res.append(diffvalue)
# 	# print res
# 	return res


# iwanttodo=[]
iwanttodo={}


#废了的票 退市
stockstop=['ALNC','MEMS','ADAM','MNRPA']

def findstocks(mo):
	for st in allstock:
		if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv") and not(st in stockstop):
			# print st
			stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			stock=stock.sort(columns='Date')

			# stock=stock[-5:]
			# print stock
			# print stock.to_json()
			
			# for x in stock.index:
			# 	print x

			# upper, middle, lower = ta.BBANDS(np.array(stock['Close']),matype=ta.MA_Type.T3)

			# choose=bandfilter(st,np.array(stock['Close']))
			# print choose
			# if choose:
			# 	choose2=emafilter(st,np.array(stock['Close']))
			# 	print choose2
			# 	if choose2:
			# 		iwanttodo.append({'tick':st,'do':choose2})
			# search.band("Li Lei").ema(15).show()

			#number 1
			# if search.load(st,stock).price(2,1000).daysofpotential(60,0.15).recent(0.05,1,4).effection(4,0.4).band(20,2,2).ema(8,15).show():
			# 	iwanttodo.append(st)
			#number 2
			# #.volumeeffect(4,0.5) -放量
			# if search.load(st,stock).volume(27000*3).price(2,1000).daysofpotential(60,0.15).recent(0.05,1,4).effection(7,0.5).band(20,2,2).ema(8,15).show():
			# 	iwanttodo.append(st)
			#number 3
			#search.load(st,stock).volume(27000*3).daysofpotential(60,0.15).recent(0.05,1,4).effection(7,0.5).price(2,1000).adx().show()
			
			# calcustr='cacuer'
			# cacuer=search.load(st,stock).volume(27000*3).price(1,500) #.adx().show()
			


			# #记分器
			# #######begin#######
			# # calcustr=calcustr+'.daysofpotential(120,0.90)'
			# # calcustr=calcustr+'.recent(0.05,0.2,7)'
			# calcustr=calcustr+'.effection(5,0.4)'
			# # calcustr=calcustr+'.adx()'
			# # calcustr=calcustr+'.cci()'
			# # calcustr=calcustr+'.rsi()'
			# calcustr=calcustr+'.macd()'
			# # calcustr=calcustr+'.price(5,50)'
			# calcustr=calcustr+'.band(15,2,2)'
			# # calcustr=calcustr+'.ema(3,6)'
			# calcustr=calcustr+'.volumeeffect(4,0.5)'
			# ########over########

			# #过滤器
			# fil=filtercontrol.load(st,stock).volume(27000*3).price(5,150).effection(3,0.3).show()
			# # print fil.do


			try:
				# calcustr=calcustr+'.show()'
				# exec('res='+calcustr)

				res=search.run(st,stock)
				# res=search.run(st,stockk)

				if res.do:
					# and  (res.dotype>=5 or res.dotype<=-5)
					# iwanttodo.append(st)
					logging.info('new stock to trade  :'+st)
					iwanttodo[st]=res.dotype
			except Exception, e:
				# raise e
				pass
			# calcustr=calcustr+'.show()'
			# exec('res='+calcustr)
			# if res.do and  (res.dotype>=5 or res.dotype<=-5):
			# 	# iwanttodo.append(st)
			# 	iwanttodo[st]=res.dotype
	if mo=='auto':
		#机器定时调用程序，提前计算，需要加一天
		todaystr=str(datetime.date.today()+datetime.timedelta(days=1))
	else:
		todaystr=str(datetime.date.today())
	if not conf.has_section(todaystr):
		conf.add_section(todaystr)
	conf.set(todaystr,'trade',json.dumps(iwanttodo))
	#如何知道引擎的名字 比如 qianyuan zhuafantan  
	conf.set(todaystr,'enginename','enginename')
	with open('logs/todaytrade.logs','w') as configfile:
		conf.write(configfile)
	return iwanttodo
# search.show()



# print findstocks()
# print random.sample(list(findstocks()),5)

def gettodaylist():
	print 'i am be called'
	return random.sample(list(findstocks('auto')),3)

#
if __name__ == '__main__':
	print datetime.date.today()
	print findstocks('hand')









# while True:
# 	stocksymbol=raw_input("Input stock:")
# 	# print stocksymbol
# 	if os.path.exists("yahoo-nodejs/old/stocks/"+stocksymbol+".csv"):
# 		stock = pd.read_table("yahoo-nodejs/old/stocks/"+stocksymbol+".csv",sep=",",encoding='utf-8',dtype={'code':str})
# 		stock=stock.sort(columns='Date')
# 		# stock=stock[-7:]
# 		# print stock

# 		ema20=ta.EMA(np.array(stock['Close']),timeperiod=10)
# 		ema60=ta.EMA(np.array(stock['Close']),timeperiod=20)
# 		# upper, middle, lower = ta.BBANDS(np.array(stock['Close']),matype=ta.MA_Type.T3)
# 		# upper, middle, lower = ta.BBANDS(np.array(stock['Close']), 20, 2, 2)
# 		# obvvalue=ta.OBV(np.array(stock['volume']),np.array(stock['volume']))
# 		upper, middle, lower = ta.BBANDS(np.array(stock['Close']),timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		
# 		# print stock['close']
# 		time = [x for x in range(len(np.array(stock['Close'])))]




# 		# print(years)
# 		# stockprice = np.array(stock['Close'])
# 		popen =np.array(stock['Open'])
# 		phigh =np.array(stock['High']) 
# 		plow =np.array(stock['Low'])  
# 		pclose = np.array(stock['Close']) 
# 		volume = np.array(stock['Volume']) 

# 		# real = ta.AVGPRICE(popen, phigh, plow, pclose)
# 		# real = ta.TYPPRICE(phigh, plow, pclose)
# 		# real = ta.WCLPRICE(phigh, plow, pclose)
# 		# real = ta.AD(phigh, plow, pclose, volume)
# 		# real = ta.ADX(phigh, plow, pclose, timeperiod=14)
# 		# real = ta.RSI(pclose, timeperiod=14)

# 		stockpricediv = np.array(stock['Close'].diff())
# 		stockpricema1 = ema20
# 		stockpricema2 = ema60
# 		stockpricema2diff=diff(stockpricema2)

# 		mom = ta.MOM(np.array(stock['Close']), timeperiod=5)
# 		sma30 = ta.SMA(np.array(stock['Close']),timeperiod=15)
# 		sma150 = ta.SMA(np.array(stock['Close']),timeperiod=30)
# 		# sma150 = ta.SMA(np.array(stock['Close']),timeperiod=60)
# 		# sma150 = ta.SMA(np.array(stock['Close']),timeperiod=150)
# 		# sma = ta.SMA(np.array(stock['Close']),timeperiod=210)




# 		plt.plot(time[-7:], pclose[-7:], 'b')
# 		# plt.plot(time, real, 'r')
		


# 		plt.plot(time[-7:], upper[-7:], 'k')
# 		plt.plot(time[-7:], middle[-7:], 'k')
# 		plt.plot(time[-7:], lower[-7:], 'k')


# 		# plt.plot(time, mom, 'p')
# 		# plt.plot(time, sma30, 'g')
# 		# plt.plot(time, sma150, 'g')



# 		plt.xlabel("date")
# 		plt.ylabel("price")
# 		plt.title(stocksymbol)
# 		plt.legend()
# 		plt.show()