#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'West'

import pymysql, redis, re
from bs4 import BeautifulSoup
from logger import Logger
from utility import Utility
from config import configs

MARKUP_TYPE = configs.markup_type

class CarPolicy:
    def __init__(self, id, title, release_date, release_department, url, policy_type, begin_date=None, content=None, end_date=None):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.release_department = release_department
        self.begin_date = begin_date
        self.end_date = end_date
        self.content = content
        self.url = url
        self.type = policy_type

    def toTuple(self):
        return (self.id, self.title, self.release_date, self.release_department,
                self.begin_date, self.end_date, self.url, self.type, self.content)


class CacheManager:
    def __init__(self):
        pool = redis.ConnectionPool(host=configs.redis.host, port=configs.redis.port)
        self.redis = redis.Redis(connection_pool=pool)

    def addPolicyId(self, policyId):
        self.redis.sadd('carpolicy', policyId)

    def isPolicyIdExisted(self, policyId):
        return self.redis.sismember('carpolicy', policyId)

class DBManager:
    def __init__(self):
        self.connection = pymysql.connect(host=configs.db.host, port=configs.db.port, user=configs.db.user, password=configs.db.password,
                                      db=configs.db.db, charset=configs.db.charset, cursorclass=pymysql.cursors.DictCursor)
    def __del__(self):
        self.connection.close()

    def insertPolicyListIntoDB(self, policyList):
        cursor = self.connection.cursor()
        try:
            sql = r'INSERT INTO car_policy(id, title, release_date, release_department, begin_date, end_date, url, type, content) ' \
                  'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(sql, [policy.toTuple() for policy in policyList])
            self.connection.commit()
        finally:
            cursor.close()

