#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'

import urllib, requests, time, random, re, datetime
from logger import Logger
from config import configs

MAX_RETRY_TIMES = configs.max_retry_times

Log = Logger.getLogger(logFileName='request.log', loggerName='utility')

class Utility:
    @staticmethod
    def getFloatFromStr(str):
        results = re.findall(r'\d+\.?\d*', str)
        return float(results[0]) if len(results) != 0 else 0.0

    @staticmethod
    def getIntFromStr(str):
        results = re.findall(r'\d+', str)
        return int(results[0]) if len(results) != 0 else 0

    @staticmethod
    def getNativityContent(url, headers=None, defaultRequest=True):
        content = None
        tryTimes = 0
        while content is None and tryTimes < MAX_RETRY_TIMES :
            tryTimes += 1
            try:
                if headers is None:
                    if defaultRequest:
                        content = requests.get(url).content
                    else:
                        req = urllib.request.Request(url=url)
                        response = urllib.request.urlopen(req)
                        return response.read()
                else:
                    if defaultRequest:
                        content = requests.get(url, headers=headers).content
                    else:
                        req = urllib.request.Request(url=url, headers=headers)
                        response = urllib.request.urlopen(req)
                        return response.read()
            except Exception as e:  # MaxRetryError
                print(e)
                print(('tryTimes:', tryTimes))
                content = None
                t = random.randint(60, 150)
                time.sleep(t)
            else:
                break
        if content is None:
            print(url, 'try too much times, quit!!')
        return content

    @staticmethod
    def randomSleep(low=60, high=150):
        t = random.randint(low, high)
        time.sleep(t)

    @staticmethod
    def getCurrentDate(format='%Y/%m/%d'):
        return time.strftime(format, time.localtime(time.time()))

    @staticmethod
    def getCurrentTimestamps():
        return time.time()

    @staticmethod
    def isAfterDate(sourceDate, targetDate, format='%Y-%m-%d'):
        sourceDate = datetime.datetime.strptime(sourceDate, format)
        targetDate = datetime.datetime.strptime(targetDate, format)
        return sourceDate >= targetDate

    @staticmethod
    def dateFormatConvert(dateStr, originFormat, targetFormat='%Y-%m-%d'):
        date = datetime.datetime.strptime(dateStr, originFormat)
        date = date.strftime(targetFormat)
        return date

    @staticmethod
    def getBeforeDate(dateStr, days=1):
        d = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        result = d + datetime.timedelta(days=-days)
        result = result.strftime('%Y-%m-%d')
        return result

if __name__ == '__main__':
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    content = Utility.getNativityContent('http://dealer.bitauto.com/100069933/price_detail/126282.html', headers=headers)
    print(content)