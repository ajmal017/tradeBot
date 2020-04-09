#coding:utf-8
import os

# #允许python 的dict数据类型 可以通过点的方式来取数据
class DottableDict(dict):   
	def __init__(self, *args, **kwargs):     
		dict.__init__(self, *args, **kwargs)     
		self.__dict__ = self  
	def allowDotting(self, state=True):     
		if state:       
			self.__dict__ = self   
		else:       
			self.__dict__ = dict() 

#允许python 的dict数据类型 可以通过点的方式来取数据
info=DottableDict()
info.allowDotting()
info.position={}
info.currentamount=10000
info.unrealized=0
info.buyingpower=info.currentamount*2
info.stockvalue=0
info.cashbalance=0



def getmoneynumber():
	pass

def getmyaccount():
	#更新仓位数据
	for st in info.position:
		if os.path.exists("yahoo-nodejs/old/stocks/"+st+".csv"):
			stock = pd.read_table("yahoo-nodejs/old/stocks/"+st+".csv",sep=",",encoding='utf-8',dtype={'code':str})
			stock=stock.sort(columns='Date')
			#计算损失多少
			#计算当前价格 （以传入日期为准）
    		info.position[st]['marketprice']=stock[-1]['Close']
	return info

#
#myblanlence=(msg.position/abs(msg.position))*(msg.marketPrice-msg.averageCost)/msg.averageCost
# pinfo={"postion":msg.position,'dealprice':msg.averageCost,"marketprice":msg.marketPrice,"banlence":myblanlence,"unrealized":msg.unrealizedPNL}
# info.position[msg.contract.m_symbol]=pinfo
#

def trade(conn,symbol,action,quantity,price = None):
	if action == 'BUY':
		info.position[symbol]={"postion":quantity,'dealprice':price,"marketprice":price,"banlence":0,"unrealized":0}
	elif action == 'SELL':
		info.position[symbol]={"postion":-quantity,'dealprice':price,"marketprice":price,"banlence":0,"unrealized":0}
	else:
		print 'trade err'
	return {}


def getcon(tport=0,tclientId=0):
	conn={}
	#更新仓位数据
	return conn

# def buy():
# 	return 'allstock'
# def sell():
# 	return 'allstock'