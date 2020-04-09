# -*- coding: utf-8 -*-
from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from time import sleep, strftime, time
from functools import partial

from ib.ext.OrderState import OrderState

from ib.opt import messagetools
import requests
import math

from pandas.io.data import DataReader
from datetime import datetime
import random

import logging
import ConfigParser

logging.getLogger("requests").setLevel(logging.WARNING)

import jinja2
import smtplib    
from email.mime.text import MIMEText  

#global var
short_sleep = partial(sleep, 5)
long_sleep = partial(sleep, 20)
buylist=[]
selllist=[]
myposition={}
stock_real_price={}
stock_real_amount={}


myaccount=0

symboldoing_log={}

# conn={}

#config
conf=ConfigParser.RawConfigParser()
conf.read('conf/orderid.conf')

# odid= conf.getint("order","id")
# print odid
# odid= conf.getint('order','id')
# odid=odid+1
# conf.set('order','id',odid)
# odid= conf.getint("order","id")
# print odid

#global functions

# orderidlist=range(11180, 25000)
# orderidlist=range(1000, 2000)
theorderid=0

def generate_orderid():
    # thisorderid=orderidlist.pop(0)
    # thisorderid=0	
    odid= conf.getint("order","id")
    # print odid
    odid= conf.getint('order','id')
    # odid=odid+1
    conf.set('order','id',odid)
    odid= conf.getint("order","id")
    # print odid

    odid= conf.getint("order","id")
    # print type(odid)

    # theorderid=thisorderid
    # print 'thisorderid'+str(thisorderid)
    # return thisorderid
    return odid
    # return random.randint(1,1000)

def make_contract(symbol):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    contract.m_primaryExch = 'SMART'
    contract.m_currency = 'USD'
    contract.m_localSymbol = symbol
    return contract

def make_order(action,quantity, price = None):

    if price is not None:
        order = Order()
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price
    else:
        order = Order()
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action
    return order

def trade(conn,symbol,action,quantity,price = None):


	#记录当天的操作，再次请求则拒绝操作   
	# 导致问题是  不可以做同一个股票的日内交易 将来算法改成日内算法就必须去掉这个限制
	#日内止损也没办法做了
	todayconf=ConfigParser.RawConfigParser()
	todayconf.read('conf/today.conf')

	if not todayconf.has_section("did"):
		todayconf.add_section("did")
	else :
		if not todayconf.has_option('did',symbol):
			todayconf.set('did',symbol,1)
		else:
			# print 'sorry  ,you have already do some thing at this stock...'
			return False

	with open('conf/today.conf','w') as todaytradeconfile:
		todayconf.write(todaytradeconfile)


	#应该是可以获取到当前正在排队的交易挂单
	print 'openorders:'
	print conn.reqOpenOrders()
	# print conn.reqGetOpenOrderList()
	#getopenorderlist
	#如果挂单中有票的symbol与volume 一致，说明是同一种交易，可拒绝


	oid=generate_orderid()
	setnum=1
	oid=oid+setnum
	logging.info('new order generate :'+str(oid))

	#发送一封邮件过来  放在后面是防止返回false了还继续发送消息
	message='symbol: '+str(symbol)+'  action: '+str(action)+' volume: '+str(quantity)
	print message
	sendemail(message)


	#如果这里操作出现了当天自动操作里面的股票，意味着人工干预了结果
	# 则记录此股票，并在将来几天内都不准许操作

	#更新订单ID
	odid= conf.getint('order','id')
	odid=odid+1
	conf.set('order','id',odid)

	with open('conf/orderid.conf','w') as configfile:
		conf.write(configfile)

	cont=make_contract(symbol)
	offer = make_order(action,quantity,price)
	conn.placeOrder(oid, cont, offer)

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
info.currentamount=1
info.unrealized=0
info.buyingpower=0
info.stockvalue=0
info.cashbalance=0
info.daytradesremaining=0
info.daytradesremainingt1=0
info.istrade=False
info.mylevel=1


def getmyaccount():
	return info


