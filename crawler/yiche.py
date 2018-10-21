#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'

from bs4 import BeautifulSoup
import redis, pymysql, time
import json, re
from model import CarBaseInfo, CarBodyInfo, CarPowerSystem, CarChassisBrake, CarSecurityConfiguration, CarDriveAssistance, \
    CarExternalConfiguration, CarInternalConfiguration, CarSeatConfiguration, CarInfotainment, \
    CarPrice, CarDealer
from logger import Logger
from utility import Utility
from config import configs
from multiprocessing import Pool

MARKUP_TYPE = configs.markup_type
MAX_RETRY_TIMES = configs.max_retry_times
THREAD_NUM = configs.yiche.thread_num

class CacheManager:
    def __init__(self):
        pool = redis.ConnectionPool(host=configs.redis.host, port=configs.redis.port)
        self.redis = redis.Redis(connection_pool=pool)

    def isCarDetailExisted(self, carId):
        return self.redis.sismember('yiche-info-carid',carId)

    def addCarDetailByCarId(self, carId):
        self.redis.sadd('yiche-info-carid', carId)

    def removeCarId(self, carId):
        self.redis.srem('yiche-info-carid', carId)
        self.redis.srem('yiche-onselling-carid', carId)
        self.redis.srem('yiche-stopselling-carid', carId)

    def isCarOnSelling(self, carId):
        return self.redis.sismember('yiche-onselling-carid', carId)

    def addOnSellingCarId(self, carId):
        self.redis.sadd('yiche-onselling-carid', carId)

    def removeCarIdFromOnSellingSet(self, carId):
        self.redis.srem('yiche-onselling-carid', carId)

    def isCarStopSelling(self, carId):
        return self.redis.sismember('yiche-stopselling-carid', carId)

    def addStopSellingCarId(self, carId):
        self.redis.sadd('yiche-stopselling-carid', carId)

    def removeCarIdFromStopSellingSet(self, carId):
        self.redis.srem('yiche-stopselling-carid', carId)

    def addCarDealerPrice(self, carPrice):
        k, v = carPrice.generateCarPriceKeyValue()
        self.redis.hset('yiche-carprice', key=k, value=v)

    def isCarDealerPriceExisted(self, carPrice):
        k, v = carPrice.generateCarPriceKeyValue()
        return self.redis.hget('yiche-carprice', key=k) is not None

    def removeCarDealerPrice(self, carPrice):
        k, v = carPrice.generateCarPriceKeyValue()
        self.redis.hdel('yiche-carprice', key=k)

    def addDealerId(self, dealerId):
        self.redis.sadd('yiche-dealerid', dealerId)

    def isDealerIdExisted(self, dealerId):
        return self.redis.sismember('yiche-dealerid', dealerId)

    def removeDealerId(self, dealerId):
        self.redis.srem('yiche-dealerid', dealerId)

    def isCarPriceHadCollectedToday(self, carId):
        today = Utility.getCurrentDate(format='%Y_%m_%d')
        setName = 'yiche-collected-carprice-' + today
        return self.redis.sismember(setName, carId)

    def addCarPriceHadCollectedToday(self, carId):
        today = Utility.getCurrentDate(format='%Y_%m_%d')
        setName = 'yiche-collected-carprice-' + today
        self.redis.sadd(setName, carId)



