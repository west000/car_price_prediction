#!/usr/bin/env python
# import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - [%(message)s]')
from bs4 import BeautifulSoup
import requests, time, random, re, datetime, os
import redis, pymysql
from config import configs
from multiprocessing import Pool
from logger import Logger

MARKUP_TYPE = configs.markup_type
MAX_RETRY_TIMES = configs.max_retry_times
PROCESS_NUM = configs.renrenche.process_num
ID_LEN = 1000

class Car:
    def __init__(self):
        self.brand = ''             # 品牌
        self.unique_id = ''         # 车子ID
        self.version = ''           # 车型
        self.first_licence = ''     # 首次上牌日期
        self.separator = 0          # 里程数
        self.new_price = 0          # 新车价格
        self.current_price = 0      # 当前二手车价格
        self.source = 0             # 车源，0代表个人，1代表车商
        self.transfer_times = 0     # 过户次数
        self.area = ''              # 所属地区
        self.color = ''             # 车身颜色
        self.add_date = ''          # 发布日期/上架日期
        self.fix_record = ''        # 维修记录
        self.url = ''               # 源信息url

    def getCarInfo(self):
        return self.__dict__

    def showCar(self):
        print(self.__dict__)

    def toTuple(self):
        '''car(brand, unique_id, version, first_licence, mailage, new_price, current_price, source, area, color, transfer_times, add_date, fix_record, url)'''
        return (self.brand, self.unique_id, self.version, self.first_licence, self.separator, self.new_price,self.current_price,
                self.source, self.area, self.color, self.transfer_times, self.add_date, self.fix_record, self.url)

