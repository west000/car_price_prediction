#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'West'

from bs4 import BeautifulSoup
import sys, os, time, random, re
import redis, pymysql
import json, re
from model import CarBaseInfo, CarBodyInfo, CarPowerSystem, CarChassisBrake, CarSecurityConfiguration, CarDriveAssistance, \
    CarExternalConfiguration, CarInternalConfiguration, CarSeatConfiguration, CarInfotainment, \
    CarPrice, CarDealer
from logger import Logger
from utility import Utility
from config import configs
import urllib, requests

MARKUP_TYPE = configs.markup_type

class AutoHome(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    @staticmethod
    def getNativityContent(url, headers=None, defaultRequest=True):
        content = None
        if headers is None:
            content = Utility.getNativityContent(url, defaultRequest=defaultRequest)
        else:
            tmp = headers.copy()
            tmp.update(AutoHome.headers)
            content = Utility.getNativityContent(url, headers=tmp, defaultRequest=defaultRequest)
        return content.decode('gb2312', 'ignore')

    @staticmethod
    def getCarBrandMap():
        url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0'
        content = AutoHome.getNativityContent(url, {})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        carTreeTag = soup.findAll('li')
        brandMap = {}
        for carTag in carTreeTag:
            brand = carTag.find('h3').get_text().replace(carTag.find('em').get_text(), '')
            url = 'https://car.autohome.com.cn' + carTag.find('a').get('href')
            brandMap[brand] = url
            # print(brand, url)
        return brandMap

if __name__ == '__main__':

    sys.setrecursionlimit(3000)

    url = 'https://car.autohome.com.cn'
    url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=15%20&fctId=0%20&seriesId=0'

    brand = '宝马'
    stateUrlMap = {'在售':'https://car.autohome.com.cn/price/brand-15.html',
                   '即将销售':'https://car.autohome.com.cn/price/brand-15-0-2-1.html',
                   '停售':'https://car.autohome.com.cn/price/brand-15-0-3-1.html'}

    stateUrlMap = {'停售':'https://car.autohome.com.cn/price/brand-15-0-3-1.html'}
    # stateUrlMap = {
    #     '在售':'https://car.autohome.com.cn/price/brand-34.html',
    #     '即将销售': 'https://car.autohome.com.cn/price/brand-34-0-2-1.html',
    #     '停售': 'https://car.autohome.com.cn/price/brand-34-0-3-1.html',
    # }

    for state, url in stateUrlMap.items():
        print('==================', state)
        brandTabTagLst = []
        requestSuffix = None
        nextSaleUrl = None
        while True:
            content = AutoHome.getNativityContent(url, {})
            soup = BeautifulSoup(content, MARKUP_TYPE)
            if requestSuffix is None:
                requestSuffix = soup.find('div', {'class':'header'}).find('li', {'class':'current'}).find('a').get('href')
                # print(requestSuffix)
            brandTabTag = soup.find('div', {'id':'brandtab-1', 'class':'tab-content-item current'})
            if brandTabTag.find('div', {'class':'sale-none'}, text='抱歉，没有找到符合条件的车') is not None:
                print('url[%s]抱歉，没有找到符合条件的车' % url)
                break


            listContTags = brandTabTag.findAll('div', {'class': 'list-cont'})
            listSpecTags = brandTabTag.findAll('div', {'class':'intervalcont fn-hide'})
            if len(listContTags) != len(listSpecTags):
                print('Error: len(listContTags) != len(listSpecTags) ')
                print(len(listContTags))
                print(len(listSpecTags))
                quit()

            for i in range(len(listContTags)):
                '''one serie'''
                contTag = listContTags[i]
                specTag = listSpecTags[i]

                serieId = contTag.get('data-value')
                serieName = contTag.find('div', {'class': 'list-cont-main'}).find('div', {'class': 'main-title'}).find(
                    'a', {'target': '_self'}).get_text()
                print('-------------------------------', serieId, serieName)
                url = 'https://carif.api.autohome.com.cn/koubei/LoadKoubeiData.ashx?_callback=loadKoubeiSpecSuccess&seriesid=%s&typeid=3' % serieId
                content = AutoHome.getNativityContent(url, {})
                jsonData = re.match(r'loadKoubeiSpecSuccess\((.*?)\)', content).group(1)
                jsonData = json.loads(jsonData)
                result = jsonData['result']
                if result is None:
                    print('Waring, serieId[%s] has not any speck' % serieId)
                    continue

                carSpecCountMap = {}
                countList = result['CountList']
                for countMap in countList:
                    carId = str(countMap['SpecId'])
                    counts = countMap['Counts']
                    carSpecCountMap[carId] = counts
                print(carSpecCountMap)

                # divSpecListTag = brandTabTag.find('div', {'id': 'divSpecList' + serieId})
                '''one car info: carId, version， koubei'''
                divSpecListTag = specTag
                carRowTags = divSpecListTag.find('ul', {'class': 'interval01-list'}).findAll('li')
                for rowTag in carRowTags:
                    carId = rowTag.get('data-value')
                    if carId is None:
                        continue
                    # print(carId)
                    version = rowTag.find('div', {'class': 'interval01-list-cars'}).find('p').get_text()
                    spkUrl = None
                    if carId in carSpecCountMap:
                        spkUrl = 'https://k.autohome.com.cn/spec/%s' % carId + requestSuffix
                    else:
                        print('carId[%s] 暂无口碑' % carId)
                    print(carId, version, spkUrl)
                print(divSpecListTag)
                quit()


            pricePageTage = brandTabTag.find('div', {'class':'price-page'})
            if pricePageTage is None:
                break
            nextPageTag = pricePageTage.find('a', text='下一页')
            if nextPageTag is None or nextPageTag.get('href') == 'javascript:void(0)':
                break
            else:
                url = 'https://car.autohome.com.cn' + nextPageTag.get('href')
                print(url)

        # for brandTabTag in brandTabTagLst:
        #     listContTags = brandTabTag.findAll('div', {'class': 'list-cont'})
        #     for contTag in listContTags:
        #         '''one serie'''
        #         serieId = contTag.get('data-value')
        #         serieName = contTag.find('div', {'class': 'list-cont-main'}).find('div', {'class': 'main-title'}).find(
        #             'a', {'target': '_self'}).get_text()
        #         print('-------------------------------', serieId, serieName)
        #         url = 'https://carif.api.autohome.com.cn/koubei/LoadKoubeiData.ashx?_callback=loadKoubeiSpecSuccess&seriesid=%s&typeid=3' % serieId
        #         content = AutoHome.getNativityContent(url, {})
        #         jsonData = re.match(r'loadKoubeiSpecSuccess\((.*?)\)', content).group(1)
        #         jsonData = json.loads(jsonData)
        #         result = jsonData['result']
        #         if result is None:
        #             print('Waring, serieId[%s] has not any speck' % serieId)
        #             continue
        #         carSpecCountMap = {}
        #         countList = result['CountList']
        #         for countMap in countList:
        #             carId = str(countMap['SpecId'])
        #             counts = countMap['Counts']
        #             carSpecCountMap[carId] = counts
        #         print(carSpecCountMap)
        #
        #         divSpecListTag = brandTabTag.find('div', {'id': 'divSpecList' + serieId})
        #         '''one car info: carId, version， koubei'''
        #         carRowTags = divSpecListTag.find('ul', {'class': 'interval01-list'}).findAll('li')
        #         for rowTag in carRowTags:
        #             carId = rowTag.get('data-value')
        #             if carId is None:
        #                 continue
        #             # print(carId)
        #             version = rowTag.find('div', {'class': 'interval01-list-cars'}).find('p').get_text()
        #             spkUrl = None
        #             if carId in carSpecCountMap:
        #                 spkUrl = 'https://k.autohome.com.cn/spec/%s' % carId + requestSuffix
        #             else:
        #                 print('carId[%s] 暂无口碑' % carId)
        #             print(carId, version, spkUrl)

