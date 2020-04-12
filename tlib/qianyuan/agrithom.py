#coding:utf-8
import os,sys
# parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)
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



###之前的系统
# from tech import Engine 
# from tech import Filter 
# search = Engine()
# filtercontrol = Filter()

#####新的系统
from tlib.qianyuan.tech import Dealler 
search=Dealler()
filtercontrol=Dealler()


#需要考虑的几点
#
#所有策略自由组合，并可以批量自动运算策略，不论是过滤还是打分，不论是类方式还是函数方式
#开发自由性，可以把指标的计算结果跟均线的数据进行比较
#可以综合各个模型的数据结果，综合判断
#

# 计分器 过滤器 自由组合指标（必须取一个新的指标名字  等同与EMA  MACD 之类的）   能不能来源于一个类？最后统一包装一下
# 因为都是根据数据，返回买卖信号。根据类型不同，返回不同的格式

def zhuafantan(stsymbol,priceclose):
	st=stsymbol
	stockk=priceclose
	calcustr='cacuer'
	cacuer=search.load(st,stockk) #.adx().show()

	#记分器
	#######begin#######
	calcustr=calcustr+'.recent(0.1,0.2,5)'
	calcustr=calcustr+'.effection(5,0.7)'
	calcustr=calcustr+'.ema(3,6)'
	calcustr=calcustr+'.volumeeffect(3,0.95)'
	########over########
	#过滤器
	fil=filtercontrol.load(st,stockk).volume(10000*10*10*5).price(5,150).effection(10,0.6).show()
	# print fil.do


	calcustr=calcustr+'.show()'
	exec('res='+calcustr)
	if res.do and (res.dotype>=3 or res.dotype<=-3) and fil.do:
		return res
	else:
		res.do=False
		return res


#需要考虑的几点
#
#所有策略自由组合，并可以批量自动运算策略，不论是过滤还是打分，不论是类方式还是函数方式
#开发自由性，可以把指标的计算结果跟均线的数据进行比较
#可以综合各个模型的数据结果，综合判断
#

def testagrithom(stsymbol,priceclose):
	st=stsymbol
	stockk=priceclose
	calcustr='cacuer'
	cacuer=search.load(st,stockk) #.adx().show()

	#记分器
	#######begin#######
	calcustr=calcustr+'.recent(0.1,0.2,5)'
	calcustr=calcustr+'.effection(5,0.7)'
	calcustr=calcustr+'.ema(3,6)'
	calcustr=calcustr+'.volumeeffect(3,0.95)'
	########over########
	#过滤器
	fil=filtercontrol.load(st,stockk).volume(10000*10*10*5).price(5,150).effection(10,0.6).show()
	# print fil.do


	calcustr=calcustr+'.show()'
	exec('res='+calcustr)
	if res.do and (res.dotype>=3 or res.dotype<=-3) and fil.do:
		return res
	else:
		res.do=False
		return res



def shuangjunxian(stsymbol,priceclose):
	st=stsymbol
	stockk=priceclose
	calcustr='cacuer'
	cacuer=search.load(st,stockk) #.adx().show()

	#记分器
	#######begin#######
	calcustr=calcustr+'.recent(0.05,0.10,5)'
	calcustr=calcustr+'.effection(5,0.6)'
	calcustr=calcustr+'.ema(30,200)'
	calcustr=calcustr+'.volumeeffect(7,0.5)'
	########over########
	#过滤器
	fil=filtercontrol.load(st,stockk).volume(10000*10*10*5).price(5,150).ema(5,13).show()
	# print fil.do


	calcustr=calcustr+'.show()'
	exec('res='+calcustr)
	if res.do and (res.dotype>=4 or res.dotype<=-4) and fil.do:
		return res
	else:
		res.do=False
		return res



def fangliangzhangdie(stsymbol,priceclose):
	st=stsymbol
	stockk=priceclose
	calcustr='cacuer'
	cacuer=search.load(st,stockk) #.adx().show()

	#记分器
	#######begin#######
	# calcustr=calcustr+'.recent(0.05,0.10,3)'
	# calcustr=calcustr+'.recent(-0.015,-0.05,3)'
	calcustr=calcustr+'.effection(7,0.9)'
	# calcustr=calcustr+'.ema(30,150)'
	# calcustr=calcustr+'.volumeeffect(7,0.5)'
	########over########
	#过滤器
	fil=filtercontrol.load(st,stockk).volume(10000*10*10*5).price(5,150).volumeeffect(7,0.9).show()
	# print fil.do


	calcustr=calcustr+'.show()'
	exec('res='+calcustr)
	if res.do and (res.dotype>=1 or res.dotype<=-1) and fil.do:
		# print 'because:'

		#高位放量，需要卖出
		res.dotype=-1
		return res
	else:
		res.do=False
		return res
