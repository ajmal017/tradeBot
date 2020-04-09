#coding:utf-8

import pandas as pd
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import os

def querystockbydate(parray,datestr):
	index=1
	for x in parray['Date']:
		if x==datestr :
		 	# print parray['Date'].index(datestr)
		 	# print index
		 	return index
		index=index+1

def diff(stock):
	res=[0]
	for x in range(len(stock)-1):
		diffvalue=stock[x+1]-stock[x]
		res.append(diffvalue)
	# print res
	return res

def pev(parray,index):
	p=parray[index-7:index-2]
	# print len(p)
	if len(p)<2:
		return 0
	s=0
	price=[]
	for x in p['Close']:
		price.append(x)
	for x in range(len(price)-1):
		s=s+abs(price[x+1]-price[x])
	l=price[-1]-price[1]
	return l/s


watchlist=['DIA','SPY','QQQ','JNJ','MSFT','PG','XOM','CNR','DATE','SFUN','NCTY','XUE','AMD','EJ','NGAS','JPN','BABA','JD','SOHU','SYMC','NOK','CDE','DUST','ICON','BMD','HTC','GDX','UNG','VHT','CMD','MBI','CRK','BGS','LMT','CANE','SGG','WEAT','JJN','NINI','JO','CAFE','CPER','LSTK','UBC','CHOC','NIB','CTNN','EGPT','AFK','EZA','GAF','ACWI','GULF','UAE','MES','PEK','FXI','ASHR','CHIQ','CNXT','CQQQ','CHIX','GXC','QQQC','YANG','YINN','XPP','YXI','FXP','CHAD','VIPS','EPP','FJP','FKO','JYN','FPA','SCIX','AIA','IFV','AXJV','HKOR','DXKW','DBKO','EWY','QKOR','JPN','GREK','EUFN','VGK','RUSL','RUSS','ERO','FXE','UUP','RSX','DXGR','EWG','QDEU','EWGS','FGM','EWQ','FEZ','EZU','ERUS','RBL','RSXJ','GUR','GER','LHB','LBJ','FLN','BRAQ','BRAZ','AND','ARGT','ECH','FRN','ILF','GML','DBMX','EWW','QMEX','EEML','FRN','FM','SCIF','EPI','INP','SCIN','INCO','IFN','PAK','ASEA','EWS','IDLV','RGRO','VNM','SPY','DIA','QQQ','IWM','SH','DBC','DBB','EFA','EEM','VNQ','IAU','OIL','FXE','EUO','SCO','VQT','GRI','EDZ','DZK','FAS','BND','VXUS','VWO','SDR','BIB','CURE','ENY','FCAN','CNDA','QCAN','PPH','BBH','PPA','ITA','MON','SYT','DD','DOW','LMT','SGG','SOYB','GLD','SSO','DBA']
# watchlist=['CTNN','SOHU','BBH']


def diff(stock):
	res=[0]
	for x in range(len(stock)-1):
		diffvalue=stock[x+1]-stock[x]
		res.append(diffvalue)
	# print res
	return res

def run(period):
	# querystockbydate(parray,period)
	selllist=[]
	buylist=[]
	for st in watchlist:
		# pass
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			# ema20=ta.EMA(np.array(stock['Close']),timeperiod=10)
			# ema60=ta.EMA(np.array(stock['Close']),timeperiod=20)

			periodindex=querystockbydate(stock,period)
			# print periodindex

			# upper, middle, lower = ta.BBANDS(np.array(stock['Close']), 20, 2, 2)
			upper, middle, lower = ta.BBANDS(np.array(stock['Close']),matype=ta.MA_Type.T3)


			time = [x for x in range(len(np.array(stock['Close'])))]
			stockprice = np.array(stock['Close'])

			if type(periodindex)==int:
				if stockprice[periodindex] >= upper[periodindex]:
					# print 'sell:'+st
					selllist.append(st)
				elif stockprice[periodindex] <= lower[periodindex]:
					# print 'buy:'+st
					buylist.append(st)
				else:
					# print 'none:'+st
					pass
	# print {'sell':selllist,'buy':buylist}

	return {'sell':selllist,'buy':buylist}