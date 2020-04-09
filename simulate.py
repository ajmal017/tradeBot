#coding:utf-8
# import tushare as ts
import pandas as pd
import numpy as np
import random
import os

import agsim as ag
import datetime

def querystockbydate(parray,datestr):
	index=1
	for x in parray["Date"]:
		if x==datestr :
		 	# print parray["Date"].index(datestr)
		 	# print index
		 	return index
		index=index+1

# stocks=ts.get_stock_basics()
stocks=""
# watchlist=["DIA","SPY","QQQ","JNJ","MSFT","PG","XOM","CNR","Date","SFUN","NCTY","XUE","AMD","EJ","NGAS","JPN","BABA","JD","SOHU","SYMC","NOK","CDE","DUST","ICON","BMD","HTC","GDX","UNG","VHT","CMD","MBI","CRK","BGS","LMT","CANE","SGG","WEAT","JJN","NINI","JO","CAFE","CPER","LSTK","UBC","CHOC","NIB","CTNN","EGPT","AFK","EZA","GAF","ACWI","GULF","UAE","MES","PEK","FXI","ASHR","CHIQ","CNXT","CQQQ","CHIX","GXC","QQQC","YANG","YINN","XPP","YXI","FXP","CHAD","VIPS","EPP","FJP","FKO","JYN","FPA","SCIX","AIA","IFV","AXJV","HKOR","DXKW","DBKO","EWY","QKOR","JPN","GREK","EUFN","VGK","RUSL","RUSS","ERO","FXE","UUP","RSX","DXGR","EWG","QDEU","EWGS","FGM","EWQ","FEZ","EZU","ERUS","RBL","RSXJ","GUR","GER","LHB","LBJ","FLN","BRAQ","BRAZ","AND","ARGT","ECH","FRN","ILF","GML","DBMX","EWW","QMEX","EEML","FRN","FM","SCIF","EPI","INP","SCIN","INCO","IFN","PAK","ASEA","EWS","IDLV","RGRO","VNM","SPY","DIA","QQQ","IWM","SH","DBC","DBB","EFA","EEM","VNQ","IAU","OIL","FXE","EUO","SCO","VQT","GRI","EDZ","DZK","FAS","BND","VXUS","VWO","SDR","BIB","CURE","ENY","FCAN","CNDA","QCAN","PPH","BBH","PPA","ITA","MON","SYT","DD","DOW","LMT","SGG","SOYB","GLD","SSO","DBA"]

# watchlist=["DIA","SPY","QQQ","JNJ","MSFT","PG","XOM","CNR","Date","SFUN","NCTY","XUE","AMD","EJ","NGAS","JPN","BABA","JD","SOHU","SYMC","NOK","CDE","DUST","ICON","BMD","HTC","GDX","UNG","VHT","CMD","MBI","CRK","BGS","LMT","CANE","SGG","WEAT","JJN","NINI","JO","CAFE","CPER","LSTK","UBC","CHOC","NIB","CTNN","EGPT","AFK","EZA","GAF","ACWI","GULF","UAE","MES","PEK","FXI","ASHR","CHIQ","CNXT","CQQQ","CHIX","GXC","QQQC","YANG","YINN","XPP","YXI","FXP","CHAD","VIPS","EPP","FJP","FKO","JYN","FPA","SCIX","AIA","IFV","AXJV","HKOR","DXKW","DBKO","EWY","QKOR","JPN","GREK","EUFN","VGK","RUSL","RUSS","ERO","FXE","UUP","RSX","DXGR","EWG","QDEU","EWGS","FGM","EWQ","FEZ","EZU","ERUS","RBL","RSXJ","GUR","GER","LHB","LBJ","FLN","BRAQ","BRAZ","AND","ARGT","ECH","FRN","ILF","GML","DBMX","EWW","QMEX","EEML","FRN","FM","SCIF","EPI","INP","SCIN","INCO","IFN","PAK","ASEA","EWS","IDLV","RGRO","VNM","SPY","DIA","QQQ","IWM","SH","DBC","DBB","EFA","EEM","VNQ","IAU","OIL","FXE","EUO","SCO","VQT","GRI","EDZ","DZK","FAS","BND","VXUS","VWO","SDR","BIB","CURE","ENY","FCAN","CNDA","QCAN","PPH","BBH","PPA","ITA","MON","SYT","DD","DOW","LMT","SGG","SOYB","GLD","SSO","DBA"]

# period=["2015-04-30","2015-05-04"]
# period=["2015-04-23","2015-04-24"]
# period=["2015-05-06","2015-04-27"]
# period=["2015-04-20","2015-04-21","2015-04-22","2015-04-23","2015-04-24","2015-04-27","2015-04-28","2015-04-29","2015-04-30","2015-05-04","2015-05-05","2015-05-06","2015-05-07","2015-05-08"]
# period=["2015-04-20","2015-04-21","2015-04-22","2015-04-23","2015-04-24","2015-04-27"]
# period=["2015-04-20","2015-04-21","2015-04-22","2015-04-23","2015-04-24","2015-04-27","2015-04-28","2015-04-29","2015-04-30","2015-05-04","2015-05-05","2015-05-06","2015-05-07","2015-05-08","2015-05-11","2015-05-12","2015-05-13","2015-05-14","2015-05-15","2015-05-18","2015-05-19","2015-05-20","2015-05-21","2015-05-22"]
# period=["2015-06-10","2015-06-11","2015-06-12"]

period=[]
for daycount in range(0,10):
	# period.append()
    # for daycount in range(1,7):
    day_lastmonth=datetime.date(2015,9,1)
    # # day_lastmonth=datetime.date(starttime.year,starttime.month,1)
    day_offset=datetime.timedelta(days=daycount)
    # day_during=datetime.timedelta(days=7)

    startday=day_lastmonth+day_offset
    # endday=startday+day_during
    period.append(str(startday))
