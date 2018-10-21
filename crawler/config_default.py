# -*- coding: utf-8 -*-

'''
Default configurations.
'''
__author__ = 'West'

configs = {
    'debug':True,
    'max_retry_times':5,
    'markup_type':'lxml',
    'db':{
        'host':'192.168.56.102',
        'port':3306,
        'user':'root',
        'password':'123',
        'db':'graduation_project',
        'charset':'utf8'
    },
    'redis':{
        'host':'192.168.56.102',
        'port':6379
    },
    'yiche':{
        'thread_num': 4,
        'carinfo_base_url':'http://car.bitauto.com',
        'price_base_url':'http://price.bitauto.com',
        'carinfo_lefttreejson_url':'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0',
        'price_lefttreejson_url':'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=baojia&pagetype=&objid='
    },
    'renrenche':{
        'process_num':4,
        'base_url':'https://renrenche.com/'
    },
    'carpolicy':{
        'base_url':'http://www.caam.org.cn',
        'national_policy_url':'http://www.caam.org.cn/newslist/a19-01.html',
        'local_policy_url':'http://www.caam.org.cn/newslist/a20-01.html',
        'earliest_date':'2008-01-01'
    }
}