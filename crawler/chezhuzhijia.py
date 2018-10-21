#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'West'

import pymysql, redis
from bs4 import BeautifulSoup
from enum import IntEnum
from logger import Logger
from utility import Utility
from config import configs

MARKUP_TYPE = configs.markup_type

class CacheManager:
    def __init__(self):
        pool = redis.ConnectionPool(host=configs.redis.host, port=configs.redis.port)
        self.redis = redis.Redis(connection_pool=pool)

    def isSerieSalesRecordExisted(self, serieId, sale_month):
        return self.redis.hget('serie-sales-record', key=serieId + '-' + sale_month) is not None

    def addSerieSalesRecord(self, serieId, sale_month, sale_volume):
        return self.redis.hset('serie-sales-record', key=serieId + '-' + sale_month, value=sale_volume)

class DBManager:
    def __init__(self):
        self.connection = pymysql.connect(host=configs.db.host, port=configs.db.port, user=configs.db.user, password=configs.db.password,
                                      db=configs.db.db, charset=configs.db.charset, cursorclass=pymysql.cursors.DictCursor)
    def __del__(self):
        self.connection.close()

    def insertSaleRecordListIntoDB(self, brand, subbrand, serie, serieId, saleRecordList):
        cursor = self.connection.cursor()
        try:
            sql = r'INSERT INTO car_sales_record(brand, subbrand, serie, serieId, sale_month, sales_volume) ' \
                  'VALUES(%s, %s, %s, %s, %s, %s)'
            cursor.executemany(sql, [(brand, subbrand, serie, serieId, saleRecord[0], saleRecord[1]) for saleRecord in saleRecordList])
            self.connection.commit()
        finally:
            cursor.close()

class CarState(IntEnum):
    OnSelling = 1
    StopSelling = 2
    Unlisted = 3

class CheZhuZhiJia(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    def __init__(self, dbManager, redisManager, log):
        self.dbManager = dbManager
        self.redisManager = redisManager
        self.log = log

    @staticmethod
    def getNativityContent(url, headers=None, defaultRequest=True):
        content = None
        if headers is None:
            content = Utility.getNativityContent(url, defaultRequest=defaultRequest)
        else:
            tmp = headers.copy()
            tmp.update(CheZhuZhiJia.headers)
            content = Utility.getNativityContent(url, headers=tmp, defaultRequest=defaultRequest)
        return str(content, encoding='utf-8')

    @staticmethod
    def getBrandSubbrandSerieMap():
        url = 'http://auto.16888.com/'
        content = CheZhuZhiJia.getNativityContent(url, {})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        brandSubbrandSerieMap = {}
        for brandBoxTag in soup.findAll('div', {'class': 'brand_box'}):
            brandName = brandBoxTag.find('a').get('name')
            brandSubbrandSerieMap[brandName] = {}
            brandListTag = brandBoxTag.find('div', {'class': 'brand_list f_r'})
            subbrandNameList = [h1.get_text() for h1 in brandListTag.findAll('h1')]
            ulListTag = [ul for ul in brandListTag.findAll('ul')]
            for i in range(len(subbrandNameList)):
                subbrandName = subbrandNameList[i]
                brandSubbrandSerieMap[brandName][subbrandName] = []
                ulTag = ulListTag[i]
                for liTag in ulTag.findAll('li'):
                    nameTag = liTag.find('span', {'class': 'name'}).find('a')
                    serieName = nameTag.get('title')
                    serieId = str(Utility.getIntFromStr(nameTag.get('href').replace('16888', '')))
                    carState = CarState.OnSelling
                    carStateTag = nameTag.find('div')
                    if carStateTag is not None:
                        if carStateTag.get('title') == '停产或国内没有在售':
                            carState = CarState.StopSelling
                        else:
                            carState = CarState.Unlisted
                    brandSubbrandSerieMap[brandName][subbrandName].append((serieId, serieName, carState))
        return brandSubbrandSerieMap


    @staticmethod
    def getNextPageUrl(tableViewTag, baseUrl):
        nextPageUrl = None
        pageTag = tableViewTag.find('div', {'class': 'xl-data-pageing lbBox'})
        if pageTag is not None:
            pageNextTag = pageTag.find('a', {'class': 'lineBlock next'})
            if pageNextTag is not None:
                nextPageUrl = baseUrl + pageNextTag.get('href')
        return nextPageUrl

    @staticmethod
    def getNextSaleVolumePageUrl(tableViewTag):
        return CheZhuZhiJia.getNextPageUrl(tableViewTag, 'http://xl.16888.com')

    def getSaleVolumeBySerieId(self, serieId):
        saleVolumeList = []
        url = 'https://xl.16888.com/s/%s/' % serieId
        while url is not None:
            content = CheZhuZhiJia.getNativityContent(url)
            soup = BeautifulSoup(content, MARKUP_TYPE)
            tableViewTag = soup.find('div', {'class': 'xl-table-view'})
            tableTag = tableViewTag.find('div', {'class': 'xl-table-data'}).find('table')
            trTags = tableTag.findAll('tr')[1:]
            if trTags[0].find('td', {'class':'table-nodata'}) is not None:
                return None
            for trTag in trTags:
                tdList = trTag.findAll('td', {'class': 'xl-td-t4'})
                yearMonth = tdList[0].get_text()
                if self.redisManager.isSerieSalesRecordExisted(serieId=serieId, sale_month=yearMonth) is False:
                    yearMonth += '-01'
                    number = tdList[1].get_text()
                    saleVolumeList.append((yearMonth, number))
            url = CheZhuZhiJia.getNextSaleVolumePageUrl(tableViewTag)
        return saleVolumeList

    def startCollectData(self):
        # 获取品牌-子品牌/生产商-车系的链接
        # 获取各品牌的所有生产商的所有车系的链接
        brandSubbrandSerieMap = CheZhuZhiJia.getBrandSubbrandSerieMap()
        saleVolumeMap = {}
        for brandName, subbrandMap in brandSubbrandSerieMap.items():
            self.log.info('品牌[%s]' % brandName)
            for subbrandName, serieList in subbrandMap.items():
                self.log.info('厂商[%s]' % subbrandName)
                for (serieId, serieName, carState) in serieList:
                    serieName = serieName.replace(brandName, '')
                    self.log.info('系列[%s:%s], 销售状态[%s]' % (serieId, serieName, carState))
                    if carState == CarState.OnSelling:
                        saleVolumeMap[serieId] = self.getSaleVolumeBySerieId(serieId)
                        if saleVolumeMap[serieId] is not None and len(saleVolumeMap[serieId]) != 0:
                            self.log.info(saleVolumeMap[serieId])
                            self.dbManager.insertSaleRecordListIntoDB(brand=brandName, subbrand=subbrandName, serie=serieName, serieId=serieId, saleRecordList=saleVolumeMap[serieId])
                            for (sale_month, sale_volume) in saleVolumeMap[serieId]:
                                self.redisManager.addSerieSalesRecord(serieId=serieId, sale_month=sale_month, sale_volume=sale_volume)

if __name__ == '__main__':
    mySqlManager = DBManager()
    redisManager = CacheManager()
    log = Logger.getLogger(logFileName='chezhuzhijia.log', loggerName='chezhuzhijia')
    czzj = CheZhuZhiJia(dbManager=mySqlManager, redisManager=redisManager, log=log)
    czzj.startCollectData()

