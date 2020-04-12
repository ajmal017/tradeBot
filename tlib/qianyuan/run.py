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


#需要考虑的几点
#
#所有策略自由组合，并可以批量自动运算策略，不论是过滤还是打分，不论是类方式还是函数方式
#开发自由性，可以把指标的计算结果跟均线的数据进行比较
#可以综合各个模型的数据结果，综合判断
#



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

# sys.path.append("./")
import tlib.qianyuan.agrithom


def main(stsymbol,priceclose):
	#抓反弹
	# print 'zhuafantan'
	# return agrithom.zhuafantan(stsymbol,priceclose)
	
	#测试新的Dealler类
	# return agrithom.testagrithom(stsymbol,priceclose)

	#双均线系统
	# return agrithom.shuangjunxian(stsymbol,priceclose)

	#放量涨跌
	return agrithom.fangliangzhangdie(stsymbol,priceclose)
	
	

	



