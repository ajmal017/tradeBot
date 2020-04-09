#coding:utf-8
import tushare as ts
import pandas as pd
import random
import os

import ag



def querystockbydate(parray,datestr):
	index=1
	for x in parray['date']:
		if x==datestr :
		 	# print parray['date'].index(datestr)
		 	# print index
		 	return index
		index=index+1

# stocks = pd.read_table("E:/python/trade/todaystocks.csv",sep=",",encoding='utf-8',dtype={'code':str})
stocks=ts.get_stock_basics()

# period=['2015-06-02','2015-06-03']
period=['2015-06-17','2015-06-18']
# period=['2015-06-11','2015-06-12']

allmakemoney=1
for p in range(len(period)-1):
	print period[p]
	print '\n'
	win=0
	fail=0
	stocktosell=[]    
	step2=[]
	step3=[]
	step4=[]
	step5=[]
	stepfor54=[]
	earnmoney=0
	inmoney=0	
	for st in stocks.index:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			# print stocks[st]
			# print stock.index()
			index=1
			index=querystockbydate(stock,period[p])
			# print len(stock)
			# print index
			if type(index)==int and  len(stock)>=index:
				# print index
				condition5=ag.step1(stock,stocks,index,st)
				if condition5 :
					step2.append(st)
		else:
			print 'file not exist'
		# print stock.__getitem__(index)

		# if index is not None  and type(index)==int:
			# print index
			# todaysdata=stock['date'][index]
			# if stock['date'][index]:
				# print 'x'
			# print 'true'
			# print i
			# break
			# continue
		# print p
		# print index
		# todaysdata=stock['date'][index]
		# print todaysdata
		
		# print stock['date']
	print len(step2)
	print 'step for 2:'
	for st in step2:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})		
			index=1
			index=querystockbydate(stock,period[p])
			# print i
			if type(index)==int and  len(stock)>=index:
				condition6=ag.step2(stock,stocks,index,st)
				if condition6 :
					step3.append(st)	
			else:
				print 'file not exist'	
		print len(step3)

	print 'step for 3:'
	for st in step3:
		if os.path.exists("stocks/"+st+".csv"):
			stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			if len(stock)>20:
				#重新计算换手率 不需要
				# stock['turnover']=stock['volume'][index-1]/stocks['outstanding'][st]
				#条件
				# for test in range(len(stock)):
					# print stock['close'][test]
				# print stock
				# month=stock['close'][-20:-1]
				# print len(month)
				if (stock['close'][len(stock)-1]-stock['close'][len(stock)-20])/stock['close'][len(stock)-20]>=0.1:
				# if (month[20]-month[1])/month[1]>=0.1:
					step4.append(st)
		else:
			print 'file not exist'	
	step4=step3
	print len(step4)

	# print 'step for 4:'
	# for st in step4:
	# 	df= ts.get_tick_data(st,date=period[p])
	# 	# df= ts.get_today_ticks(st)
	# 	sanhu={'buy':0,'sell':0}
	# 	dahu={'buy':0,'sell':0}
	# 	for i in range(len(df)):
	# 		if df['amount'][i]<500000:
	# 			# print "sanhu"
	# 			if df['type'][i] == "买盘":
	# 				sanhu['buy']=sanhu['buy']+df['amount'][i]
	# 			elif df['type'][i] == "卖盘":
	# 				sanhu['sell']=sanhu['sell']+df['amount'][i]
	# 		else:
	# 			# print "dahu"
	# 			if df['type'][i]=="买盘":
	# 				dahu['buy']=dahu['buy']+df['amount'][i]
	# 			elif df['type'][i]=="卖盘":
	# 				dahu['sell']=dahu['sell']+df['amount'][i]
	# 	#sanhu['sell']>sanhu['buy'] and 
	# 	if dahu['buy']>dahu['sell']:
	# 		step5.append(st)
	# print len(step5)
	step5=step4

	if len(step3)>140:
		print 'no trade'
		allmakemoney=allmakemoney
	else:
		for stockitems in step5:
			print stockitems
