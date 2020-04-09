#coding:utf-8

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime
import allstocks as stocklib

stockprice=[]
stockpricema1=[]
stockpricema2=[]

# allstock=['AAL','AAAP']
allstock=stocklib.getstocks()


def update_data():
	for st in allstock:
		try:
			# pass yahoo-nodejs/old/
			if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
				# stock = pd.read_table("stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
				# stock=stock.sort(columns='Date')
				# stock.append('')
				# stock.to_csv('stocks/'+st+'.csv',index=False)

				old=pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
				# tests['Date']=tests['Date'].replace('/','-')
				# tests['Adj Close']=tests['Close']
				old=old.sort(columns='Date',ascending=True)	

				tests=pd.read_csv("yahoo-nodejs/old/YAHOO-singleday/stocks/"+st+".csv",sep=",",encoding='utf-8',names=['Date','Open','High','Low','Close','Volume'])
				#1/29/2016日期转换为 2016-01-29
				# tests['Date']=tests['Date'].str.replace(oldstr,'2016-01-29')
				month,day,year= tests['Date'].str.split('/')[0]
				tests['Date']=tests['Date'].str.replace(str(month)+'/',str(year)+'-')
				if int(month)>=10:
					# print str(month)+'>10'
					tests['Date']=tests['Date'].str.replace('-'+str(day),'-'+str(month))
				else:
					tests['Date']=tests['Date'].str.replace('-'+str(day),'-0'+str(month))	
				if int(day)>=10:
					tests['Date']=tests['Date'].str.replace('/'+str(year),'-'+str(day))
				else:
					tests['Date']=tests['Date'].str.replace('/'+str(year),'-0'+str(day))
				#1/29/2016日期转换为 2016-01-29
				
				tests['Adj Close']=tests['Close']
				# tests=tests.sort(columns='Date')
				# print tests

				if old['Date'][0]==tests['Date'][0]:
					pass
				else:
					old=old.append(tests)
				old=old.sort(columns='Date',ascending=False)
				old.to_csv('yahoo-nodejs/old/stocks/'+st+".csv",index=False)

				# old=pd.read_table("aal.csv",sep=",",encoding='utf-8',dtype={'code':str})
				# old=old.sort(columns='Date')
				# print old
				pass
		except Exception, e:
			# raise e
			pass

if __name__ == '__main__':
	update_data()