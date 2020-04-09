#coding:utf-8
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
# sys.path.append("..")
import pandas as pd
import talib as ta
import numpy as np
import os

import matplotlib.pyplot as plt
# import allstocks as stocklib

# sys.path.append('..')
#导入基本量化库
# import api_sim as api
#导入基本数学计算库
# import api_sim as api
#导入技术分析库
# import indexlib as lib

# 本引擎只产生信号
# sys.path.append("..")
# sys.path.append("../")

# from pub.publib import Engine
# from pub.publib import Filter
# search = Engine()
# filtercontrol = Filter()

import pub.publibpure as techindex



#允许python 的dict数据类型 可以通过点的方式来取数据
class DottableDict(dict):   
	def __init__(self, *args, **kwargs):     
		dict.__init__(self, *args, **kwargs)     
		self.__dict__ = self  
	def allowDotting(self, state=True):     
		if state:       
			self.__dict__ = self   
		else:       
			self.__dict__ = dict() 

#过滤器
class Filter:
	stocks=[]
	st=''

	def before(self):
		if not(self.do):
			return self

	def load(self,st,priceclose):
		self.priceopen = np.array(priceclose['Open'])
		self.pricehigh = np.array(priceclose['High'])
		self.priceclose = np.array(priceclose['Close'])
		self.pricelow = np.array(priceclose['Low'])
		self.volumeseries = np.array(priceclose['Volume'])
		self.st = st
		# self.do = True
		# self.mydo={"do":True,"dotype":0}

		#允许python 的dict数据类型 可以通过点的方式来取数据
		self.mydo=DottableDict()
		self.mydo.allowDotting()
		self.mydo.do=True
		# self.mydo.dotype=0
		# print 'now : '+st
		# print self.priceclose
		# print 'load data'
		return self

	def price(self,pmin,pmax):
		pricelist = self.priceclose
		# print 'price'
		# print pricelist[-1]
		# print self.do

		if self.mydo.do:
			if pricelist[-1]>=pmin and  pricelist[-1]<=pmax :
				# print '大于500'
				self.mydo.do=True
				# self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				# print 'xiao于500'
				self.mydo.do=False
				# self.mydo.dotype=0 #sell
		return self
	def effection(self,days,effect):
		pricelist = self.priceclose
		
		if self.mydo.do:
			allbodong=0
			starttoend=abs(pricelist[-1]-pricelist[-days])
			for x in xrange(1,days):
				allbodong=allbodong+abs(pricelist[-x-1]-pricelist[-x])
			if starttoend/allbodong>effect:
				self.mydo.do=True
				# self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self	
	def volume(self,vol):
		volumelist = self.volumeseries
		pricelist = self.priceclose
		
		if self.mydo.do:
			if volumelist[-1]*pricelist[-1]>vol:
				self.mydo.do=True
				# self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self
	def show(self):
		# print self.stocks
		# print 'done'
		# return {'do':self.do}
		return self.mydo

