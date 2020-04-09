#coding:utf-8
import pandas as pd
import talib as ta
import numpy as np
import os
import matplotlib.pyplot as plt
# import allstocks as stocklib

#导入基本量化库
# import api_sim as api
#导入基本数学计算库
# import api_sim as api
#导入技术分析库
# import indexlib as lib

# 本引擎只产生信号
# from lib import Engine 
# from lib import Filter 

#导入算法交易员的算法库
import qianyuan



class Engine:
	def run(self,st,stockk):

		res = qianyuan.main(st,stockk)
		# res=search.load(st,stockk).show()

		return res
