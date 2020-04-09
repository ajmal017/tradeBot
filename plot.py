#coding:utf-8

import pandas as pd
import talib as ta
import numpy as np
import os
import matplotlib.pyplot as plt
import allstocks as stocklib

from engine import Engine 


stockprice=[]
stockpricema1=[]
stockpricema2=[]
# ta={}
allstock=stocklib.getstocks()
search = Engine()

# search.load(st,np.array(stock['Close'])).band("Li Lei").ema(15).show()

# def diff(stock):
# 	res=[0]
# 	for x in range(len(stock)-1):
# 		diffvalue=stock[x+1]-stock[x]
# 		res.append(diffvalue)
# 	# print res
# 	return res

while True:
	stocksymbol=raw_input("Input stock:")
	# print stocksymbol
	if os.path.exists("yahoo-nodejs/old/stocks/"+stocksymbol+".csv"):
		stock = pd.read_table("yahoo-nodejs/old/stocks/"+stocksymbol+".csv",sep=",",encoding='utf-8',dtype={'code':str})
		stock=stock.sort(columns='Date')
		# stock=stock[-7:]
		# print stock
		time = [x for x in range(len(np.array(stock['Close'])))]

		# print(years)
		# stockprice = np.array(stock['Close'])
		popen =np.array(stock['Open'])
		phigh =np.array(stock['High']) 
		plow =np.array(stock['Low'])  
		pclose = np.array(stock['Close']) 
		volume = np.array(stock['Volume']) 

		# stockpricediv = np.array(stock['Close'].diff())
		# stockpricema1 = ema20
		# stockpricema2 = ema60
		# stockpricema2diff=diff(stockpricema2)

		# mom = ta.MOM(np.array(stock['Close']), timeperiod=5)
		# sma30 = ta.SMA(np.array(stock['Close']),timeperiod=15)
		# sma150 = ta.SMA(np.array(stock['Close']),timeperiod=30)
		# sma150 = ta.SMA(np.array(stock['Close']),timeperiod=60)
		# sma150 = ta.SMA(np.array(stock['Close']),timeperiod=150)
		# sma = ta.SMA(np.array(stock['Close']),timeperiod=210)

		# upper, middle, lower = ta.BBANDS(pclose,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)

		# real = ta.AVGPRICE(popen, phigh, plow, pclose)
		# real = ta.TYPPRICE(phigh, plow, pclose)
		# real = ta.WCLPRICE(phigh, plow, pclose)
		# real = ta.AD(phigh, plow, pclose, volume)
		# real = ta.ADX(phigh, plow, pclose, timeperiod=14)
		# real = ta.RSI(pclose, timeperiod=14)
		# real = ta.ADX(phigh, plow, pclose, timeperiod=14)
		# real = ta.CCI(phigh, plow, pclose, timeperiod=14)
		# macd, macdsignal, macdhist = ta.MACD(pclose, fastperiod=12, slowperiod=26, signalperiod=9)
		sma = ta.SMA(pclose,timeperiod=3)
		smaa = ta.SMA(pclose,timeperiod=6)
		adxreal = ta.ADX(phigh, plow, pclose, timeperiod=14)



		# plt.plot(time[-7:], pclose[-7:], 'b')
		plt.plot(time[-70:], pclose[-70:], 'b')
		# plt.plot(time, real, 'r')
		


		# plt.plot(time[-7:], upper[-7:], 'k')
		# plt.plot(time[-7:], middle[-7:], 'k')
		# plt.plot(time[-7:], lower[-7:], 'k')

		# plt.plot(time[-7:], real[-7:], 'k')
		# plt.plot(time[-7:], real[-7:], 'k')

		# plt.plot(time[-7:], macd[-7:], 'k')
		# plt.plot(time[-7:], macdsignal[-7:], 'k')
		# plt.plot(time[-7:], macdhist[-7:], 'k')

		plt.plot(time[-70:], sma[-70:], 'k')
		plt.plot(time[-70:], smaa[-70:], 'k')

		plt.plot(time[-70:], adxreal[-70:], 'k')


	


		# plt.plot(time, mom, 'p')
		# plt.plot(time, sma30, 'g')
		# plt.plot(time, sma150, 'g')



		plt.xlabel("date")
		plt.ylabel("price")
		plt.title(stocksymbol)
		plt.legend()
		plt.show()