class CarPolicyCrawler:
    earliestDate = configs.carpolicy.earliest_date
    baseUrl = configs.carpolicy.base_url
    nationalPolicyUrl = configs.carpolicy.national_policy_url
    localPolicyUrl = configs.carpolicy.local_policy_url
    policyUrlMap = {
        'national_policy': nationalPolicyUrl,
        'local_policy': localPolicyUrl,
    }

    includeKeyword = ('排量', '排气量', '报废', '新能源', '二手车', '迁入', '迁出', '补贴',
                      '农村', '下乡', '优惠','减免','限行', '限排', '限外', '限牌', '电动汽车',
                      '电动车', '智能网联汽车', '进口车', '进口汽车', '排气污染',
                      '对原产于美国的部分进口商品加征关税', '购置税', '减征', '交强险', '车船税', '补助',
                      '轿车', '越野车', '小汽车', '黄标车', '旧车', '蓄电池', '电池', '电动汽车', '充电', '节能汽车', '自驾车', '旅居车', )

    excludeKeyword = ('出租车', '客车', '摩托', '客运', '农机', '进口货物', '成品油', '智能制造', '人工智能',
                      '二手车交易信息采集工作', '天然气', '名单', '电器',
                      '服务车', '农用', '收割机', '手扶拖拉机', '煤油', '航空', '军用', '自行车', '偷漏税',
                      '专用汽车', '三轮', '拆解', '助力车', '警车', '农用车', '货运车',
                      '交通安全', )

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
            tmp.update(CarPolicyCrawler.headers)
            content = Utility.getNativityContent(url, headers=tmp, defaultRequest=defaultRequest)
        return str(content, encoding='gb2312', errors='ignore')


    def __init__(self, redisManager, dbManager, log):
        self.redisManager = redisManager
        self.dbManager = dbManager
        self.log = log

    @staticmethod
    def getNextPageUrl(pageTag):
        nextPageUrl = None
        nextPageUrlTag = pageTag.find('a', text='下一页')
        if nextPageUrlTag is not None:
            nextPageUrl = CarPolicyCrawler.baseUrl + nextPageUrlTag.get('href')
        return nextPageUrl

    @staticmethod
    def keywordsToStr(keywords):
        result = '%s|'*len(keywords)
        result = result[:-1]
        result = result % keywords
        return result

    @staticmethod
    def isTitleProper(title):
        isProper = False
        if re.search(CarPolicyCrawler.keywordsToStr(CarPolicyCrawler.includeKeyword), title) is not None:
            isProper = True
        if re.search(CarPolicyCrawler.keywordsToStr(CarPolicyCrawler.excludeKeyword), title) is not None:
            isProper = False
        return isProper

    @staticmethod
    def getPolicyContent(url, policy):
        print(url)
        content = CarPolicyCrawler.getNativityContent(url, headers={})
        soup = BeautifulSoup(content, MARKUP_TYPE)
        newstextTag = soup.find('div', {'class':'newstext'})
        liTag = newstextTag.find('ol').findAll('li')
        endDate = liTag[1].get_text().replace('【时效性】', '').strip()
        endDate = endDate.replace('至', '').replace('止', '')
        beginDate = liTag[2].get_text().replace('【实施日期】', '').strip()
        if beginDate == '':
            beginDate = None
        else:
            if re.search('年', beginDate) is not None:
                beginDate = Utility.dateFormatConvert(dateStr=beginDate, originFormat='%Y年%m月%d日')
            elif re.search('-', beginDate) is not None:
                pass
            else:
                beginDate = Utility.dateFormatConvert(dateStr=beginDate, originFormat='%m/%d/%Y')
        policyContentTag = newstextTag.findAll('p')
        policyContent = ''
        for tag in policyContentTag:
            if policyContentTag is None:
                continue
            policyContent = tag.get_text()
        policy.begin_date = beginDate
        policy.end_date = endDate
        policy.content = policyContent
        return policy


    def startCollectData(self):
        for pt, url in CarPolicyCrawler.policyUrlMap.items():
            print('-'*100)
            policyType = 1 if pt == 'national_policy' else 2
            isContinue = True
            while url is not None and isContinue is True:
                content = CarPolicyCrawler.getNativityContent(url=url, headers={})
                soup = BeautifulSoup(content, MARKUP_TYPE)
                tableTag = soup.find('div', {'class':'rightcontblock'})
                policyRowListTag = tableTag.find('ul').findAll('li')[1:]
                policyList = []
                for rowTag in policyRowListTag:
                    policyUrl = CarPolicyCrawler.baseUrl + rowTag.find('a').get('href')
                    policyId = policyUrl.split('/')[-1].replace('.html', '')
                    if self.redisManager.isPolicyIdExisted(policyId):
                        continue
                    else:
                        self.redisManager.addPolicyId(policyId)

                    title = rowTag.find('a').get_text()
                    releaseDate = rowTag.find('small').get_text()
                    releaseDepartment = rowTag.find('span').get_text().strip()
                    if Utility.isAfterDate(releaseDate, CarPolicyCrawler.earliestDate) is False:
                        isContinue = False
                        break
                    if CarPolicyCrawler.isTitleProper(title):
                        policy = CarPolicy(id=policyId, title=title, release_date=releaseDate, release_department=releaseDepartment,
                                           url=policyUrl, policy_type=policyType)
                        if CarPolicyCrawler.getPolicyContent(policyUrl, policy) is None:
                            self.log.warning(policyUrl)
                        else:
                            policyList.append(policy)
                            self.log.info('标题[%s], 发布时间[%s], 发布单位[%s], url[%s]' % (title, releaseDate, releaseDepartment, policyUrl))

                if len(policyList) != 0:
                    self.dbManager.insertPolicyListIntoDB(policyList=policyList)
                pageTag = tableTag.find('div', {'class':'the_pages'})
                url = CarPolicyCrawler.getNextPageUrl(pageTag)

            # filename = 'data/' + pt + '.txt'
            # with open(filename, 'w', encoding='utf-8') as f:
            #     f.write('\n'.join(titleList))

if __name__ == '__main__':
    mySqlManager = DBManager()
    redisManager = CacheManager()
    log = Logger.getLogger(logFileName='carpolicy.log', loggerName='carpolicy')
    cpc = CarPolicyCrawler(redisManager=redisManager, dbManager=mySqlManager, log=log)
    cpc.startCollectData()