def my_account_handler(msg):
	#https://www.interactivebrokers.com.hk/cn/software/tws/usersguidebook/realtimeactivitymonitoring/available_for_trading.htm
	#AvailableFunds
	#ExcessLiquidity
	#DayTradesRemaining
	#DayTradesRemainingT+1
	#DayTradesRemainingT+2
	#
	#FutureOptionValue
	#GrossPositionValue
	#MoneyMarketFundValue
	#TBondValue
	#TradingType
	#WarrantValue
	if msg.key.lower()=='daytradesremainingt+1':
		print 'daytradesremainingt1:'+str(msg.value)
		# print int(myaccount.daytradesremainingt1)>1
		if int(msg.value) >= 3:
			info.istrade=True
		info.daytradesremainingt1=msg.value
	if msg.key.lower()=='daytradesremaining':
		print 'daytradesremaining:'+str(msg.value)
		info.daytradesremaining=msg.value
	if msg.key.lower()=='netliquidation':
		info.currentamount=msg.value
	if msg.key.lower()=='stockmarketvalue':
	   	info.stockvalue=msg.value
	   	info.mylevel=float(msg.value)/float(info.currentamount)
	   	# print 'my stocks value:'+str(msg.value)
   	if msg.key.lower()=='unrealizedpnl':
   		info.unrealized=msg.value
   		# print 'my account Unrealized earns:'+str(msg.value)
   	if msg.key.lower()=='buyingpower':
   		info.buyingpower=msg.value
   		# print 'buyingpower'+str(msg.value)
   		# print 'my account BuyingPower:'+str(msg.value)
   	if msg.key.lower()=='cashbalance':
	   	info.cashbalance=msg.value
	   	# print 'my account CashBalance:'+str(msg.value)
   	return info


def sendemail(message):
    # 邮件通知
    sender = 'data@cdsb.com'
    receiver = 'qy1120319@126.com'
    subject = '天宝自动交易机器人-交易警报'
    smtpserver = 'smtp.qq.com'
    username = 'data@cdsb.com'
    password = 'Qy1120'

    # data=''
    # env = jinja2.Environment(loader = jinja2.FileSystemLoader('template'))
    # template=env.get_template('self.html')
    template=jinja2.Template(u'<html>自动交易提醒 : {{ data }}</html>')
    htmlstr=template.render(data=message)
    msg = MIMEText(htmlstr,'html','utf-8')
    msg['Subject'] = subject
    # 设置根容器属性  
    msg['From'] = '天宝<data@cdsb.com>'
    # msg['Cc']='qy1120319@163.com'
    try:
	    smtp = smtplib.SMTP()
	    smtp.connect('smtp.qq.com')
	    smtp.login(username, password)
	    smtp.sendmail(sender, receiver, msg.as_string())
	    smtp.quit()
    except Exception, e:
    	# raise e
    	print 'email error'
    	pass
    # smtp = smtplib.SMTP()
    # smtp.connect('smtp.qq.com')
    # smtp.login(username, password)
    # smtp.sendmail(sender, receiver, msg.as_string())
    # smtp.quit()




def my_postion_handler(msg):
	# alllost=0
	#my position management
    if int(msg.averageCost)!=0:
        myblanlence=(msg.position/abs(msg.position))*(msg.marketPrice-msg.averageCost)/msg.averageCost
        pinfo={"position":msg.position,'dealprice':msg.averageCost,"marketprice":msg.marketPrice,"banlence":myblanlence,"unrealized":msg.unrealizedPNL}
        info.position[msg.contract.m_symbol]=pinfo
    #alllost=0
    alllost=0
    # allmoney=0
    for st in info.position:
    	alllost=alllost + info.position[st]['unrealized']
    	# allmoney=allmoney + abs(msg.position*info.position[st]['dealprice'])-info.position[st]['unrealized']
	# print alllost
	info.unrealized=alllost
	# print allmoney
	# print 'theorderid : '+str(theorderid)
	# print info
def getcon(tport,tclientId):
	conn = Connection.create(port=tport, clientId=tclientId)
	conn.register(my_account_handler, 'UpdateAccountValue')
	conn.register(my_postion_handler,message.updatePortfolio)
	conn.connect()
	conn.reqCurrentTime()
	conn.reqAccountUpdates(1,'')
	conn.reqManagedAccts()
	print 'openorders:'
	print conn.reqOpenOrders()
	# print info
	return conn