print period


allcostmoney=0
allearnmoney=0
martketvalue=0
# myposition=[]
myposition={}

buyposition={}
sellposition={}
myaccount={
	"name":"qianyuan",
	"cash":5000,
	"position":{},
}

def simbuy(symbol,price,amount):
	if price*amount>myaccount["cash"]:
		# exit("have no enough money!")
		pass
	else:
		if myaccount["position"].has_key(symbol):
			if myaccount["position"][symbol]["type"]=="sell":
				if amount==myaccount["position"][symbol]["amount"]:
					myaccount["cash"]=myaccount["cash"]-price*amount
				 	myaccount["position"].pop(symbol)
				elif amount>myaccount["position"][symbol]["amount"]:
					myaccount["cash"]=myaccount["cash"]-price*amount
					myaccount["position"][symbol]["type"]="buy"
					myaccount["position"][symbol]["amount"]=amount-myaccount["position"][symbol]["amount"]
					myaccount["position"][symbol]["price"]=price
				elif amount<myaccount["position"][symbol]["amount"]:
					myaccount["cash"]=myaccount["cash"]-price*amount
					myaccount["position"][symbol]["type"]="sell"
					myaccount["position"][symbol]["amount"]=myaccount["position"][symbol]["amount"]-amount
			elif myaccount["position"][symbol]["type"]=="buy":
				myaccount["cash"]=myaccount["cash"]-price*amount
				myaccount["position"][symbol]["amount"]=myaccount["position"][symbol]["amount"]+amount
				myaccount["position"][symbol]["price"]=(myaccount["position"][symbol]["price"]+price)/2
		else:
			myaccount["cash"]=myaccount["cash"]-price*amount
			myaccount["position"][symbol]={"price":price,"amount":amount,"type":"buy"}

def simsell(symbol,price,amount):
	if myaccount["position"].has_key(symbol):
		if myaccount["position"][symbol]["type"]=="buy":
			if amount==myaccount["position"][symbol]["amount"]:
				myaccount["cash"]=myaccount["cash"]+price*amount
			 	myaccount["position"].pop(symbol)
			elif amount>myaccount["position"][symbol]["amount"]:
				myaccount["cash"]=myaccount["cash"]+price*amount
				myaccount["position"][symbol]["type"]="sell"
				myaccount["position"][symbol]["amount"]=amount-myaccount["position"][symbol]["amount"]
				myaccount["position"][symbol]["price"]=price
			elif amount<myaccount["position"][symbol]["amount"]:
				myaccount["cash"]=myaccount["cash"]+price*amount
				myaccount["position"][symbol]["type"]="buy"
				myaccount["position"][symbol]["amount"]=myaccount["position"][symbol]["amount"]-amount
		elif myaccount["position"][symbol]["type"]=="sell":
			myaccount["cash"]=myaccount["cash"]+price*amount
			myaccount["position"][symbol]["amount"]=myaccount["position"][symbol]["amount"]+amount
			myaccount["position"][symbol]["price"]=(myaccount["position"][symbol]["price"]+price)/2
	else:
		myaccount["cash"]=myaccount["cash"]+price*amount
		myaccount["position"][symbol]={"price":price,"amount":amount,"type":"sell"}
		# exit("have no such stock!")
def get_cash(d):
	# myaccount["cash"]
	stockvalue=0
	for st in myaccount["position"]:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding="utf-8",dtype={"code":str})
			# print stocks[st]
			# print st
			for x in stock["Date"]:
				if x==d:
					# print x
					yesterday= querystockbydate(stock,d)-1
					today= querystockbydate(stock,d)
					tomorow= querystockbydate(stock,d)+1

					if myaccount["position"][st]["amount"]>0 and myaccount["position"][st]["type"]=="buy":
						# allearnmoney=allearnmoney+stock["Close"][today]*myposition[po]["amount"]
						# print "have:"+str(stock["Close"][today]*myposition[po]["amount"])
						# stockvalue=stockvalue+stock["Close"][today]*myaccount["position"][st]["amount"]-myaccount["position"][st]["price"]*myaccount["position"][st]["amount"]
						stockvalue=stockvalue+stock["Close"][today]*myaccount["position"][st]["amount"]

					elif myaccount["position"][st]["amount"]>0 and  myaccount["position"][st]["type"]=="sell":
						# allcostmoney=allcostmoney+stock["Close"][today]*myposition[po]["amount"]
						stockvalue=stockvalue-stock["Close"][today]*myaccount["position"][st]["amount"]
						# print "owe:"+str(stock["Close"][today]*myposition[po]["amount"])					
				else:
					# exit("cant find date match!")
					pass
	print myaccount["position"]
	print "cash:"+str(myaccount["cash"])
	print "stock:"+str(stockvalue)
	return myaccount["cash"]+stockvalue

lastday=""
for p in period:
	print p
	lastday=p
	res=ag.run(p)
	# print res
	for st in res["buy"]:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding="utf-8",dtype={"code":str})
			# print stocks[st]
			# print st
			for x in stock["Date"]:
				if x==p:
					yesterday= querystockbydate(stock,p)-1
					today= querystockbydate(stock,p)
					tomorow= querystockbydate(stock,p)+1
					print 'buy:'+st
					simbuy(st,stock["Close"][today],10)
	for st in res["sell"]:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding="utf-8",dtype={"code":str})
			# print stocks[st]
			# print st
			for x in stock["Date"]:
				if x==p:
					yesterday= querystockbydate(stock,p)-1
					today= querystockbydate(stock,p)
					tomorow= querystockbydate(stock,p)+1
					print 'sell:'+st
					
					simsell(st,stock["Close"][today],10)	

print get_cash(lastday)			