class DBManager:
    def __init__(self, log):
        self.connection = pymysql.connect(host=configs.db.host, port=configs.db.port, user=configs.db.user, password=configs.db.password,
                                      db=configs.db.db, charset=configs.db.charset, cursorclass=pymysql.cursors.DictCursor)
        self.log = log

    def __del__(self):
        self.connection.close()

    def getAllCarIdFromCarBaseInfo(self):
        cursor = self.connection.cursor()
        carIds = None
        try:
            sql = 'SELECT unique_id FROM car_base_info'
            cursor.execute(sql)
            result = cursor.fetchall()
            carIds = [item['unique_id'] for item in result]
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return carIds

    def getAllDealerIdFromCarDealer(self):
        cursor = self.connection.cursor()
        dealerIds = None
        try:
            sql = 'SELECT id FROM car_dealer'
            cursor.execute(sql)
            result = cursor.fetchall()
            dealerIds = [item['id'] for item in result]
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return dealerIds

    def getAllOnSellingCarId(self):
        return self._getCarIdsBySellStatus(is_stop_sell=False)

    def getAllStopSellingCarId(self):
        return self._getCarIdsBySellStatus(is_stop_sell=True)

    def _getCarIdsBySellStatus(self, is_stop_sell):
        cursor = self.connection.cursor()
        carIds = None
        try:
            sql = 'SELECT unique_id FROM car_base_info WHERE stop_selling=%s' % is_stop_sell
            cursor.execute(sql)
            result = cursor.fetchall()
            carIds = [item['unique_id'] for item in result]
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return carIds

    def insertCarDetailIntoDB(self, carDetail):
        cursor = self.connection.cursor()
        try:
            tableNameList = ['car_base_info','car_body_info','car_power_system','car_chassis_brake',
                             'car_security_configuration','car_drive_assistance','car_external_configuration',
                             'car_internal_configuration','car_seat_configuration','car_infotainment']

            detailList = [carDetail.baseInfo, carDetail.bodyInfo, carDetail.powerSystem, carDetail.chassisBrake,
                          carDetail.securityConfiguration, carDetail.driveAssistance, carDetail.externalConfiguration,
                          carDetail.internalConfiguration, carDetail.seatConfiguration, carDetail.infotainment]
            sqlList = []
            for i in range(len(tableNameList)):
                tableName = tableNameList[i]
                valuesName = ', '.join(detailList[i].__slots__)
                formatStr = '%s, ' * len(detailList[i].__slots__)
                formatStr = formatStr[:-2]
                sql = 'INSERT INTO %s(%s) VALUES(%s)' % (tableName, valuesName, formatStr)
                # print(sql)
                sqlList.append(sql)

            for i in range(len(detailList)):
                detail = detailList[i]
                values = tuple(detail.__getattr__(key) for key in detail.__slots__)
                try:
                    cursor.execute(sqlList[i], values)
                except Exception as e:
                    message = str(e)
                    if re.search('.*?Duplicate entry.*?', message) is not None:
                        pass
                        # self.log.warning('Duplicate key in TABLE[%s], unique_id[%s] has existed' % (tableNameList[i], detail.unique_id))
                    else:
                        raise e
            self.connection.commit()
        except Exception as e:
            self.log.error(e)
            quit()
        finally:
            cursor.close()

    def updateSellState(self, carIdList, isStopSelling):
        if carIdList is None or len(carIdList) == 0:
            return None
        else:
            formatStr = '%s, ' * len(carIdList)
            formatStr = formatStr[:-2]
            sql = 'UPDATE car_base_info SET stop_selling = %s WHERE unique_id in (%s)' % ('%s', formatStr)
            values = carIdList
            values.insert(0, isStopSelling)
            values = tuple(values)
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, values)
                self.connection.commit()
            except Exception as e:
                self.log.error(e)
                self.log.error(('update car_base_info failed', 'carList', carIdList, 'change stop_selling to ', isStopSelling))
                quit()
            finally:
                cursor.close()

    def insertCarPriceListIntoDB(self, carPriceList, redisManager):
        cursor = self.connection.cursor()
        try:
            sql = 'INSERT INTO car_price(carid, dealer_id, sales_price, is_promotion, publish_date, end_date) '\
                  'VALUES(%s, %s, %s, %s, %s, %s)'
            for carPrice in carPriceList:
                try:
                    cursor.execute(sql, carPrice.toTuple())
                except Exception as e:
                    message = str(e)
                    # self.log.warning('carId[%s], dealer_id[%s], price_url[%s]' % (carPrice.carid, carPrice.dealer_id, carPrice.price_url))
                    if re.search('.*?car_dealer.*?', message) is not None:
                        # self.log.warning('TABLE car_dealer id NOT EXIST')
                        # 由于表car_dealer中没有对应dealerId，需删除redis中的dealerId，让下次爬取数据时重新将dealerId的数据保存到表car_dealer中
                        redisManager.removeDealerId(carPrice.dealer_id)
                    elif re.search('.*?car_base_info.*?', message) is not None:
                        # self.log.warning('TABLE car_base_info unique_id NOT EXIST')
                        # 由于表car_base_info中没有对应的unique_id，需删除redis中记录的carId，让下次爬取数据时重新将carId的配置数据保存到表car_base_info中
                        redisManager.removeCarId(carPrice.carid)
                    else:
                        raise e
            # cursor.executemany(sql, [carPrice.toTuple() for carPrice in carPriceList])
            self.connection.commit()
        except Exception as e:
            self.log.error(e)
            quit()
        finally:
            cursor.close()

    def insertDealerListIntoDB(self, dealerList):
        cursor = self.connection.cursor()
        try:
            sql = 'INSERT INTO car_dealer(id, province, city, area, name, full_name, type, address, official_webstie, sale_phone_number, contact_number) ' \
                  'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            for dealer in dealerList:
                try:
                    cursor.execute(sql, dealer.toTuple())
                except Exception as e:
                    message = str(e)
                    if re.search('.*?Duplicate entry.*?', message) is not None:
                        pass
                        # self.log.warning('Duplicate key in TABLE[car_dealer], id[%s] has existed' % dealer.id)
                    else:
                        raise e
            # cursor.executemany(sql, [dealer.toTuple() for dealer in dealerList])
            self.connection.commit()
        except Exception as e:
            self.log.error(e)
            quit()
        finally:
            cursor.close()

    def _dealOneCarPrice(self, carId):
        cursor = self.connection.cursor()
        try:
            sql = 'SELECT id, dealer_id, sales_price, is_promotion, publish_date, end_date FROM car_price ' \
                  'WHERE carid=\'%s\' ORDER BY dealer_id, publish_date' % carId
            cursor.execute(sql)
            result = cursor.fetchall()

            if len(result) > 1:
                begin_dealer_id = None
                dealerMap = {}
                i, rlen = 0, len(result)
                while i < rlen:
                    if begin_dealer_id is None:
                        begin_dealer_id = result[i]['dealer_id']
                        dealerMap[begin_dealer_id] = [result[i], ]
                        i += 1
                    while i < rlen and result[i]['dealer_id'] == begin_dealer_id:
                        dealerMap[begin_dealer_id].append(result[i])
                        i += 1
                    begin_dealer_id = None
                removeIds = []
                modify_eds = []
                for itemList in dealerMap.values():
                    if len(itemList) <= 1:
                        continue
                    i, n = 0, 0
                    while i < len(itemList):
                        begin_index = i
                        price = itemList[i]['sales_price']
                        i += 1
                        end_date = None
                        need_modify = False
                        while i < len(itemList) and itemList[i]['sales_price'] == price:
                            need_modify = True
                            removeIds.append(itemList[i]['id'])
                            end_date = itemList[i]['end_date']
                            i += 1
                        if need_modify is True:
                            modify_date = None
                            if i < len(itemList):
                                if end_date is None:
                                    dateStr = itemList[i]['publish_date'].strftime('%Y-%m-%d')
                                    modify_date = Utility.getBeforeDate(dateStr)
                                else:
                                    modify_date = end_date
                            else:
                                modify_date = end_date
                            modify_eds.append((modify_date, itemList[begin_index]['id']))

                # print(removeIds)
                # print(modify_eds)
                sql = 'DELETE FROM car_price WHERE id=%s'
                cursor.executemany(sql, removeIds)
                sql = 'UPDATE car_price SET end_date=%s WHERE id=%s'
                cursor.executemany(sql, modify_eds)
                self.connection.commit()
            self.connection.commit()
        except Exception as e:
            print(e)
            quit()

    def dealCarPrice(self):
        cursor = self.connection.cursor()
        try:
            sql = 'SELECT unique_id FROM car_base_info WHERE stop_selling is False'
            cursor.execute(sql)
            result = cursor.fetchall()
            self.connection.commit()
            carIds = [item['unique_id'] for item in result]
            for carId in carIds:
                print(carId)
                self._dealOneCarPrice(carId)
        except Exception as e:
            print(e)
            quit()


