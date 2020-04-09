#coding:utf-8

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

# def getpricelist(st):
# 	return st._symbol,st._open,st._high,st._close,st._low,st._volume

# class Dealler:
# 	def load(self,symbol,priceclose):
# 		# st=StockSelf()
# 		# st._open=np.array(priceclose['Open'])
# 		# st._high=np.array(priceclose['High'])
# 		# st._close=np.array(priceclose['Close'])
# 		# st._low=np.array(priceclose['Low'])
# 		# st._volume=np.array(priceclose['Volume'])
# 		# st._symbol=symbol
# 		# self.stockself=st
# 		# return self
# 			return {}
# 	def ifgopass(self):
# 		# if not self.stockself.mydo.do:
# 		# 	return self
# 		# else:
# 		# 	pass
# 			pass
# 	def price(self,pmin,pmax):
# 		# st,openn,high,close,low,volume=getpricelist(self.stockself)
# 		# ifgopass(self)
# 		# if close[-1]>=pmin and  close[-1]<=pmax :
# 		# 	self.stockself.mydo.do=True
# 		# 	self.stockself.mydo.dotype=self.mydo.dotype+1 #buy
# 		# else:
# 		# 	self.stockself.mydo.do=False
# 		# 	self.stockself.mydo.dotype=self.mydo.dotype-1 #sell
# 		# return self
# 			return {}
# 	def show(self):
# 		# return self.stockself.mydo
# 			return {}

# test=Dealler()
# print test.load('','').price('','').show()

import os
import pandas as pd
import numpy as np
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


def getpricelist(selfobj):
	return selfobj._symbol,selfobj._open,selfobj._high,selfobj._close,selfobj._low,selfobj._volume

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


class Dealler:
	_symbol=''
	_open=[]
	_high=[]
	_close=[]
	_low=[]
	_volume=[]
	mydo=DottableDict()
	def __init__(self):
		self.mydo.allowDotting()
		self.mydo.do=True
		self.mydo.dotype=0
	def load(self,symbol,priceclose):
		# st=StockSelf()
		self._open=np.array(priceclose['Open'])
		self._high=np.array(priceclose['High'])
		self._close=np.array(priceclose['Close'])
		self._low=np.array(priceclose['Low'])
		self._volume=np.array(priceclose['Volume'])
		self._symbol=symbol
		# self.stockself=st
		return self
	def ifgopass(self):
		if not self.mydo.do:
			return self
		else:
			pass
	def buy(self):
		self.mydo.do=True
		self.mydo.dotype=self.mydo.dotype+1 #buy
	def sell(self):
		self.mydo.do=False
		self.mydo.dotype=self.mydo.dotype-1 #sell


	def price(self,pmin,pmax):
		st,openn,high,close,low,volume=getpricelist(self)
		self.ifgopass()
		if close[-1]>=pmin and  close[-1]<=pmax :
			# self.mydo.do=True
			# self.mydo.dotype=self.mydo.dotype+1 #buy
			self.buy()
		else:
			# self.mydo.do=False
			# self.mydo.dotype=self.mydo.dotype-1 #sell
			self.sell()
		return self
	def show(self):
		# print self
		return self.mydo


search=Dealler()
filtercontrol=Dealler()

allstock=['AAPL','YANG','VIPS']
for st in allstock:
	print st
	if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
		stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
		stock=stock.sort(columns='Date')

		calcustr='cacuer'
		cacuer=search.load(st,stock)

		#记分器
		#######begin#######
		calcustr=calcustr+'.price(1,500)'
		########over########
		#过滤器
		fil=filtercontrol.load(st,stock).price(5,150).show()
		# print fil


		calcustr=calcustr+'.show()'
		exec('res='+calcustr)

		# print res

		# if res.do and (res.dotype>=3 or res.dotype<=-3) and fil.do:
		# 	return res
		# else:
		# 	res.do=False
		# 	return res
