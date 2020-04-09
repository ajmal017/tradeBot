#coding:utf-8
import tushare as ts
import pandas as pd
import random
import allstocks as stocklib
from itertools import combinations
import os
# import scipy as sp
from scipy.stats.stats import pearsonr


allstock=stocklib.getstocks()


stockfor2list=list(combinations(list(allstock),2))


for tow in stockfor2list:
	st1= tow[0]
	st2= tow[1]
	if os.path.exists("yahoo-nodejs/old/stocks/"+st1+".csv") and os.path.exists("yahoo-nodejs/old/stocks/"+st2+".csv") :
		stock1 = pd.read_table("yahoo-nodejs/old/stocks/"+st1+".csv",sep=",",encoding='utf-8',dtype={'code':str})
		stock2 = pd.read_table("yahoo-nodejs/old/stocks/"+st2+".csv",sep=",",encoding='utf-8',dtype={'code':str})

		pearson=pearsonr(stock1['Close'],stock2['Close'])[0]
		if pearson>0.9 or pearson<-0.9:
			print pearson
			print stockname[i]+' and  '+stockname[n]
			# print stockname[n]
			print '\n'

# stocks = pd.read_table("E:/python/trade/todaystocks.csv",sep=",",encoding='utf-8',dtype={'code':str})
#  =['2015-05-11','2015-05-12']

# newstock=[]
# stockname=[]

# for i in range(len(stocks)):
# 	if random.uniform(1, 100)<10 and  i>0 and i<3000:
# 		pricelist= ts.get_hist_data(stocks['code'][i],start='2015-02-13',end='2015-05-11')
# 		# print pricelist
# 		if len(pricelist)>=56:
# 			thisstock=[]
# 			for x in pricelist['p_change']:
# 				# print x
# 				thisstock.append(x)
# 			newstock.append(thisstock)
# 			stockname.append(stocks['code'][i])

# for arr in newstock:
# 	print len(arr)

# for i in range(len(newstock)):
# 	for n in range(len(newstock)):
# 		if n>i:
# 			# print bytes(i)+'and'+bytes(n)
# 			pearson=pearsonr(newstock[i],newstock[n])[0]
# 			if pearson>0.9 or pearson<-0.9:
# 				print pearson
# 				print stockname[i]+' and  '+stockname[n]
# 				# print stockname[n]
# 				print '\n'



# # print pearsonr(newstock[1],newstock[2])[0]