# 一辆车的所有配置信息
class CarDetail:
    def __init__(self):
        self.baseInfo = None
        self.bodyInfo = None
        self.powerSystem = None
        self.chassisBrake = None
        self.securityConfiguration = None
        self.driveAssistance = None
        self.externalConfiguration = None
        self.internalConfiguration = None
        self.seatConfiguration = None
        self.infotainment = None

    def toTuple(self):
        return self.__dict__

    def saveToDB(self, dbManager):
        dbManager.insertCarDetailIntoDB(self)


class YiChe:
    baseCarInfoUrl = configs.yiche.carinfo_base_url
    basePriceUrl = configs.yiche.price_base_url
    carInfoLeftTreeJsonUrl = configs.yiche.carinfo_lefttreejson_url
    priceLeftTreeJsonUrl = configs.yiche.price_lefttreejson_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    def __init__(self, redisManager, dbManager, log, brandCarInfoUrlMap):
        self.redisManager = redisManager
        self.dbManager = dbManager
        self.log = log
        self.brandCarInfoUrlMap = brandCarInfoUrlMap

    @staticmethod
    def getNativityContent(url, headers=None, defaultRequest=True):
        content = None
        if headers is None:
            content = Utility.getNativityContent(url, defaultRequest=defaultRequest)
        else:
            tmp = headers.copy()
            tmp.update(YiChe.headers)
            content = Utility.getNativityContent(url, headers=tmp, defaultRequest=defaultRequest)
        if content is None:
            return None
        return str(content, encoding='utf-8')

    @staticmethod
    def getAttrValueByName(table, name, tagType='span'):
        tag = table.find(tagType, text=name+'：')
        if tag is None:
            return None
        result = tag.parent.next_sibling.next_sibling.find('span')
        if result is None:
            optionList = tag.parent.next_sibling.next_sibling.findAll('div', {'class':'l'})
            optionList = [r.text for r in optionList]
            result = '|'.join(optionList)
            # print(result)
        else:
            result = result.get_text()
        return result

    @staticmethod
    def getCarBaseInfo(table, carId):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        baseInfo = CarBaseInfo()
        for attr, name in CarBaseInfo.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            baseInfo.__setattr__(name, value)
        baseInfo.__setattr__('unique_id', carId)
        # 外观颜色另做处理
        tagList = table.find('td', text='外观颜色：').next_sibling.findAll('a')
        color = ''
        color_code = ''
        for tag in tagList:
            color += tag['title'] + '|'
            style = tag.find('span').get('style')
            color_code += style.replace('background:', '') + '|'
        baseInfo.exterior_color = color[:-1]
        baseInfo.exterior_color_code = color_code[:-1]
        # print(baseInfo)
        return baseInfo

    @staticmethod
    def getCarBodyInfo(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        bodyInfo = CarBodyInfo()
        for attr, name in CarBodyInfo.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            bodyInfo.__setattr__(name, value)
        bodyInfo.__setattr__('unique_id', unique_id)
        # print(bodyInfo)
        return bodyInfo

    @staticmethod
    def getCarPowerSystem(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carPowerSystem = CarPowerSystem()
        for attr, name in CarPowerSystem.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carPowerSystem.__setattr__(name, value)
        carPowerSystem.__setattr__('unique_id', unique_id)
        # print(carPowerSystem)
        return carPowerSystem

    @staticmethod
    def getCarChassisBrake(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carChassisBrake = CarChassisBrake()
        for attr, name in CarChassisBrake.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carChassisBrake.__setattr__(name, value)
        carChassisBrake.__setattr__('unique_id', unique_id)
        # print(carChassisBrake)
        return carChassisBrake

    @staticmethod
    def getCarSecurityConfiguration(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carSecurityConfiguration = CarSecurityConfiguration()
        for attr, name in CarSecurityConfiguration.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carSecurityConfiguration.__setattr__(name, value)
        carSecurityConfiguration.__setattr__('unique_id', unique_id)
        # print(carSecurityConfiguration)
        return carSecurityConfiguration

    @staticmethod
    def getCarDriveAssistance(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carDriveAssistance = CarDriveAssistance()
        for attr, name in CarDriveAssistance.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carDriveAssistance.__setattr__(name, value)
        carDriveAssistance.__setattr__('unique_id', unique_id)
        # print(carDriveAssistance)
        return carDriveAssistance

    @staticmethod
    def getCarExternalConfigurationn(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carExternalConfiguration = CarExternalConfiguration()
        for attr, name in CarExternalConfiguration.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carExternalConfiguration.__setattr__(name, value)
        carExternalConfiguration.__setattr__('unique_id', unique_id)
        # print(carExternalConfiguration)
        return carExternalConfiguration

    @staticmethod
    def getCarInternalConfiguration(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carInternalConfiguration = CarInternalConfiguration()
        for attr, name in CarInternalConfiguration.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carInternalConfiguration.__setattr__(name, value)
        carInternalConfiguration.__setattr__('unique_id', unique_id)
        # print(carInternalConfiguration)
        return carInternalConfiguration

    @staticmethod
    def getCarSeatConfiguration(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carSeatConfiguration = CarSeatConfiguration()
        for attr, name in CarSeatConfiguration.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carSeatConfiguration.__setattr__(name, value)
        carSeatConfiguration.__setattr__('unique_id', unique_id)
        # print(carSeatConfiguration)
        return carSeatConfiguration

    @staticmethod
    def getCarInfotainment(table, unique_id):
        if table is None:
            return None
        table = table.parent.next_sibling.next_sibling
        carInfotainment = CarInfotainment()
        for attr, name in CarInfotainment.__attrname__.items():
            value = YiChe.getAttrValueByName(table, attr)
            carInfotainment.__setattr__(name, value)
        carInfotainment.__setattr__('unique_id', unique_id)
        # print(carInfotainment)
        return carInfotainment

    def getCarDetailConfiguration(self, url, carId, brand, subbrand, serie, version, isStopSelling):
        if self.redisManager.isCarDetailExisted(carId) is True:
            return None

        self.log.info('CarId[%s]配置信息，Url[%s]' % (carId, url))
        carDetail = CarDetail()
        content = YiChe.getNativityContent(url=url)
        if content is None:
            return
        soup = BeautifulSoup(content, MARKUP_TYPE)
        baseInfoTable = soup.find('h6', text='基本信息')
        baseInfo = YiChe.getCarBaseInfo(baseInfoTable, carId)
        if baseInfo is None:
            # self.log.warning('找不到CarId[%s]的基本信息，Url[%s]' % (carId, url))
            return None
        baseInfo.brand = brand
        baseInfo.subbrand = subbrand
        baseInfo.series = serie
        baseInfo.version = version
        baseInfo.stop_selling = isStopSelling
        baseInfo.source_url = url
        # 图片链接
        imgList = soup.find('div', {'class':'content clearfix'}).find('div', {'class':'img'}).findAll('a')
        if len(imgList) == 2:
            img_url = imgList[0].find('img').get('src')
            real_shot_img_link = imgList[1].get('href')
            baseInfo.img_url = img_url
            baseInfo.real_shot_img_link = real_shot_img_link
        carDetail.baseInfo = baseInfo

        bodyInfoTable = soup.find('h6', text='车身尺寸')
        bodyInfo = YiChe.getCarBodyInfo(bodyInfoTable, carId)
        if bodyInfo is None:
            bodyInfo = CarBodyInfo()
            bodyInfo.unique_id = carId
        carDetail.bodyInfo = bodyInfo

        carPowerSystemTable = soup.find('h6', text='动力系统')
        carPowerSystem = YiChe.getCarPowerSystem(carPowerSystemTable, carId)
        if carPowerSystem is None:
            carPowerSystem = CarPowerSystem()
            carPowerSystem.unique_id = carId
        carDetail.powerSystem = carPowerSystem

        carChassisBrakeTable = soup.find('h6', text='底盘制动')
        carChassisBrake = YiChe.getCarChassisBrake(carChassisBrakeTable, carId)
        if carChassisBrake is None:
            carChassisBrake = CarChassisBrake()
            carChassisBrake.unique_id = carId
        carDetail.chassisBrake = carChassisBrake

        carSecurityConfigurationTable = soup.find('h6', text='安全配置')
        carSecurityConfiguration = YiChe.getCarSecurityConfiguration(carSecurityConfigurationTable, carId)
        if carSecurityConfiguration is None:
            carSecurityConfiguration = CarSecurityConfiguration()
            carSecurityConfiguration.unique_id = carId
        carDetail.securityConfiguration = carSecurityConfiguration

        carDriveAssistanceTable = soup.find('h6', text='驾驶辅助')
        carDriveAssistance = YiChe.getCarDriveAssistance(carDriveAssistanceTable, carId)
        if carDriveAssistance is None:
            carDriveAssistance = CarDriveAssistance()
            carDriveAssistance.unique_id = carId
        carDetail.driveAssistance = carDriveAssistance

        carExternalConfigurationnTable = soup.find('h6', text='外部配置')
        carExternalConfigurationn = YiChe.getCarExternalConfigurationn(carExternalConfigurationnTable, carId)
        if carExternalConfigurationn is None:
            carExternalConfigurationn = CarExternalConfiguration()
            carExternalConfigurationn.unique_id = carId
        carDetail.externalConfiguration = carExternalConfigurationn

        carInternalConfigurationTable = soup.find('h6', text='内部配置')
        carInternalConfiguration = YiChe.getCarInternalConfiguration(carInternalConfigurationTable, carId)
        if carInternalConfiguration is None:
            carInternalConfiguration = CarInternalConfiguration()
            carInternalConfiguration.unique_id = carId
        carDetail.internalConfiguration = carInternalConfiguration

        carSeatConfigurationTable = soup.find('h6', text='座椅配置')
        carSeatConfiguration = YiChe.getCarSeatConfiguration(carSeatConfigurationTable, carId)
        if carSeatConfiguration is None:
            carSeatConfiguration = CarSeatConfiguration()
            carSeatConfiguration.unique_id = carId
        carDetail.seatConfiguration = carSeatConfiguration

        carInfotainmentTable = soup.find('h6', text='信息娱乐')
        carInfotainment = YiChe.getCarInfotainment(carInfotainmentTable, carId)
        if carInfotainment is None:
            carInfotainment = CarInfotainment()
            carInfotainment.unique_id = carId
        carDetail.infotainment = carInfotainment

        try:
            self.log.info(('CarId[%s]的配置信息为' % carId, carDetail.toTuple()))
            carDetail.saveToDB(self.dbManager)
            self.redisManager.addCarDetailByCarId(carId)
        except Exception as e:
            self.log.error(e)
            quit()

    '''保存一个系列所有款车的配置信息'''
    def saveOneSerieCarDetails(self, brand, subBrand, serie, versionList):
        for carId, version, url, isStopSelling in versionList:
            self.getCarDetailConfiguration(url=url, carId=carId, brand=brand, subbrand=subBrand, serie=serie, version=version, isStopSelling=isStopSelling)

    @staticmethod
    def getAllBrandUrl(url, baseUrl):
        content = YiChe.getNativityContent(url)
        result = re.search(r'JsonpCallBack\((.*?)\)', content)
        jsonData = result.group(1)
        # print(jsonData)
        charMap = re.search(r'char:\{(.*?)\},', jsonData).group(1)
        charList = []
        for kv in charMap.split(','):
            kv = kv.split(':')
            if kv[1] == '1':
                charList.append(kv[0])
        # print(charList)
        brandMap = {}
        for character in charList:
            brandList = re.search(character + r':\[(.*?)\]', jsonData).group(1)
            brandList = brandList[1:-1]
            for oneBrand in brandList.split('},{'):
                results = re.search(r'name:\"(.*?)\",url:\"(.*?)\",', oneBrand)
                name = results.group(1)
                url = baseUrl + results.group(2)
                # print(name, '-', url)
                brandMap[name] = url
        return brandMap

    @staticmethod
    def getOneSerieUrl(col, brandName):
        if col.find('li', {'class':'price'}).get_text() == '未上市':
            return (None, None)
        info = col.find('li', {'class':'name'}).find('a')
        serie = info['title'].replace(brandName, '').replace('(进口)', '')
        url = 'http://car.bitauto.com/' + info['href']
        return (serie, url)

    '''生成某一子品牌的所有车系的配置，具体到子品牌-车系'''
    @staticmethod
    def generateSubbrandSeries(tag, brandName):
        seriesMap = {}
        cols = tag.findAll('div', {'class': 'col-xs-3'})
        for col in cols:
            serie, url = YiChe.getOneSerieUrl(col, brandName)
            if serie is None:
                continue
            seriesMap[serie] = url
        return seriesMap

    '''获取某个品牌的所有车系的配置链接，具体到品牌-子品牌-车系'''
    @staticmethod
    def getOneBrandSubbrandSeries(brandName, url):
        content = YiChe.getNativityContent(url, {})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        mainSection = soup.find('div', {'class':'main-inner-section condition-selectcar type-3'})
        carSection = mainSection.find('div', {'id':re.compile('divCsLevel_0')})
        subBrandH5List = carSection.findAll('h5', {'class':'h5-sep'})
        subBrandNameList = []
        seriesMapList = []

        if len(subBrandH5List) == 0:
            subBrandNameList.append(brandName)
            seriesMap = YiChe.generateSubbrandSeries(carSection, brandName)
            seriesMapList.append(seriesMap)
        else:
            subBrandNameList = [subBrand.get_text().replace('>>','') for subBrand in subBrandH5List]
            for subBrandH5 in subBrandH5List:
                seriesMap = YiChe.generateSubbrandSeries(subBrandH5.next_sibling, brandName)
                seriesMapList.append(seriesMap)

        subBrandSeriesMap = {}
        for i in range(len(subBrandNameList)):
            subBrandSeriesMap[subBrandNameList[i]] = seriesMapList[i]
        # print(subBrandSeriesMap)
        return subBrandSeriesMap

    '''从某一车系页面（具体到车系-年份），获取该车系的版本列表'''
    @staticmethod
    def generateVersionUrlList(carBox, infoList, isStopSelling=False):
        versionList = carBox.findAll('td', {'class':'txt-left'})
        if versionList is None:
            return None
        for td in versionList:
            carId = Utility.getIntFromStr(td['id'])
            td = td.find('a')
            url = 'http://car.bitauto.com' + td['href']
            version = td.get_text()
            # print(carId, '-', version, '-', url)
            infoList.append((carId, version, url, isStopSelling))
        return infoList

    '''获取某一车系的所有版本，包括在售+停售'''
    def getOneSeriesAllVersionList(self, url):
        baseUrl = url
        content = YiChe.getNativityContent(baseUrl, {})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        allOnsaleCarBox = soup.find('div', {'id':'data_tab_jq5_0'})
        infoList = []
        isStopSelling = False
        if allOnsaleCarBox is None:
            self.log.debug('无在售车款')
        else:
            result = YiChe.generateVersionUrlList(allOnsaleCarBox, infoList, isStopSelling)
            if result is None:
                self.log.debug('[Error]在售车款列表为空', url)
        nosaleYearList = soup.find('div', {'id':'carlist_nosaleyear'})
        if nosaleYearList is None:
            self.log.debug('无停售车款')
        else:
            isStopSelling = True
            yearList = [ year['id'] for year in nosaleYearList.findAll('a')]
            csID = re.search(r'var CarCommonCSID = \"(.*?)\";', content).group(1)
            carIdMap = {}
            for year in yearList:
                url = 'http://car.bitauto.com/AjaxNew/GetNoSaleSerailListByYear.ashx?csID=%s&year=%s' % (csID, year)
                data = YiChe.getNativityContent(url)
                self.parseNoSaleSerailList(data, carIdMap)
            for carId, version in carIdMap.items():
                url = baseUrl + 'm' + carId
                infoList.append((carId, version, url, isStopSelling))
        return infoList

    def parseNoSaleSerailList(self, data, carIdMap):
        try:
            data = json.loads(data)
        except Exception as e:
            self.log.error(e)
            self.log.error('data[%s]' % data)
            return None
        for d in data:
            for car in d['carList']:
                carId, yearType, name = car['CarID'], car['YearType'], car['Name']
                carIdMap[carId] = yearType + ' ' + name

    @staticmethod
    def getAllBrandCarInfoUrl():
        return YiChe.getAllBrandUrl(YiChe.carInfoLeftTreeJsonUrl, YiChe.baseCarInfoUrl)

    @staticmethod
    def getAllBrandPriceUrl():
        return YiChe.getAllBrandUrl(YiChe.priceLeftTreeJsonUrl, YiChe.basePriceUrl)

    '''carId + carPriceUrl'''
    def getOneBrandAllSeriesPriceUrl(self, url):
        content = YiChe.getNativityContent(url, {'Host':'price.bitauto.com'})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        carPriceSection = soup.find('div', {'id':'c_result'})
        if carPriceSection is None:
            self.log.debug('暂无有效车型', url)
            return None
        carPriceList = carPriceSection.findAll('div', {'class':'col-xs-3'})
        priceMap = {}
        for carPriceTag in carPriceList:
            price = carPriceTag.find('li', {'class':'price'}).find('a')
            if price.get_text() == '暂无报价':
                continue
            url = YiChe.basePriceUrl + price.get('href')
            serieId = Utility.getIntFromStr(price.get('href'))
            priceMap[serieId] = url
        return priceMap

    def updateCacheAndDB(self, versionList):
        updateOnSellingCarIdList = []
        updateStopSellingCarIdList = []
        # 更新Cache
        for carId, version, url, isStopSelling in versionList:
            # 当前车辆停售
            if isStopSelling is True:
                self.redisManager.addStopSellingCarId(carId)
                # 如果之前车辆在售，则需要修改状态
                if self.redisManager.isCarOnSelling(carId) is True:
                    self.redisManager.removeCarIdFromOnSellingSet(carId)
                    updateOnSellingCarIdList.append(carId)
            else:
                self.redisManager.addOnSellingCarId(carId)
                # 如果之前车辆停售，现在变为在售，虽然这种情况几乎不可能，但不排除
                if self.redisManager.isCarStopSelling(carId) is True:
                    self.redisManager.removeCarIdFromStopSellingSet(carId)
                    updateStopSellingCarIdList.append(carId)
        if len(updateOnSellingCarIdList) != 0:
            self.log.info(('原本在售的车，现在开始停售', Utility.getCurrentDate(), updateOnSellingCarIdList))
        if len(updateStopSellingCarIdList) != 0:
            self.log.info(('原本停售的车，现在重新销售', Utility.getCurrentDate(), updateStopSellingCarIdList))
        # 更新DB
        self.dbManager.updateSellState(updateOnSellingCarIdList, True)
        self.dbManager.updateSellState(updateStopSellingCarIdList, False)

    @staticmethod
    def parseCarPrice(carId, dealerPriceInfo):
        dealerId = dealerPriceInfo['DealerInfo']['VendorId']
        priceUrl = 'http://dealer.bitauto.com/%s/price_detail/%s.html' % (dealerId, carId)
        price = int(float(dealerPriceInfo['CarDealerPriceInfo']['OrderPrice']) * 10000)
        publishDate = None
        endDate = None
        is_promotion = False
        if dealerPriceInfo['NewsDataInfo'] is None \
                or dealerPriceInfo['NewsDataInfo']['NewsType'] != 1 \
                or dealerPriceInfo['NewsDataInfo']['IsTemplateNewsClassId'] != 0:
            # 价格非促销价格，则publishDate表示爬取日期
            publishDate = Utility.getCurrentDate()
        else:
            publishDate = dealerPriceInfo['NewsDataInfo']['NewsPubTime']
            endDate = dealerPriceInfo['NewsDataInfo']['EndDateTime']
            is_promotion = True

        carPrice = CarPrice(carId=carId, dealer_id=dealerId, sales_price=price, is_promotion=is_promotion,
                            publish_date=publishDate, end_date=endDate, price_url=priceUrl)
        return carPrice

    def getDealerWebsiteTelesFullname(self, url):
        tryTimes = 0
        website, phones, fullname = None, None, None
        while True and tryTimes < MAX_RETRY_TIMES:
            content = YiChe.getNativityContent(url, headers={})
            soup = BeautifulSoup(content, MARKUP_TYPE)
            pageStyle = 0
            if fullname is None:
                InheaderTag = soup.find('div', {'class':'inheader'})
                if InheaderTag is not None:
                    fullname = InheaderTag.find('h1', {'class': 'name'}).get_text()
                elif soup.find('div', {'id':'lm_head'}) is not None:
                    pageStyle = 1
                else:
                    # self.log.warning('cannot find dealer fullName, url[%s], tryTime[%s]' % (url, tryTimes))
                    if soup.find('div', {'class':'zh_warning'}).find('h2').get_text() == '错误页面':
                        # self.log.warning('要访问的页面不存在!')
                        break
                    tryTimes += 1
                    Utility.randomSleep(60, 150)
                    continue

            if pageStyle == 0:
                infoTag = soup.find('div', {'class':'jxs_info'})
            elif pageStyle == 1:
                infoTag = soup.find('div', {'class': 'bizcardBlc'})

            website, phones = None, None
            if infoTag is not None:
                if pageStyle == 0:
                    websiteTag = infoTag.find('b', text='官网：').next_sibling.next_sibling
                    website = websiteTag.find('a').get('href')
                    phonesTag = infoTag.find('b', text='电话：').next_sibling.next_sibling
                    phones = phonesTag.find('em').get('data-tel').strip().replace(' ', '|')
                elif pageStyle == 1:
                    fullname = infoTag.find('h3').get('title')
                    website = infoTag.find('p', {'class': 'site'}).find('a').get_text()
                    phones = infoTag.find('p', {'class': 'tel'}).get('title')
                break
            else:
                # self.log.warning('cannot find dealer website and phones, url[%s], tryTimes[%s]' % (url, tryTimes))
                tryTimes += 1
                Utility.randomSleep(60, 150)
                continue
        return (website, phones, fullname)

    def parseCarDealer(self, url, dealerInfo):
        id = dealerInfo['VendorId']
        province = dealerInfo['PName']
        city = dealerInfo['CName']
        area = dealerInfo['LocationName']
        name = dealerInfo['VendorName']
        type = dealerInfo['VendorBizMode']
        address = dealerInfo['VendorSaleAddr']
        sale_phone_number = dealerInfo['VendorTel']
        website, teles, fullName = self.getDealerWebsiteTelesFullname(url)
        fullName = dealerInfo['VendorFullName']
        dealer = CarDealer(id=id, province=province, city=city, area=area, name=name, full_name=fullName, type=type, address=address,
                           official_website=website, sale_phone_number=sale_phone_number, contact_number=teles)
        return dealer

    # 快操作，因为直接调API
    def getCarPriceAndDealerList(self, data, carPriceList, dealerList):
        jsonData = re.search(r'jsonpDealerListdata\((.*)\)', data).group(1)
        jsonData = json.loads(jsonData)
        if jsonData['CarInfo'] is None:
            # self.log.warning(('cannot find any info!', 'data:[%s]' % data))
            return None
        carId = jsonData['CarInfo']['CarId']
        if jsonData['DealerPriceInfos'] is None:
            # self.log.warning(('can not find carId[%s] DealerPriceInfos' % carId, 'data:[%s]' % data))
            return None
        for dealerPriceInfo in jsonData['DealerPriceInfos']:
            # print(dealerPriceInfo)
            carPrice = YiChe.parseCarPrice(carId=carId, dealerPriceInfo=dealerPriceInfo)
            # print(carPrice.__dict__)
            if self.redisManager.isCarDealerPriceExisted(carPrice) is False:
                carPriceList.append(carPrice)
                self.redisManager.addCarDealerPrice(carPrice)
            dealerId = dealerPriceInfo['DealerInfo']['VendorId']
            if self.redisManager.isDealerIdExisted(dealerId) is False:
                dealer = self.parseCarDealer(url=carPrice.price_url, dealerInfo=dealerPriceInfo['DealerInfo'])
                # print(dealer.__dict__)
                dealerList.append(dealer)
                self.redisManager.addDealerId(dealerId)
        return ' '

    # 慢操作，因为需要访问/baojia/c0，解析页面获取信息
    def getCarPriceAndDealerListFromBaoJia(self, carId, url, carPriceList, dealerList):
        content = YiChe.getNativityContent(url, {})
        if content is None:
            return None
        soup = BeautifulSoup(content, MARKUP_TYPE)
        provinceTextListTag = soup.find('ul', {'class':'layer-txt-list'})
        if provinceTextListTag is None:
            return None
        provinceTextList = provinceTextListTag.findAll('li')
        provinceTextList = provinceTextList[1:]
        provinceUrlMap = {}
        for provinceText in provinceTextList:
            tag = provinceText.find('a')
            spanText = provinceText.find('span').get_text()
            province = tag.get_text().replace(spanText, '')
            url = tag.get('href').split('?', 1)[0]
            url = YiChe.baseCarInfoUrl + url
            provinceUrlMap[province] = url
        self.log.info(('经销商所在的所有省份',provinceUrlMap))
        for province, url in provinceUrlMap.items():
            self.getCarPriceAndDealerListFromBaoJiaByProvince(carId, province, url, carPriceList, dealerList)

    @staticmethod
    def getSalePhoneNumberByDealerId(dealerId):
        url = 'http://autocall.bitauto.com/eil/das2.ashx?userid=%s&mediaid=10&source=bitauto' % dealerId
        content = YiChe.getNativityContent(url)
        result = None
        if content is not None:
            result = re.search(r'"tel":"(.*)"', content)
        return None if result is None else result.group(1)

    def parseCarPriceFromBaoJia(self, rowOfferTag, carId):
        mainInfo = rowOfferTag.find('div', {'class': 'col-xs-6 left'})
        dealerId = mainInfo.find('p', {'class': 'add'}).find('input', {'name': 'vendorId'}).get('value')
        priceUrl = 'http://dealer.bitauto.com/%s/price_detail/%s.html' % (dealerId, carId)
        isPromotion = False
        publishDate, endDate = None, None
        salesPrice = None
        nowPriceTag = rowOfferTag.find('h3', {'class': 'now-price'}).find('a', {'target': '_blank'})
        if nowPriceTag.find('i', {'class': 'promote popup-control-box'}) is not None:
            promoteUrl = nowPriceTag.get('href')
            publishDate, endDate = self.getPublishAndEndDateFromPromotePage(promoteUrl)
            if publishDate is not None and endDate is not None:
                isPromotion = True
        else:
            publishDate = Utility.getCurrentDate()
        salesPrice = nowPriceTag.find('em').get_text()
        salesPrice = int(float(Utility.getFloatFromStr(salesPrice)) * 10000)
        carPrice = CarPrice(carId=carId, dealer_id=dealerId, sales_price=salesPrice, is_promotion=isPromotion,
                            publish_date=publishDate, end_date=endDate, price_url=priceUrl)
        return carPrice

    def parseCarDealerFromBaoJia(self, rowOfferTag, dealerId, province, type, priceUrl):
        city, area = None, None
        addList = rowOfferTag.find('div', {'class': 'col-xs-7 middle'}).find('p', {'class': 'add'}).get_text().split(' ')
        city = addList[0]
        if len(addList) == 2:
            area = addList[1]
        mainInfo = rowOfferTag.find('div', {'class': 'col-xs-6 left'})
        dealerName = mainInfo.find('h6', {'class': 'title-4s'}).find('a', {'target': '_blank'}).get('title')
        dealerName = dealerName.split(' ')[0]
        address = mainInfo.find('p', {'class': 'add'}).find('span', {'class': 's-title'}).next_sibling.get('title')
        phoneTag = mainInfo.find('p', {'class': 'tel'}).find('span', {'class': 'phone-sty'})
        # print(priceUrl)
        website, teles, fullName = self.getDealerWebsiteTelesFullname(priceUrl)
        sale_phone_number = YiChe.getSalePhoneNumberByDealerId(dealerId)
        if sale_phone_number is None:
            sale_phone_number = teles
        dealer = CarDealer(id=dealerId, province=province, city=city, area=area, name=dealerName, full_name=fullName,
                           type=type, address=address,
                           official_website=website, sale_phone_number=sale_phone_number,
                           contact_number=teles)
        return dealer

    def getCarPriceAndDealerListFromBaoJiaByProvince(self, carId, province, provinceUrl, carPriceList, dealerList):
        # bizmode为经销商类型：0:综合店，1:4S店，2:特许店
        bizmodeList = [0, 1, 2]
        for bizmode in bizmodeList:
            url = provinceUrl + '?bizmode=%s#V' % bizmode
            content = YiChe.getNativityContent(url, {})
            if content is None:
                continue
            soup = BeautifulSoup(content, MARKUP_TYPE)
            if soup.find('div', {'class':'note-box txt'}) is not None:
                # 当前省份没有对应类型的销售店
                continue
            offerListBox = soup.find('div', {'class':'offer-list-box'})
            if offerListBox is None or offerListBox.find('div', {'class':'note-box note-empty type-2'}):
                # 当前省份没有对应类型的销售店
                continue
            offerLists = offerListBox.findAll('div', {'class':'row offer-list'})
            for rowOffer in offerLists:
                carPrice = self.parseCarPriceFromBaoJia(rowOffer, carId)
                # print(carPrice.__dict__)
                if self.redisManager.isCarDealerPriceExisted(carPrice) is False:
                    carPriceList.append(carPrice)
                    self.redisManager.addCarDealerPrice(carPrice)
                dealerId = carPrice.dealer_id
                if self.redisManager.isDealerIdExisted(dealerId) is False:
                    dealer = self.parseCarDealerFromBaoJia(rowOffer, dealerId=dealerId,
                                  province=province, type=bizmode, priceUrl=carPrice.price_url)
                    dealerList.append(dealer)
                    self.redisManager.addDealerId(dealerId)

    def getPublishAndEndDateFromPromotePage(self, promoteUrl):
        content = YiChe.getNativityContent(promoteUrl, {})
        if content is None:
            return (Utility.getCurrentDate(format('%Y/%m/%d')), None)
        soup = BeautifulSoup(content, MARKUP_TYPE)
        saleTimeTag = soup.find('div', {'class':'saletime'})
        if saleTimeTag is None:
            # self.log.warning('url[%s] is not promote url' % promoteUrl)
            return (None, None)
        results = re.search('.*?(\d+)年(\d+)月(\d+)日 - (\d+)年(\d+)月(\d+)日', saleTimeTag.get_text())
        by, bm, bd, ey, em, ed = results.groups()
        publishDate = '%s/%s/%s' % (by, bm, bd)
        endDate = '%s/%s/%s' % (ey, em, ed)
        return (publishDate, endDate)

    def saveOneSerieCarPrice(self, versionList):
        dealerListDataBaseUrl = 'http://frontapi.easypass.cn/CsReviewPageApi/CarPriceList//GetCarDealerPriceList/%s/0/5000/1/-1/-1?callback=jsonpDealerListdata'
        '''一个系列下的所有车款'''
        for carId, version, url, isStopSelling in versionList:
            '''一款车，全国所有经销商的报价'''
            # 如果今天已经收集了carId的报价，则今天不用再次收集
            if self.redisManager.isCarPriceHadCollectedToday(carId) is True:
                # self.log.info('carId[%s] has collected today' % carId)
                continue
            if isStopSelling is False:
                requestUrl = dealerListDataBaseUrl % carId
                content = YiChe.getNativityContent(requestUrl)
                carPriceList = []
                dealerList = []
                # self.log.info(('开始收集报价', 'CarId[%s]' % carId, 'CarDetailUrl[%s]' % url ))
                beginTime = Utility.getCurrentTimestamps()
                result = self.getCarPriceAndDealerList(content, carPriceList, dealerList)
                costTime = Utility.getCurrentTimestamps() - beginTime
                # self.log.info(('结束收集报价', 'CarId[%s]' % carId, '今天共有[%s]家经销商给出报价' % len(carPriceList), '花费时间[%s]秒' % costTime))
                if result is None:
                    # self.log.warning(('carId[%s] state is onselling, but can not find any dealer or price' % carId, 'data[%s]' % content, url))
                    url = url + '/baojia/c0'
                    # self.log.info(('开始尝试', '从 url[%s] 收集报价' % url))
                    beginTime = Utility.getCurrentTimestamps()
                    self.getCarPriceAndDealerListFromBaoJia(carId=carId, url=url, carPriceList=carPriceList, dealerList=dealerList)
                    costTime = Utility.getCurrentTimestamps() - beginTime
                    # self.log.info(('结束尝试', '共有[%s]家经销商给出报价' % len(carPriceList), '花费时间[%s]秒' % costTime))
                else:
                    '''切记：由于外键的表级约束，必须先更新Dealer，再更新CarPrice'''
                    if len(dealerList) != 0:
                        self.dbManager.insertDealerListIntoDB(dealerList)
                    if len(carPriceList) != 0:
                        self.dbManager.insertCarPriceListIntoDB(carPriceList, self.redisManager)
                # 今天完成carId的报价收集
                self.redisManager.addCarPriceHadCollectedToday(carId)

    def startCollectData(self):
        self.log.info(('汽车品牌的Url', self.brandCarInfoUrlMap))
        '''所有品牌'''
        for brand, brandUrl in self.brandCarInfoUrlMap.items():
            '''一个品牌的所有子品牌'''
            subBrandSeriesMap = YiChe.getOneBrandSubbrandSeries(brand, brandUrl)
            for subBrand, seriesMap in subBrandSeriesMap.items():
                '''一个子品牌的所有系列'''
                for serie, url in seriesMap.items():
                    '''一个系列的所有车款'''
                    # print('+++', serie, '-', url)
                    '''车款列表versionList的每个元素为：(carId, version, url, isStopSelling)'''
                    versionList = self.getOneSeriesAllVersionList(url)
                    # print(versionList)
                    self.updateCacheAndDB(versionList)
                    self.saveOneSerieCarDetails(brand, subBrand, serie, versionList)
                    self.saveOneSerieCarPrice(versionList)
                    # print('---', serie, '-', url)

    @staticmethod
    def generateBrandUrlMapList():
        brandCarInfoUrlMap = YiChe.getAllBrandCarInfoUrl()
        mapList = []
        eachMapLen = int(len(brandCarInfoUrlMap) / THREAD_NUM)
        tmpMap = {}
        count = 0
        for brand, brandUrl in brandCarInfoUrlMap.items():
            count += 1
            tmpMap[brand] = brandUrl
            if count > eachMapLen:
                mapList.append(tmpMap)
                count = 0
                tmpMap = {}
        if len(tmpMap) != 0:
            mapList.append(tmpMap)
        return mapList


def init():
    redisManager = CacheManager()
    dbManager = DBManager(log=None)
    if redisManager.redis.exists('yiche-info-carid') is False:
        carIds = dbManager.getAllCarIdFromCarBaseInfo()
        redisManager.redis.sadd('yiche-info-carid', carIds)
    if redisManager.redis.exists('yiche-dealerid') is False:
        dealerIds = dbManager.getAllDealerIdFromCarDealer()
        redisManager.redis.sadd('yiche-dealerid', dealerIds)
    if redisManager.redis.exists('yiche-stopselling-carid') is False:
        carIds = dbManager.getAllStopSellingCarId()
        redisManager.redis.sadd('yiche-stopselling-carid', carIds)
    if redisManager.redis.exists('yiche-onselling-carid') is False:
        carIds = dbManager.getAllOnSellingCarId()
        redisManager.redis.sadd('yiche-onselling-carid', carIds)


def start(brandCarInfoUrlMap, i):
    log = Logger.getLogger(logFileName='yiche-thread[%s].log' % i, loggerName='yiche-thread[%s]' % i)
    RedisManager = CacheManager()
    MySQLManager = DBManager(log=log)
    yiche = YiChe(redisManager=RedisManager, dbManager=MySQLManager, log=log, brandCarInfoUrlMap=brandCarInfoUrlMap)
    yiche.startCollectData()


if __name__ == '__main__':
    init()
    while True:
        if True:
            brandCarInfoUrlMapList = YiChe.generateBrandUrlMapList()
            pool = Pool(THREAD_NUM)
            for i in range(0, THREAD_NUM):
                brandUrlMap = brandCarInfoUrlMapList[i]
                pool.apply_async(start, args=(brandUrlMap, i))
            pool.close()
            pool.join()
        # 收集完数据，处理一下当天的报价数据
        if True:
            dbManager = DBManager(log=None)
            dbManager.dealCarPrice()
        print('轮询一遍之后，休息30分钟......')