class Utility:
    @staticmethod
    def getFloatFromStr(str):
        results = re.findall(r'\d+\.?\d*', str)
        return float(results[0]) if len(results) != 0 else 0.0

    @staticmethod
    def getContent(url, headers=None):
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        content = None
        tryTimes = 0
        while content is None and tryTimes < MAX_RETRY_TIMES :
            tryTimes += 1
            try:
                content = requests.get(url, headers=headers).content
            except Exception as e:  # MaxRetryError
                print(e)
                print('tryTimes:', tryTimes)
                content = None
                t = random.randint(60, 150)
                time.sleep(t)
            else:
                break
        if content is None:
            print('[Warnning:%s]' % time.asctime(time.localtime(time.time())), url, 'try too much times, quit!!')
            quit()
        return content

    @staticmethod
    def getCurrentDate(format='%Y/%m/%d'):
        return time.strftime(format, time.localtime(time.time()))

    @staticmethod
    def generateRandomDate(beginDate, endDate):
        beginDate = datetime.datetime.strptime(beginDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
        days = (endDate - beginDate).days
        day = random.randint(random.randint(1, int(days/2)+1), days)
        result = beginDate + datetime.timedelta(days=day)
        result = result.strftime('%Y-%m-%d')
        return result

    @staticmethod
    def splitList(originList, n):
        listLen = len(originList)
        eachLen = int(listLen / n)
        resultList = []
        for i in range(n):
            if i == n - 1:
                resultList.append(originList[i * eachLen:])
            else:
                resultList.append(originList[i * eachLen:(i + 1) * eachLen])
        return resultList

class DBManager:
    def __init__(self):
        self.connection = pymysql.connect(host='192.168.56.102', port=3306, user='root', password='123',
                                      db='graduation_project', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    def __del__(self):
        self.connection.close()

    def getUrlList(self, beginId):
        cursor = self.connection.cursor()
        urls = None
        try:
            sql = 'SELECT url FROM car WHERE id>=%s AND id<%s'
            cursor.execute(sql, (beginId, beginId + ID_LEN))
            result = cursor.fetchall()
            urls = [item['url'] for item in result]
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return urls

    def getMaxId(self):
        cursor = self.connection.cursor()
        maxId = None
        try:
            sql = 'SELECT max(id) FROM car'
            cursor.execute(sql)
            maxId = cursor.fetchone()['max(id)']
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return maxId

    def getAllCarIdFromCar(self):
        cursor = self.connection.cursor()
        carIds = None
        try:
            sql = 'SELECT unique_id FROM car'
            cursor.execute(sql)
            result = cursor.fetchall()
            carIds = [item['unique_id'] for item in result]
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return carIds

    def insertCarListIntoDB(self, carList):
        for car in carList:
            self.insertCarIntoDB(car)

    def insertCarIntoDB(self, car):
        cursor = self.connection.cursor()
        try:
            sql = 'INSERT INTO car(brand, unique_id, version, first_licence, mailage, new_price, current_price, source, area, color, transfer_times, add_date, fix_record, url) ' \
                  'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, car.toTuple())
            self.connection.commit()
        except Exception as e:
            message = str(e)
            if re.search('.*?Duplicate entry.*?', message) is not None:
                pass
                # print('Duplicate key in TABLE car, unique_id[%s] has existed' % car.unique_id)
            else:
                raise e
        finally:
            cursor.close()

    def updateSaleDate(self, url, date):
        unique_id = url.split('/')[-1]
        self.updateSaleDateByCarId(unique_id, date)

    def updateSaleDateByCarId(self, carId, date):
        cursor = self.connection.cursor()
        try:
            sql = r"UPDATE car SET sale_date=%s WHERE unique_id=%s"
            cursor.execute(sql, (date, carId))
            self.connection.commit()
        finally:
            cursor.close()

    def getNotSaleCarUrlAndDate(self):
        cursor = self.connection.cursor()
        rows = None
        try:
            sql = 'SELECT url, add_date FROM car WHERE sale_date is NULL'
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            print(e.message)
        finally:
            cursor.close()
        return rows

    def getAllNotSaleCarId(self):
        cursor = self.connection.cursor()
        rows = None
        try:
            sql = 'SELECT unique_id, add_date FROM car WHERE sale_date is NULL'
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            print(e.message)
        finally:
            cursor.close()
        return rows

class CacheManager:
    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.56.102', port=6379)
        self.redis = redis.Redis(connection_pool=pool)

    def isCarIdExisted(self, carId):
        return self.redis.sismember('rrc-id', carId)

    def addCarId(self, carId):
        self.redis.sadd('rrc-id', carId)

    # 本次轮询到的所有carId，轮询之后，删除'rrc-current-polling'
    def addCarIdCurrentPolling(self, carId):
        self.redis.sadd('rrc-current-polling', carId)

    # 本次轮询的carId是否存在
    def isCurrentPollingCarIdExisted(self, carId):
        return self.redis.sismember('rrc-current-polling', carId)

    def deleteCarIdFromCurrentPollingSet(self, carId):
        self.redis.srem('rrc-current-polling', carId)

    def deleteCurrentPollingSet(self):
        return  self.redis.delete('rrc-current-polling')

    def isCityFinished(self, city):
        return self.redis.sismember('finished-city', city)

    def addFinishedCity(self, city):
        self.redis.sadd('finished-city', city)

    def addCityBrandFinishedToday(self, city, brand):
        today = Utility.getCurrentDate()
        setName = today + '-city-brand-finished'
        key = city + '-' + brand
        self.redis.sadd(setName, key)

    def isCityBrandFinishedToday(self, city, brand):
        today = Utility.getCurrentDate()
        setName = today + '-city-brand-finished'
        key = city + '-' + brand
        return self.redis.sismember(setName, key)

    def addHaveNotSaleCarUrl(self, url, add_date):
        key = url.split('/')[-1]
        self.redis.hset('rrc-notsalecar', key=key, value=add_date)

    def isCarNotSaledExisted(self, url):
        key = url.split('/')[-1]
        return self.redis.hget('rrc-notsalecar', key=key) is not None

    def delSaleCarUrl(self, url):
        key = url.split('/')[-1]
        self.redis.hdel('rrc-notsalecar', key=key)

    def isCarIdHTMLSaved(self, carId):
        return self.redis.sismember('save-rrc-carId', carId)

    def saveCarIdHTML(self, carId):
        self.redis.sadd('save-rrc-carId', carId)


class RenRenChe(object):
    baseURL = configs.renrenche.base_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host':'www.renrenche.com'
    }
    searchCondition = '/ershouche/?sort=publish_time&seq=desc'

    def __init__(self, redisManager, dbManager, log, areaMap):
        self.redisManager = redisManager
        self.dbManager = dbManager
        self.log = log
        self.areaMap = areaMap

    @staticmethod
    def getBS4PageInstance(url):
        content = Utility.getContent(url, headers=RenRenChe.headers)
        return BeautifulSoup(content, MARKUP_TYPE)

    @staticmethod
    def getCityCodeAndNameMap():
        page = RenRenChe.getBS4PageInstance(RenRenChe.baseURL)
        main = page.find('div', {'class': 'area-city-letter'})
        areaMap = {}
        for area in main.find_all('a'):
            city = area['href'].replace('/', '')
            areaMap[city] = area.get_text()
        return areaMap

    @staticmethod
    def getBrandMapByCity(city):
        url = RenRenChe.baseURL + city + '/ershouche'
        page = RenRenChe.getBS4PageInstance(url)
        main = page.find('div', {'class': 'brand-more-content'})
        brandMap = {}
        for brandLine in main.find_all('span', {'class': 'bn'}):
            for brand in brandLine.find_all('a'):
                code = brand['href'].split('/')[2]
                name = brand.get_text()
                brandMap[code] = name
        return brandMap

    @staticmethod
    def getCarInfoFromDetailsPage(url, car):
        page = RenRenChe.getBS4PageInstance(url)
        cardTable = page.find('div', {'class': 'card-table'})
        if cardTable is None:
            return None
        cardTable = cardTable.table
        if cardTable is None:
            print('card-table not find', car.url)
            return None
        car.color = cardTable.find('td', text='车身颜色').next_sibling.next_sibling.get_text()
        car.first_licence = cardTable.find('td', text='上牌日期').next_sibling.next_sibling.get_text()
        car.area = cardTable.find('td', text='归属地').next_sibling.next_sibling.get_text()
        car.transfer_times = int(
            cardTable.find('td', text='过户次数').next_sibling.next_sibling.get_text().replace('次', ''))
        add_date = cardTable.parent.previous_sibling.previous_sibling.find(text=re.compile('检测时间：[0-9\-]*'))
        add_date = add_date.split('：', 1)[1]
        car.add_date = add_date[0:10]

        detailLists = page.find('div', {'class': 'middle-content'})
        if detailLists is not None:
            try:
                car.new_price = int(Utility.getFloatFromStr(
                    detailLists.find('div', {'class': 'new-car-price detail-title-right-tagP'}).find(
                        'span').get_text()) * 10000)
                car.current_price = int(Utility.getFloatFromStr(
                    detailLists.find('p', {'class': 'price detail-title-right-tagP'}).get_text()) * 10000)
            except Exception as e:
                print('Error:', url)
                return None
        else:
            detailLists = page.find('div', {'class': 'detail-box'})
            if detailLists is not None:
                try:
                    priceWithTax = detailLists.find('li', text=re.compile('新车*')).get_text().split('+')
                    new_price = int(Utility.getFloatFromStr(priceWithTax[0]) * 10000)
                    tax = int(Utility.getFloatFromStr(priceWithTax[1]) * 10000)
                    car.new_price = new_price + tax
                    car.current_price = int(
                        Utility.getFloatFromStr(detailLists.find('p', {'class': 'box-price'}).get_text()) * 10000)
                except Exception as e:
                    print('Error:', url)
                    return None
            else:
                print('detail-box not find', car.url)
                return None

        fixRecord = page.find('div', {'class': 'img-position bottom'}).findAll('div', {'class': 'defect-text'})
        fixRecordInfo = [dt.get_text() for dt in fixRecord]
        fixRecord = page.find('div', {'class': 'img-position inside'}).findAll('div', {'class': 'defect-text'})
        fixRecordInfo += [dt.get_text() for dt in fixRecord]
        car.fix_record = '|'.join(fixRecordInfo)
        return car

    def getCarListItemsFromOverviewPage(self, page, city, cityCarCount):
        # 注意：通常页面中，row-fluid list-row js-car-list只有一个
        #       但是，如果出现“ 附近城市车辆”推荐，则有两个，第一个为搜索城市的汽车列表，第二个为附近城市的列表
        carListULTag = page.findAll('ul', {'class': 'row-fluid list-row js-car-list'})
        count = cityCarCount
        carList = []
        carListUL = carListULTag[0].findAll('li', {'class': 'span6 list-item car-item '})
        if len(carListUL) == 0:
            carListUL = carListULTag[0].findAll('li', {'class': 'span6 list-item car-item'})
        for carItems in carListUL:
            for carInfo in carItems.find_all('a'):
                # print(carInfo)
                carId = carInfo.get('data-car-id')
                self.redisManager.addCarIdCurrentPolling(carId)
                if carId is None or self.redisManager.isCarIdExisted(carId):
                    continue
                car = Car()
                car.unique_id = carId
                car.url = RenRenChe.baseURL + carInfo['href']
                title = carInfo['title'].split('-', 1)
                car.brand = title[0]
                car.version = carInfo['title']
                basic = carInfo.find('span', {'class': 'basic'}).get_text()
                basic = basic.split('/')
                car.first_licence = basic[0]
                car.separator = int(float(basic[1].replace('万公里', '')) * 10000)
                carDetailUrl = RenRenChe.baseURL + carInfo['href']
                if RenRenChe.getCarInfoFromDetailsPage(carDetailUrl, car) is None:
                    print('[Warnning:%s]' % time.asctime(time.localtime(time.time())), 'quit', carDetailUrl, '第', count+1, '辆车')
                    self.redisManager.deleteCarIdFromCurrentPollingSet(carId)
                    continue
                self.redisManager.addCarId(carId)
                carList.append(car)
                count = count + 1
                # print('第', count, '辆车', car.url)
                # print('第', count, '辆车：', car.getCarInfo())
        self.dbManager.insertCarListIntoDB(carList)
        return count

    @staticmethod
    def isThisCityWithBrandFinished(page):
        return len(page.findAll('ul', {'class': 'row-fluid list-row js-car-list'})) > 1

    @staticmethod
    def getNextOverviewPageUrl(page):
        # 注意：如果出现“抱歉，暂时没有符合条件的车”，则没有pagination js-pagination
        pageList = page.find('ul', {'class': 'pagination js-pagination'})
        if pageList is None:
            return None
        else:
            pageList = pageList.children
        pageList = [li for li in pageList]
        nextPage = pageList[-2]
        liClass = nextPage.get('class')
        if liClass is not None and liClass[0] == 'disabled':
            return None
        else:
            nextUrl = nextPage.find('a').get('href')
            # print(nextUrl)
            return nextUrl

    @staticmethod
    def generateAreaMapList():
        areaMap = RenRenChe.getCityCodeAndNameMap()
        areaMapList = []
        eachMapLen = int(len(areaMap) / PROCESS_NUM)
        tmpMap = {}
        count = 0
        for areaCode, areaName in areaMap.items():
            # print(areaCode, '-', areaName)
            count += 1
            tmpMap[areaCode] = areaName
            if count > eachMapLen:
                areaMapList.append(tmpMap)
                count = 0
                tmpMap = {}
        if len(tmpMap) != 0:
            areaMapList.append(tmpMap)
        return areaMapList

    @staticmethod
    def generateNotSaleUrlDateList():
        DB = DBManager()
        urlDateList = DB.getNotSaleCarUrlAndDate()
        listLen = len(urlDateList)
        eachLen = int(listLen / PROCESS_NUM)
        resultList = []
        for i in range(PROCESS_NUM):
            if i == PROCESS_NUM-1:
                resultList.append(urlDateList[i * eachLen:])
            else:
                resultList.append(urlDateList[i * eachLen:(i + 1) * eachLen])
        return resultList

    def startCollectData(self):
        cityCostTimeDict = {}
        for areaCode, areaName in self.areaMap.items():
            self.log.info(('城市', areaName, '开始'))
            # if RedisManager.isCityFinished(areaCode):
            #     print('城市', areaName, '之前已经完成数据采集')
            #     continue
            oneCityTotalCostTime, oneCityTotalCarCount = 0, 0
            brandMap = RenRenChe.getBrandMapByCity(areaCode)
            for brandCode, brandName in brandMap.items():
                if self.redisManager.isCityBrandFinishedToday(city=areaName, brand=brandName) is True:
                    continue
                # print('地区及品牌', areaName, '-', brandName)
                self.log.debug(('地区及品牌', areaName, brandName))
                url = RenRenChe.baseURL + areaCode + '/' + brandCode + RenRenChe.searchCondition
                pageCount, costTime, oneBrandCarCount = 1, 0, 0
                while True:
                    onePageCarCount = oneBrandCarCount
                    beginTime = time.time()
                    self.log.debug(('+++第', pageCount, '页', '开始', 'url:', url))
                    page = RenRenChe.getBS4PageInstance(url)
                    oneBrandCarCount = self.getCarListItemsFromOverviewPage(page, areaCode, oneBrandCarCount)
                    onePageCarCount = oneBrandCarCount - onePageCarCount
                    endTime = time.time()
                    timeInterval = endTime - beginTime
                    costTime += timeInterval
                    self.log.debug(('---第', pageCount, '页', '结束', '耗时:', timeInterval, '秒', '共有', onePageCarCount, '辆车'))
                    if RenRenChe.isThisCityWithBrandFinished(page):
                        break
                    nextUrl = RenRenChe.getNextOverviewPageUrl(page)
                    if nextUrl is None:
                        break
                    url = RenRenChe.baseURL + nextUrl
                    pageCount += 1
                oneCityTotalCostTime += costTime
                oneCityTotalCarCount += oneBrandCarCount
                self.redisManager.addCityBrandFinishedToday(city=areaName, brand=brandName)
                # print('地区及品牌', areaName, '-', brandName, '[', '车辆数:', oneBrandCarCount, '耗时:', costTime, '秒', ']')
                self.log.info(('地区及品牌', areaName, brandName, '车辆数:', oneBrandCarCount, '耗时:', costTime, '秒'))
            # print('城市', areaName, '共有', oneCityTotalCarCount, '辆二手车,', '总共耗时', oneCityTotalCostTime, '秒')
            self.log.info(('城市', areaName, '共有', oneCityTotalCarCount, '辆二手车,', '总共耗时', oneCityTotalCostTime, '秒'))
            cityCostTimeDict[areaName] = (oneCityTotalCostTime, oneCityTotalCarCount)
            self.redisManager.addFinishedCity(areaCode)
        self.log.info(cityCostTimeDict)
        totalTime = 0
        totalCount = 0
        for city, (times, count) in cityCostTimeDict.items():
            totalTime += times
            totalCount += count
            self.log.info('城市[%s] 本次共花费[%s]秒 收集到[%s]辆二手车信息' % (city, times, count))
        self.log.info('本次总时间[%s] 总车辆数[%s]' % (totalTime, totalCount))

    def updateSaleDate(self, urlDateList):
        self.log.info(len(urlDateList))
        counter = 0
        for urlDate in urlDateList:
            url = urlDate['url']
            addDate = urlDate['add_date']
            # 某次完整的遍历被中断，为了性能将遍历过的url存到redis中，全部遍历完即可删除
            if self.redisManager.isCarNotSaledExisted(url=url) is True:
                continue
            else:
                self.redisManager.addHaveNotSaleCarUrl(url=url, add_date=addDate)

            res = requests.get(url, RenRenChe.headers)
            content = None
            if res.status_code == requests.codes.ok:
                content = res.content
            else:
                print('requests error')
                continue
            soup = BeautifulSoup(content, MARKUP_TYPE)
            mainPage = soup.find('div', {'class':'recommend-img-container'})
            if mainPage is None:
                self.log.warning((url, addDate, 'can not find <recommend-img-container>'))
                quit()
            else:
                if mainPage.find('div', {'class':'sold-out-tips'}, text='已下架') is not None:
                    counter += 1
                    addDate = addDate.strftime('%Y-%m-%d')
                    saleDate = Utility.generateRandomDate(beginDate=addDate, endDate=Utility.getCurrentDate('%Y-%m-%d'))
                    self.dbManager.updateSaleDate(url=url, date=saleDate)
                    self.log.info(url)
                    if counter != 0 and counter % 100 == 0:
                        self.log.info('have sale [%d] cars' % counter)
        self.log.info('total sale [%d] cars' % counter)

    @staticmethod
    def saveHTMLToFile(url, carId, index=1):
        session = requests.Session()
        res = session.get(url=url)
        if res.status_code == requests.codes.ok:
            content = requests.get(url, headers=RenRenChe.headers).content
            path = './html/renrenche%s/%s.html' % (index, carId)
            with open(path, 'wb') as f:
                f.write(content)
            return True
        return False


def init():
    redisManager = CacheManager()
    dbManager = DBManager()

    if redisManager.redis.exists('rrc-id') is False:
        carIds = dbManager.getAllCarIdFromCar()
        redisManager.redis.sadd('rrc-id', carIds)

def start(areaMap, i):
    MySQLManager = DBManager()
    RedisManager = CacheManager()
    log = Logger.getLogger(logFileName='rrc-process[%s].log' % i, loggerName='rrc-process[%s]' % i)
    rrc = RenRenChe(redisManager=RedisManager, dbManager=MySQLManager, log=log, areaMap=areaMap)
    rrc.startCollectData()

def updateSaleDate(urlDateList, i):
    MySQLManager = DBManager()
    RedisManager = CacheManager()
    log = Logger.getLogger(logFileName='rrc-update-process[%s].log' % i, loggerName='rrc-update-process[%s]' % i)
    rrc = RenRenChe(redisManager=RedisManager, dbManager=MySQLManager, log=log, areaMap={})
    rrc.updateSaleDate(urlDateList)

def saveHTML(urls, threadId, pathIndex):
    redisManager = CacheManager()
    for url in urls:
        carId = url.split('/')[-1]
        if redisManager.isCarIdHTMLSaved(carId) is False:
            if RenRenChe.saveHTMLToFile(url, carId, index=pathIndex) is True:
                redisManager.saveCarIdHTML(carId)
                print('[%s]-[%s]-[%s]'% (threadId, carId, url))

if __name__ == '__main__':
    # 平时的爬取任务
    if True:
        init()
        while True:
            dbManager = DBManager()
            notSaleCarId = dbManager.getAllNotSaleCarId()
            # for carId in open('tmp.txt'):
            #     carId = carId.replace('\n', '')
            #     dbManager.updateSaleDateByCarId(carId, date=None)
            # quit()
            # 抓新的二手车数据
            if True:
                areaMapList = RenRenChe.generateAreaMapList()
                pool = Pool(PROCESS_NUM)
                for i in range(0, PROCESS_NUM):
                    areaMap = areaMapList[i]
                    pool.apply_async(start, args=(areaMap, i))
                pool.close()
                pool.join()

            # 更新售出二手车的出售日期
            if True:
                redisManager = CacheManager()
                currentDate = Utility.getCurrentDate()
                print(len(notSaleCarId))
                connter = 0
                for kv in notSaleCarId:
                    carId = kv['unique_id']
                    add_date = kv['add_date']
                    if redisManager.isCurrentPollingCarIdExisted(carId) is False:
                        print(carId)
                        connter += 1
                        dbManager.updateSaleDateByCarId(carId, currentDate)
                print(connter)
                redisManager.deleteCurrentPollingSet()

            print('轮询一遍之后，休息30分钟......')
            time.sleep(1800)

    # 保存HTML任务
    if False:
        dbManager = DBManager()
        maxId = dbManager.getMaxId()
        print('maxId:', maxId)
        beginId = 152000
        while beginId < maxId:
            pathIndex = int(beginId/10000) + 1
            dir = './html/renrenche%s/' % pathIndex
            if os.path.exists(dir) is False:
                os.makedirs(dir)

            beginTime = time.time()
            urlList = dbManager.getUrlList(beginId=beginId)
            beginId += ID_LEN
            if urlList is None or len(urlList) == 0:
                continue
            urlsList = Utility.splitList(urlList, PROCESS_NUM)
            pool = Pool(PROCESS_NUM)
            for i in range(0, PROCESS_NUM):
                urls = urlsList[i]
                pool.apply_async(saveHTML, args=(urls, i, pathIndex))
            pool.close()
            pool.join()
            endTime = time.time()
            print('id[{} ~ {}) cost {:.2f}s'.format(beginId-ID_LEN, beginId,endTime - beginTime))


    # while True:
    #     urlDate = RenRenChe.generateNotSaleUrlDateList()
    #     # updateSaleDate(urlDate[0], 0)
    #     # quit()
    #     pool = Pool(PROCESS_NUM)
    #     for i in range(0, PROCESS_NUM):
    #         urlDateList = urlDate[i]
    #         pool.apply_async(updateSaleDate, args=(urlDateList, i))
    #     pool.close()
    #     pool.join()
    #     print('轮询一遍之后，休息30分钟......')
    #     time.sleep(1800)
    #     quit()
    #     redisMananger = CacheManager()
    #     redisMananger.redis.delete('rrc-notsalecar')

