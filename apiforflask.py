# -*- coding: utf-8 -*-
from __future__ import division  
from apscheduler.schedulers.background import BackgroundScheduler

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
# from datetime import datetime

import datetime
import urllib2
import urllib

import random
import logging
import os
import pandas as pd
import numpy as np
import subprocess
logging.getLogger("requests").setLevel(logging.WARNING)
import talib as ta

import jinja2
import smtplib    
from email.mime.text import MIMEText  

import ConfigParser
import json

#账户操作API
import api_real as api
#平仓函数
def cut_position(conn,position,x):
    if position[x]['position']>0:
        api.trade(conn,x,'SELL',abs(position[x]['position']))
    elif position[x]['position']<0:
        api.trade(conn,x,'BUY',abs(position[x]['position']))
def buy(conn,st,spr):
    api.trade(conn,st,'BUY',abs(spr))
def sell(conn,st,spr):
    api.trade(conn,st,'SELL',abs(spr))


##########################
conn=api.getcon(4001,1929)
sleep(30*1) 
def getconn():
    return conn
def getaccount():
    myaccount=api.getmyaccount()
    return myaccount