#记分器
class Engine:
	stocks=[]
	st=''

	def before(self):
		if not(self.do):
			return self

	def load(self,st,priceclose):
		self.priceopen = np.array(priceclose['Open'])
		self.pricehigh = np.array(priceclose['High'])
		self.priceclose = np.array(priceclose['Close'])
		self.pricelow = np.array(priceclose['Low'])
		self.volumeseries = np.array(priceclose['Volume'])
		self.st = st
		# self.do = True
		# self.mydo={"do":True,"dotype":0}

		# d = DottableDict()
		# d.allowDotting() 
		#允许python 的dict数据类型 可以通过点的方式来取数据
		self.mydo=DottableDict()
		self.mydo.allowDotting()
		self.mydo.do=True
		self.mydo.dotype=0
		# print 'now : '+st
		# print self.priceclose
		# print 'load data'
		return self

	def adx(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		# real = ta.ADX(high, low, close, timeperiod=14)
		smacloses = ta.SMA(close,timeperiod=3)
		smaclosel = ta.SMA(pclose,timeperiod=6)
		real = ta.ADX(high, low, close, timeperiod=14)

		#判断曲线形状
		allbodong=0
		starttoend=abs(real[-1]-real[-5])
		for x in xrange(1,5):
			allbodong=allbodong+abs(real[-x-1]-real[-x])
		# if starttoend/allbodong>0.7 and real[-1]-real[-5]<0:
		# 	self.do=True

		if self.mydo.do:
			# if real[-1]>20 and real[-1]<40:
			if smacloses>smaclosel and real[-1]>25 and starttoend/allbodong>0.6 and real[-1]-np.min(real[-5]) >0:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif smacloses<smaclosel and real[-1]>25 and starttoend/allbodong>0.6 and real[-1]-np.max(real[-5]) >0:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self		
	def cci(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		real = ta.CCI(high, low, close, timeperiod=14)

		if self.mydo.do:
			if np.min(real[-3])<-100 and real[-1]>-100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif np.max(real[-3])>100 and real[-1]<100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self	
	def macd(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		#DIFF  DEA  DIFF-DEA  
		macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
		#1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 
		#2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
		#
		if self.mydo.do:
			if macd[-1]>0 and macdsignal[-1]>0 and macd[-1]>macdsignal[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif macd[-1]<0 and macdsignal[-1]<0 and macd[-1]<macdsignal[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
				# print 'sell'
			else:
				self.mydo.do=False
		return self	
	def kdj(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
	   	#1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
	  		#2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号。#待修改
	   	#下跌趋势中，K小于D，K线向下跌破D线时，为卖出信号。#待修改
		#K,D
	   	slowk, slowd = ta.STOCH(high,low,close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
	   	if self.mydo.do:
			if slowk[-1]>=90 or slowd[-1]>=80:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			elif slowk[-1]<=10 or slowd[-1]<=20:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self
	def rsi(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		#参数14,5
	   	slowreal = ta.RSI(close, timeperiod=14)
	   	fastreal = ta.RSI(close, timeperiod=5)
	   	if self.mydo.do:
			if slowreal[-1]>=80 or fastreal[-1]>=80:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			elif slowk[-1]<=20 or fastreal[-1]<=20:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			# elif (slowk[-2]<50 and slowk[-1]>50) or (fastreal[-2]<50 and fastreal[-1]>50 ):
			# 	self.do=True
			# elif  (slowk[-2]>50 and slowk[-1]<50) or (fastreal[-2]>50 and fastreal[-1]<50 ):
			# 	self.do=False
			else:
				self.mydo.do=False
		return self

	def mfi(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		volume = self.volumeseries

		real = ta.MFI(high, low, close, volume, timeperiod=14)
		
		if self.mydo.do:
			if (real[-2]<20 and real[-1]>20):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif  (real[-2]>80 and real[-1]<80):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self	

	def ad(self):
		popen = self.priceopen
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		volume = self.volumeseries

		real = ta.AD(high, low, close, volume)
		
		if self.mydo.do:
			#背离
			if close[-1] >np.max(close[-10]) and real[-2]>real[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #buy
			elif close[-1] < np.min(close[-10]) and real[-2]<real[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif popen[-1]<close[-1] and real[-2]<real[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif popen[-1]>close[-1] and real[-2]>real[-1]:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self	


	# def obv(self):
	# 	close = self.priceclose
	# 	low = self.pricelow
	# 	high = self.pricehigh
	# 	volume = self.volumeseries
	# 	# print type(self.volumeseries)
	# 	real = ta.OBV(close,volume)		
	# 	if self.mydo.do:
	# 		if real[-2]<real[-1] and close[-2]<close[-1]:
	# 			self.mydo.do=True
	# 			self.mydo.dotype=1 #buy
	# 		elif  real[-2]<real[-1] and close[-2]>close[-1]:
	# 			self.mydo.do=True
	# 			self.mydo.dotype=1 #buy
	# 		elif  real[-2]>real[-1] and close[-2]<close[-1]:
	# 			self.mydo.do=True
	# 			self.mydo.dotype=0 #sell
	# 		else:
	# 			self.mydo.do=False
	# 	return self	

	def cci(self):
		close = self.priceclose
		low = self.pricelow
		high = self.pricehigh
		real = ta.CCI(high, low, close, timeperiod=14)

		if self.mydo.do:
			if real[-1]>real[-5] and np.max(real[-3])<100 and real[-1]>100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif real[-1]<real[-5] and np.min(real[-3])>100 and real[-1]<100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			if real[-1]>real[-5] and np.max(real[-3])<-100 and real[-1]>-100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif real[-1]<real[-5] and np.min(real[-3])>-100 and real[-1]<-100:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self	

	def volumeeffect(self,days,effect):
		volumelist = self.volumeseries
		close = self.priceclose
		
		if self.mydo.do:
			allbodong=0
			starttoend=abs(volumelist[-1]-volumelist[-days])
			for x in xrange(1,days):
				allbodong=allbodong+abs(volumelist[-x-1]-volumelist[-x])
			if starttoend/allbodong>effect:
				if volumelist[-1]>=volumelist[-3] and close[-1]>=close[-3]:
					#放量上涨
					self.mydo.do=True
					self.mydo.dotype=self.mydo.dotype+1 #buy
				elif volumelist[-1]<volumelist[-3] and close[-1]<close[-3]:
					#放量下跌
					self.mydo.do=True
					self.mydo.dotype=self.mydo.dotype-1 #sell
				else:
					self.mydo.do=False
			elif starttoend/allbodong<effect:
				self.mydo.do=False
				# self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self
	def volume(self,vol):
		volumelist = self.volumeseries
		pricelist = self.priceclose
		
		if self.mydo.do:
			if volumelist[-1]*pricelist[-1]>vol:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self
	def daysofpotential(self,days,percent):
		pricelist = self.priceclose
		
		if self.mydo.do:
			tmax=np.max(pricelist[-days:])
			# tmin=np.min(pricelist[-60:])
			if (tmax-pricelist[-1])/pricelist[-1]>=percent:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
				# self.mydo.dotype=self.mydo.dotype-1 #sell
		return self
# (sma30[-1]-sma30[-4])/sma30[-4]>0.05
	def recent(self,pmin,pmax,days):
		pricelist = self.priceclose
		
		if self.mydo.do:
			p=abs(pricelist[-1]-pricelist[-days])/pricelist[-days]
			if p>=pmin and p<=pmax :
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self
	def price(self,pmin,pmax):
		pricelist = self.priceclose
		# print 'price'
		# print pricelist[-1]
		# print self.do

		if self.mydo.do:
			if pricelist[-1]>=pmin and  pricelist[-1]<=pmax :
				# print '大于500'
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				# print 'xiao于500'
				self.mydo.do=False
				# self.mydo.dotype=0 #sell
		return self
	def effection(self,days,effect):
		pricelist = self.priceclose
		
		if self.mydo.do:
			allbodong=0
			starttoend=abs(pricelist[-1]-pricelist[-days])
			for x in xrange(1,days):
				allbodong=allbodong+abs(pricelist[-x-1]-pricelist[-x])
			if starttoend/allbodong>effect:
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			else:
				self.mydo.do=False
		return self
	def band(self,days,up,down):
		pricelist = self.priceclose

		if self.mydo.do:
			upper, middle, lower = ta.BBANDS(pricelist,timeperiod=days,nbdevup=up,nbdevdn=down,matype=0)
			stockprice = pricelist

			#通过方差判定是沿着哪条线走的
			dis=[]
			l1=0
			l2=0
			l3=0
			for s in pricelist[-days:]:
				for u in upper[-days:]:
					l1=l1+abs(s-u)
			dis.append(l1)
			for s in pricelist[-days:]:
				for m in middle[-days:]:
					l2=l2+abs(s-m)
			dis.append(l2)
			for s in pricelist[-days:]:
				for l in lower[-days:]:
					l3=l3+abs(s-l)
			dis.append(l3)

			line=''
			if dis.index(np.min(dis))==0:
				line='up'
			elif dis.index(np.min(dis))==1:
				line='mid'
			elif dis.index(np.min(dis))==2:
				line='low'

			# print line


			choose=[]
			if stockprice[-1] > middle[-1] and np.min(stockprice[-days]) > np.min(middle[-days]):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif stockprice[-1] < middle[-1]  and np.max(stockprice[-days]) < np.max(middle[-days]):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			elif line=='up' and np.max(stockprice[-days]) < np.max(upper[-days]):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif line=='mid' :
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			elif line=='low' and np.min(stockprice[-days]) > np.min(lower[-days]):
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			#缩口状态还没写
			else:
				self.mydo.do=False

		# self.before()
		# self.do=False
		# self.stocks.append(st)
		return self

	def ema(self,shorttime,longtime):
		# self.name = name
		pricelist=self.priceclose
		sma30 = ta.EMA(pricelist,timeperiod=shorttime)
		sma150 = ta.EMA(pricelist,timeperiod=longtime)
		
		# print 'ema'
		
		if self.mydo.do:
			if sma30[-1] > sma150[-1] :
				# stocks.append(self.st)
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif sma30[-1] < sma150[-1] :
				# stocks.append(self.st)
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
			
		# self.before()
		# self.do=True
		# self.stocks.append(st)
		return self
	def sar(self,acceleration=0,maximum=0):
		high=self.pricehigh
		low=self.pricelow
		close=self.priceclose

		real = ta.SAR(high, low,acceleration,maximum)
		if self.mydo.do:
			if close[-1] > real[-1] :
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype+1 #buy
			elif close[-1] < real[-1]  :
				self.mydo.do=True
				self.mydo.dotype=self.mydo.dotype-1 #sell
			else:
				self.mydo.do=False
		return self
	def show(self):
		# print self.stocks
		# print 'done'
		# return {'do':self.do}
		return self.mydo




########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################
########################新引擎#####################################


# import pub.publibpure as techindex


#需要考虑的几点
#
#所有策略自由组合，并可以批量自动运算策略，不论是过滤还是打分，不论是类方式还是函数方式
#开发自由性，可以把指标的计算结果跟均线的数据进行比较
#可以综合各个模型的数据结果，综合判断
#

# 计分器 过滤器 自由组合指标（必须取一个新的指标名字  等同与EMA  MACD 之类的）   能不能来源于一个类？最后统一包装一下
# 因为都是根据数据，返回买卖信号。根据类型不同，返回不同的格式


# 建造者模式
# class StockSelf():
# 	_symbol=''
# 	_open=[]
# 	_high=[]
# 	_close=[]
# 	_low=[]
# 	_volume=[]
# 	mydo=DottableDict()
# 	mydo.allowDotting()
# 	mydo.do=True
# 	mydo.dotype=0

def getpricelist(selfobj):
	# print selfobj._symbol
	return selfobj._symbol,selfobj._open,selfobj._high,selfobj._close,selfobj._low,selfobj._volume
def buy(selfobj):
	selfobj.mydo.do=True
	selfobj.mydo.dotype=selfobj.mydo.dotype+1 #buy
def sell(selfobj):
	selfobj.mydo.do=True
	selfobj.mydo.dotype=selfobj.mydo.dotype-1 #sell
def undo(selfobj):
	selfobj.mydo.do=False
def ifgopass(selfobj):
	if not selfobj.mydo.do:
		return selfobj
	else:
		pass
# def ifgopass(selfobj):
# 	if not selfobj.mydo.do:
# 		return self
# 	else:
# 		pass
# def buy(selfobj):
# 	selfobj.mydo.do=True
# 	selfobj.mydo.dotype=selfobj.mydo.dotype+1 #buy
# def sell(selfobj):
# 	selfobj.mydo.do=False
# 	selfobj.mydo.dotype=selfobj.mydo.dotype-1 #sell


####不管是过滤器还是打分器，都返回 do.type   和  do   ,
# 具体需不需要判断这些属性，则是后面的逻辑


# techindex

class Dealler:
	# _symbol=''
	# _open=[]
	# _high=[]
	# _close=[]
	# _low=[]
	# _volume=[]
	# mydo=DottableDict()
	# def __init__(self):
	# 	self.mydo.allowDotting()
	# 	self.mydo.do=True
	# 	self.mydo.dotype=0
	def load(self,symbol,priceclose):
		# st=StockSelf()
		self.mydo=DottableDict()
		self.mydo.allowDotting()
		self.mydo.do=True
		self.mydo.dotype=0
		self._open=np.array(priceclose['Open'])
		self._high=np.array(priceclose['High'])
		self._close=np.array(priceclose['Close'])
		self._low=np.array(priceclose['Low'])
		self._volume=np.array(priceclose['Volume'])
		self._symbol=symbol
		# self.stockself=st
		return self
	def recent(self,pmin,pmax,days):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)
		p=abs(close[-1]-close[-days])/close[-days]
		if p>=pmin and p<=pmax :
			buy(self)
		else:
			sell(self)
		return self
	def effection(self,days,effect):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)
		
		allbodong=0
		starttoend=abs(close[-1]-close[-days])
		for x in xrange(1,days):
			allbodong=allbodong+abs(close[-x-1]-close[-x])
		if starttoend/allbodong>effect:
			buy(self)
		else:
			undo(self)
		return self	
	def ema(self,shorttime,longtime):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)

		sma30 = ta.EMA(close,timeperiod=shorttime)
		sma150 = ta.EMA(close,timeperiod=longtime)
		
		if sma30[-1] > sma150[-1] :
			buy(self)
		elif sma30[-1] < sma150[-1] :
			sell(self)
		else:
			undo(self)
		return self
	def volumeeffect(self,days,effect):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)
		
		allbodong=0
		starttoend=abs(volume[-1]-volume[-days])
		for x in xrange(1,days):
			allbodong=allbodong+abs(volume[-x-1]-volume[-x])
		if starttoend/allbodong>effect:
			if volume[-1]>=volume[-3] and close[-1]>=close[-3]:
				buy(self)
			elif volume[-1]<volume[-3] and close[-1]<close[-3]:
				sell(self)
			else:
				undo(self)
		elif starttoend/allbodong<effect:
			undo(self)
		else:
			undo(self)
		return self
	def volume(self,vol):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)
		
		if volume[-1]*close[-1]>vol:
			buy(self)
		else:
			undo(self)
		return self
	def price(self,pmin,pmax):
		st,openn,high,close,low,volume=getpricelist(self)
		ifgopass(self)
		if close[-1]>=pmin and  close[-1]<=pmax :
			# self.mydo.do=True
			# self.mydo.dotype=self.mydo.dotype+1 #buy
			buy(self)
		else:
			# self.mydo.do=False
			# self.mydo.dotype=self.mydo.dotype-1 #sell
			sell(self)
		return self
	def show(self):
		# print self
		return self.mydo
