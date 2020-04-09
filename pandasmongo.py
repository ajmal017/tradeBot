#coding:utf-8

import pandas as pd
import talib as ta
import numpy as np
import os
import matplotlib.pyplot as plt
import allstocks as stocklib
import random
import logging
import ConfigParser
import datetime
import json
from pymongo import MongoClient
con = MongoClient()
testdb = con.day_history


# stdata=testdb.day_collection.count()
# print stdata
stdata=testdb.day_collection.find({'symbol':'55.07'},{'_id':0,'open':1,'high':1,'close':1,'low':1})
# print list(stdata)
# print stdata
dd=list(stdata)
print dd


# elevations=[{"Open":10,"High":11,"Close":10.5,"Low":9,"Volume":1000,"Date":'2015-10-29'},{"Open":10,"High":11,"Close":10.5,"Low":9,"Volume":1000,"Date":'2015-10-30'}]
elevations=dd
stockdata= pd.read_json(json.dumps(elevations))
print stockdata
print type(stockdata)
# print stockdata.hist()

print stockdata['close']
# print stockdata.to_json(orient='columns={"Open":"Open","High":"High","Close":"Close","Low":"Low","Volume":"Volume","Date":"Date"}')
# stockdata.set_index(col='date')
# data = json.loads(elevations)
# lat,lng,el = [],[],[]
# for result in data['results']:
#     lat.append(result[u'location'][u'lat'])
#     lng.append(result[u'location'][u'lng'])
#     el.append(result[u'elevation'])
# df = pd.DataFrame([lat,lng,el]).T