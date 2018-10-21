#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, time, random
import hashlib, json
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
from model import CarBaseInfo
import datetime
from utility import Utility
from multiprocessing import Pool
import os

def countCaluateTime(function, runTimes=1000):
    beginTime = time.time()
    for i in range(1000):
        function()
    endTime = time.time()
    print(endTime - beginTime)


def getBeforeDate(dateStr, days=1):
    d = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    result = d - datetime.timedelta(days=days)
    result = result.strftime('%Y-%m-%d')
    return result

result = getBeforeDate('2018-04-01')
print(result)

quit()

def generateRandomDate(beginDate):
    endDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(endDate)
    beginDate = datetime.datetime.strptime(beginDate, '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
    days = (endDate - beginDate).days
    day = random.randint(0, days)
    result = beginDate + datetime.timedelta(days=day)
    result = result.strftime('%Y-%m-%d %H:%M:%S')
    return result

result = generateRandomDate('2017-12-22 22:44:28')
print(result)
quit()

s = '关于/附/条件/批准/美国通用汽车公司/收购/德尔福/公司/反垄断/审查/决定/的/公告/'
s = '国务院办公厅/关于/加强/内燃机/工业/节能/减排/的/意见/'
s = '关于/公布/取消/公路/养路费/等/涉及/交通/和/车辆/收费/项目/的/通知/'
s = '关于/调整/小汽车/进口/环节/消费税/的/通知/'
s = '商务部/公告/2018/年/第/34/号/ /关于/对/原产/于/美国/的/部分/进口商品/加征/关税/的/公告/'
s = '关于/在/深圳/开展/商业/车险/定价/机制/改革/试点/的/通知/'
s = s.replace('/', '')
print(s)

quit()

urlDateList = [i for i in range(105)]
listLen = len(urlDateList)
eachLen = int(listLen / 4)
resultList = []
for i in range(4):
    if i == 3:
        resultList.append(urlDateList[i*eachLen:])
    else:
        resultList.append(urlDateList[i * eachLen:(i + 1) * eachLen])

for r in resultList:
    print(r)
    print(len(r))

quit()




d1=datetime.datetime.strptime('2018-04-05', "%Y-%m-%d")
d2=datetime.datetime.strptime('2018-04-09', "%Y-%m-%d")
print((d1-d2).days)
quit()


includeKeyword = ('排量', '报废', '新能源', '二手车', '迁入', '迁出', '补贴', '农村', '下乡', '优惠',
                       '限行', '限排', '电动汽车', '电动车', '智能', '进口车', '进口汽车', '排气污染')
excludeKeyword = ('出租车', '客车', '摩托')

str = '%s|'*len(includeKeyword)
str = str % includeKeyword
str = str[:-1]
print(str)

isProper = False
title = '[关于调整完善新能源汽车推广应用财政补贴政策的通知'
if re.search('排量|报废|新能源', title) is not None:
    isProper = True
if re.search('出租车|客车|摩托', title) is not None:
    isProper = False

print(isProper)
quit()

# today = Utility.getCurrentDate(format='%Y_%m_%d')
# print(today)
print(Utility.isAfterDate('2018-04-10', '2018-04-10'))
print(Utility.isAfterDate('2018-04-10', '2018-04-11'))
print(Utility.isAfterDate('2018-04-10', '2018-04-09'))
quit()

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

quit()

# d = {'a':(1, 2), 'b':(2,3)}
# for a, (b, c) in d.items():
#     print(a, b, c)
#

# ll = [1, 2]
# a, b = ll
# print(a, b)

# dealerName = '青岛阿斯顿马丁 2014款 6.0L Carbon Black 报价 价格'
# result = dealerName.split(' ')[0]
# print(result)
#
# n = 0
# try:
#     print(1/n)
# except Exception as e:
#     print(e)
#     raise e
#
#
# message = r"ERROR - [(1452, 'Cannot add or update a child row: a foreign key constraint fails (`graduation_project`.`car_price`, CONSTRAINT `car_price_ibfk_2` FOREIGN KEY (`dealer_id`) REFERENCES `car_dealer` (`id`))')] - [yiche.py:147]"
# print(message)
# if re.search('.*?car_dealer.*?', message) is not None:
#     print('get')
# else:
#     print('not get')
# if re.search('.*?car_base_info.*?', message) is not None:
#     print('get')
# else:
#     print('not get')

# result = time.strftime('%Y/%m/%d',time.localtime(time.time()))
# print(result)

# str = '222|444||555'
# a, b, c, d = str.split('|')
# print((a, b, c, d))
#
# str = 'a %s b' % 1
# print(str)

# sql = 'UPDATE car_base_info SET stop_selling = %s WHERE unique_id in (%s)' % ('%s', '%s, %s, %s')
# print(sql)


# str = 'car_base_info, car_body_info, car_power_system, car_chassis_brake, car_security_configuration, car_drive_assistance,car_external_configuration, car_internal_configuration, car_seat_configuration, car_infotainment'
# ll = ['\'' + s + '\'' for s in str.split(', ')]
# print(','.join(ll))

# url = 'http://car.bitauto.com/quanxinaodia4l/'
# page = str(requests.get(url).content, encoding='utf-8')
# print(page)


url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0'
headers = {
            'Host': 'api.car.bitauto.com',
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',

            'Cookie':'locatecity=440100; UserGuid=01422d72-1d34-4190-9694-a9bbeb239e5c; BitAutoLogId=35ab8b34a8cb5aeba7e3794882f440bd; _dc3c=1; dcad10=; dc_search10=; CIGDCID=67b9d353d7655eb5969c78a9a176fa76; CarStateForBitAuto=29caf9d1-1784-6827-c6e0-d8d6a2cae5d2; BitAutoUserCode=03318794-21de-8b08-7584-9ed91cea00a0; CarChannelUserInfo=f55157c6-d5bf-6d5f-e81b-cdcdf49c899f%3B0%3B0; bitauto_framecity=0%2C; Hm_lvt_7b86db06beda666182190f07e1af98e3=1522111301,1522141604; selectcity=440100; bitauto_ipregion=211.97.3.171%3a%e5%b9%bf%e4%b8%9c%e7%9c%81%e5%b9%bf%e5%b7%9e%e5%b8%82%3b501%2c%e5%b9%bf%e5%b7%9e%e5%b8%82%2cguangzhou; dmts10=1; carCssummaryAdCookier=1522248206752; csids=5311_1991_5085_5083_5256_2723; Hm_lpvt_7b86db06beda666182190f07e1af98e3=1522254263; dmt10=84%7C0%7C0%7Ccar.bitauto.com%2F%7C; dm10=18%7C1522255237%7C1%7Cwww.baidu.com%7C%2Flink%3Furl%3Dz9YPNrzitnMdLFuYgKkeEUo76SgnB-JODxyxbQ8lAbdWKos5mB9F0UndBq7kmtXr%26ck%3D2541.13.202.357.554.330.148.1659%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26wd%3D%26eqid%3De704e3870001668b000000065ab8d9ef%7C%7C%7C1522063892%7C1522063892%7C1522239147%7C1522246640%7C67b9d353d7655eb5969c78a9a176fa76%7C0%7C%7C',
            'If-Modified-Since':'Tue, 27 Mar 2018 00:36:19 GMT'
        }

# response =urllib.request.urlopen(url)
# page = response.read().decode('utf-8')
# print(page)

# page = requests.request('get', url).content
# print(page)
#
# page = requests.get(url).content
# print(page)

# s = None
# if s == 'l':
#     print('y')
# else:
#     print('n')

# url = r'http://car.bitauto.com/benchiglsjijinkou/m126822/'
# content = requests.get(url).content
# soup = BeautifulSoup(content, 'lxml')
# print(soup)


# def parseCarCompareJson(soup):
#     pattern = re.compile(r'var carCompareJson = (.*?);.*', re.MULTILINE | re.DOTALL)
#     script = soup.find('script', {'type': 'text/javascript'}, text=pattern)
#     if script is None:
#         print('Error:', url)
#         quit()
#     carCompareJson = pattern.search(script.get_text()).group(1)
#     carCompareJson = carCompareJson[1:-3]
#     datas = carCompareJson.split(']],')
#     carList = []
#     for oneCarStr in datas:
#         oneCarStr = oneCarStr[2:]
#         items = oneCarStr.split('],[')
#         oneData = []
#         for item in items:
#             item = item[1:-1]
#             oneList = [item[0:] for item in item.split(r'","')]
#             oneData.append(oneList)
#         carList.append(oneData)
#     return carList
#
# def parseCarParameter(content, refererUrl):
#     # print(content)
#     result = re.search(r'http://image.bitautoimg.com/carchannel/jsnewv2/JsForParameterv2.min.js\?v=\d+', content)
#     if result is None:
#         print('Error:', 'can not search JsForParameter')
#         quit()
#     parameterUrl = result.group()
#     parameterUrl = r'http://image.bitautoimg.com/carchannel/jsnewv2/JsForParameterv2.min.js?v=201712110'
#     print(parameterUrl)
#     content = YiChe.getNativityContent(parameterUrl, {'Referer': refererUrl, 'Host': 'image.bitautoimg.com'})
#     # print(content)
#     return None

def aaaaa():
    data = """{sFieldTitle:"图片",sType:"fieldPic",sPid:"",sFieldIndex:"",sTrPrefix:"1",unit:"",joinCode:""},{sFieldTitle:"基本信息",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-carinfo"},{sFieldTitle:"厂商指导价",sType:"fieldPara",sPid:"",sTrPrefix:"1",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"商家报价",sType:"fieldPrice",sPid:"",sTrPrefix:"1",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"上市时间",sType:"fieldMulti",sPid:"385,384,383",sTrPrefix:"1,1,1",sFieldIndex:"12,11,10",unit:"/,/",joinCode:""},{sFieldTitle:"车型级别",sType:"fieldPara",sPid:"",sTrPrefix:"0",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"车身型式",sType:"fieldPara",sPid:"574",sTrPrefix:"1",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"动力类型",sType:"fieldPara",sPid:"578",sTrPrefix:"1",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"发动机",sType:"fieldMulti",sPid:"785,418,417,425",sTrPrefix:"3,3,3,3",sFieldIndex:"1,7,8,9",unit:"L ,,缸 ,",joinCode:""},{sFieldTitle:"最大功率/最大扭矩",sType:"fieldMulti",sPid:"430,429",sTrPrefix:"3,3",sFieldIndex:"2,5",unit:"kW,N.m",joinCode:",/"},{sFieldTitle:"电动机总功率/总扭矩",sType:"fieldMulti",sPid:"870,872",sTrPrefix:"3,3",sFieldIndex:"20,21",unit:"kW,N.m",joinCode:",/"},{sFieldTitle:"变速箱类型",sType:"fieldMulti",sPid:"724,712",sTrPrefix:"1,1",sFieldIndex:"7,8",unit:"挡,",joinCode:", "},{sFieldTitle:"混合工况油耗[L/100km]",sType:"fieldPara",sPid:"782",sTrPrefix:"3",sFieldIndex:"18",unit:"",joinCode:"",isVantage:"1",size:"0"},{sFieldTitle:"纯电动最大续航里程[km]",sType:"fieldPara",sPid:"883",sTrPrefix:"3",sFieldIndex:"30",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"电池充电时间",sType:"fieldMulti",sPid:"878,879",sTrPrefix:"3,3",sFieldIndex:"28,27",unit:"h,h",joinCode:""},{sFieldTitle:"0-100km/h加速时间[s]",sType:"fieldPara",sPid:"650",sTrPrefix:"3",sFieldIndex:"17",unit:"",joinCode:"",isVantage:"1",size:"0"},{sFieldTitle:"最高车速[km/h]",sType:"fieldPara",sPid:"663",sTrPrefix:"3",sFieldIndex:"16",unit:"",joinCode:""},{sFieldTitle:"环保标准",sType:"fieldPara",sPid:"421",sTrPrefix:"3",sFieldIndex:"19",unit:"",joinCode:""},{sFieldTitle:"保修政策",sType:"fieldPara",sPid:"398",sTrPrefix:"2",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"电池保修政策",sType:"fieldPara",sPid:"1006",sTrPrefix:"3",sFieldIndex:"31",unit:"",joinCode:""},{sFieldTitle:"新能源汽车国家补贴[万]",sType:"fieldPara",sPid:"997",sTrPrefix:"2",sFieldIndex:"21",unit:"",joinCode:""},{sFieldTitle:"外观颜色",sType:"fieldPara",sPid:"598",sTrPrefix:"0",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"车身尺寸",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-carbody"},{sFieldTitle:"长×宽×高[mm]",sType:"fieldMulti",sPid:"588,593,586",sTrPrefix:"2,2,2",sFieldIndex:"0,1,2",unit:",,",joinCode:",x,x",size:"1"},{sFieldTitle:"轴距[mm]",sType:"fieldPara",sPid:"592",sTrPrefix:"2",sFieldIndex:"3",unit:"",joinCode:"mm",isVantage:"1",size:"1"},{sFieldTitle:"整备质量[kg]",sType:"fieldPara",sPid:"669",sTrPrefix:"2",sFieldIndex:"4",unit:"",joinCode:"kg"},{sFieldTitle:"座位数[个]",sType:"fieldPara",sPid:"665",sTrPrefix:"2",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"行李厢容积[L]",sType:"fieldMulti",sPid:"465,466,1000",sTrPrefix:"2,2,2",sFieldIndex:"6,19,20",unit:",,",joinCode:",-,-",size:"1"},{sFieldTitle:"油箱容积[L]",sType:"fieldPara",sPid:"576",sTrPrefix:"2",sFieldIndex:"7",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"前轮胎规格",sType:"fieldPara",sPid:"729",sTrPrefix:"2",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"后轮胎规格",sType:"fieldPara",sPid:"721",sTrPrefix:"2",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"备胎",sType:"fieldPara",sPid:"707",sTrPrefix:"2",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"最小转弯直径[m]",sType:"fieldPara",sPid:"1039",sTrPrefix:"2",sFieldIndex:"22",unit:"",joinCode:""},{sFieldTitle:"最小离地间隙[mm]",sType:"fieldPara",sPid:"589",sTrPrefix:"2",sFieldIndex:"23",unit:"",joinCode:""},{sFieldTitle:"满载质量[kg]",sType:"fieldPara",sPid:"668",sTrPrefix:"2",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"轮胎规格",sType:"fieldPara",sPid:"1001",sTrPrefix:"2",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"载重质量[kg]",sType:"fieldPara",sPid:"974",sTrPrefix:"2",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"轮胎个数",sType:"fieldPara",sPid:"982",sTrPrefix:"2",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"货厢长×宽×高[mm]",sType:"fieldMulti",sPid:"966,969,970",sTrPrefix:"2,2,2",sFieldIndex:"16,17,18",unit:",,",joinCode:",x,x",isVantage:"1",size:"1"},{sFieldTitle:"动力系统",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-carengine"},{sFieldTitle:"排量",sType:"fieldPara",sPid:"423",sTrPrefix:"3",sFieldIndex:"0",unit:"mL",joinCode:""},{sFieldTitle:"最大功率[kW]",sType:"fieldPara",sPid:"430",sTrPrefix:"3",sFieldIndex:"2",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"最大马力[Ps]",sType:"fieldPara",sPid:"791",sTrPrefix:"3",sFieldIndex:"3",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"最大功率转速[rpm]",sType:"fieldPara",sPid:"433",sTrPrefix:"3",sFieldIndex:"4",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"最大扭矩[N.m]",sType:"fieldPara",sPid:"429",sTrPrefix:"3",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"最大扭矩转速[rpm]",sType:"fieldPara",sPid:"432",sTrPrefix:"3",sFieldIndex:"6",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"电动机总功率[kW]",sType:"fieldPara",sPid:"870",sTrPrefix:"3",sFieldIndex:"20",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"电动机总扭矩[N.m]",sType:"fieldPara",sPid:"872",sTrPrefix:"3",sFieldIndex:"21",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"系统综合功率[kW]",sType:"fieldPara",sPid:"1008",sTrPrefix:"3",sFieldIndex:"33",unit:"",joinCode:""},{sFieldTitle:"系统综合扭矩[N.m]",sType:"fieldPara",sPid:"1009",sTrPrefix:"3",sFieldIndex:"34",unit:"",joinCode:""},{sFieldTitle:"供油方式",sType:"fieldPara",sPid:"580",sTrPrefix:"3",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"压缩比",sType:"fieldPara",sPid:"414",sTrPrefix:"3",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"燃油标号",sType:"fieldPara",sPid:"577",sTrPrefix:"3",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"发动机启停",sType:"fieldPara",sPid:"894",sTrPrefix:"3",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"变速箱类型",sType:"fieldPara",sPid:"712",sTrPrefix:"3",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"挡位个数",sType:"fieldPara",sPid:"724",sTrPrefix:"3",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"前电动机最大功率[kW]",sType:"fieldPara",sPid:"1002",sTrPrefix:"3",sFieldIndex:"22",unit:"",joinCode:""},{sFieldTitle:"前电动机最大扭矩[N.m]",sType:"fieldPara",sPid:"1004",sTrPrefix:"3",sFieldIndex:"23",unit:"",joinCode:""},{sFieldTitle:"后电动机最大功率[kW]",sType:"fieldPara",sPid:"1003",sTrPrefix:"3",sFieldIndex:"24",unit:"",joinCode:""},{sFieldTitle:"后电动机最大扭矩[N.m]",sType:"fieldPara",sPid:"1005",sTrPrefix:"3",sFieldIndex:"25",unit:"",joinCode:""},{sFieldTitle:"电池容量[kwh]",sType:"fieldPara",sPid:"876",sTrPrefix:"3",sFieldIndex:"26",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"电池充电时间",sType:"fieldMulti",sPid:"878,879",sTrPrefix:"3,3",sFieldIndex:"28,27",unit:"h ,h",joinCode:""},{sFieldTitle:"耗电量[kwh/100km]",sType:"fieldPara",sPid:"868",sTrPrefix:"3",sFieldIndex:"29",unit:"",joinCode:"",isVantage:"1",size:"0"},{sFieldTitle:"最大续航里程[km]",sType:"fieldPara",sPid:"883",sTrPrefix:"3",sFieldIndex:"30",unit:"",joinCode:"",isVantage:"1",size:"1"},{sFieldTitle:"发动机描述",sType:"fieldPara",sPid:"945",sTrPrefix:"3",sFieldIndex:"35",unit:"",joinCode:""},{sFieldTitle:"卡车变速箱描述",sType:"fieldPara",sPid:"1011",sTrPrefix:"3",sFieldIndex:"36",unit:"",joinCode:""},{sFieldTitle:"卡车前进挡位个数",sType:"fieldPara",sPid:"980",sTrPrefix:"3",sFieldIndex:"37",unit:"",joinCode:""},{sFieldTitle:"卡车倒挡位个数",sType:"fieldPara",sPid:"981",sTrPrefix:"3",sFieldIndex:"38",unit:"",joinCode:""},{sFieldTitle:"底盘制动",sType:"bar",sPid:"",sTrPrefix:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-bottomstop"},{sFieldTitle:"驱动方式",sType:"fieldPara",sPid:"655",sTrPrefix:"4",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"前悬架类型",sType:"fieldPara",sPid:"728",sTrPrefix:"4",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"后悬架类型",sType:"fieldPara",sPid:"720",sTrPrefix:"4",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"可调悬架",sType:"fieldPara",sPid:"708",sTrPrefix:"4",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"前轮制动器类型",sType:"fieldPara",sPid:"726",sTrPrefix:"4",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"后轮制动器类型",sType:"fieldPara",sPid:"718",sTrPrefix:"4",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"驻车制动类型",sType:"fieldPara",sPid:"716",sTrPrefix:"4",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"车体结构",sType:"fieldPara",sPid:"572",sTrPrefix:"4",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"限滑差速器/差速锁",sType:"fieldMultiValue",sPid:"733",sTrPrefix:"4",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"接近角[°]",sType:"fieldPara",sPid:"591",sTrPrefix:"4",sFieldIndex:"16",unit:"",joinCode:""},{sFieldTitle:"离去角[°]",sType:"fieldPara",sPid:"581",sTrPrefix:"4",sFieldIndex:"17",unit:"",joinCode:""},{sFieldTitle:"通过角[°]",sType:"fieldPara",sPid:"890",sTrPrefix:"4",sFieldIndex:"18",unit:"",joinCode:""},{sFieldTitle:"最大涉水深度[mm]",sType:"fieldPara",sPid:"662",sTrPrefix:"4",sFieldIndex:"19",unit:"",joinCode:""},{sFieldTitle:"客车前悬架类型",sType:"fieldPara",sPid:"1012",sTrPrefix:"4",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"客车后悬架类型",sType:"fieldPara",sPid:"1013",sTrPrefix:"4",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"卡车驱动形式",sType:"fieldPara",sPid:"1014",sTrPrefix:"4",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"前桥描述",sType:"fieldPara",sPid:"975",sTrPrefix:"4",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"前桥允许载荷[kg]",sType:"fieldPara",sPid:"1015",sTrPrefix:"4",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"后桥描述",sType:"fieldPara",sPid:"976",sTrPrefix:"4",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"后桥允许载荷[kg]",sType:"fieldPara",sPid:"1016",sTrPrefix:"4",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"安全配置",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-safeconfig"},{sFieldTitle:"防抱死制动(ABS)",sType:"fieldPara",sPid:"673",sTrPrefix:"5",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"制动力分配(EBD/CBC等)",sType:"fieldPara",sPid:"685",sTrPrefix:"5",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"制动辅助(BA/EBA等)",sType:"fieldPara",sPid:"684",sTrPrefix:"5",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"牵引力控制(ARS/TCS等)",sType:"fieldPara",sPid:"698",sTrPrefix:"5",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"车身稳定控制(ESP/DSC等)",sType:"fieldPara",sTrPrefix:"5",sPid:"700",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"主驾驶安全气囊",sType:"fieldPara",sPid:"682",sTrPrefix:"5",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"副驾驶安全气囊",sType:"fieldPara",sPid:"697",sTrPrefix:"5",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"前侧气囊",sType:"fieldPara",sPid:"691",sTrPrefix:"5",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"后侧气囊",sType:"fieldPara",sPid:"680",sTrPrefix:"5",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"侧安全气帘",sType:"fieldPara",sPid:"690",sTrPrefix:"5",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"膝部气囊",sType:"fieldPara",sPid:"835",sTrPrefix:"5",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"安全带气囊",sType:"fieldPara",sPid:"845",sTrPrefix:"5",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"后排中央气囊",sType:"fieldPara",sPid:"1017",sTrPrefix:"5",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"胎压监测",sType:"fieldPara",sPid:"714",sTrPrefix:"5",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"零胎压续行轮胎",sType:"fieldPara",sPid:"715",sTrPrefix:"5",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"后排儿童座椅接口",sType:"fieldPara",sPid:"495",sTrPrefix:"5",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"驾驶辅助",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-drivingassistance"},{sFieldTitle:"定速巡航",sType:"fieldMultiValue",sPid:"545",sTrPrefix:"6",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"车道保持",sType:"fieldPara",sTrPrefix:"6",sPid:"898",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"并线辅助",sType:"fieldPara",sTrPrefix:"6",sPid:"1040",sFieldIndex:"16",unit:"",joinCode:""},{sFieldTitle:"碰撞报警/主动刹车",sType:"fieldPara",sTrPrefix:"6",sPid:"818",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"疲劳提醒",sType:"fieldPara",sPid:"1018",sTrPrefix:"6",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"自动泊车",sType:"fieldPara",sPid:"816",sTrPrefix:"6",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"遥控泊车",sType:"fieldPara",sPid:"901",sTrPrefix:"6",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"自动驾驶辅助",sType:"fieldPara",sPid:"1019",sTrPrefix:"6",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"自动驻车",sType:"fieldPara",sPid:"811",sTrPrefix:"6",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"上坡辅助",sType:"fieldPara",sPid:"812",sTrPrefix:"6",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"陡坡缓降",sType:"fieldPara",sPid:"813",sTrPrefix:"6",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"夜视系统",sType:"fieldPara",sPid:"819",sTrPrefix:"6",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"可变齿比转向",sType:"fieldPara",sPid:"1020",sTrPrefix:"6",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"前倒车雷达",sType:"fieldPara",sPid:"800",sTrPrefix:"6",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"后倒车雷达",sType:"fieldPara",sPid:"702",sTrPrefix:"6",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"倒车影像",sType:"fieldMultiValue",sPid:"703",sTrPrefix:"6",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"驾驶模式选择",sType:"fieldPara",sPid:"1021",sTrPrefix:"6",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"外部配置",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-outerconfig"},{sFieldTitle:"前大灯",sType:"fieldMultiValue",sPid:"614",sTrPrefix:"7",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"LED日间行车灯",sType:"fieldPara",sPid:"794",sTrPrefix:"7",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"自动大灯",sType:"fieldMultiValue",sPid:"609",sTrPrefix:"7",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"前雾灯",sType:"fieldPara",sPid:"607",sTrPrefix:"7",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"大灯功能",sType:"fieldMultiValue",sPid:"612",sTrPrefix:"7",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"天窗类型",sType:"fieldMultiValue",sPid:"567",sTrPrefix:"7",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"前电动车窗",sType:"fieldPara",sPid:"601",sTrPrefix:"7",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"后电动车窗",sType:"fieldPara",sPid:"1038",sTrPrefix:"7",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"外后视镜电动调节",sType:"fieldMultiValue",sPid:"622",sTrPrefix:"7",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"外后视镜加热",sType:"fieldPara",sPid:"624",sTrPrefix:"7",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"内后视镜自动防眩目",sType:"fieldPara",sPid:"621",sTrPrefix:"7",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"流媒体后视镜",sType:"fieldPara",sPid:"1041",sTrPrefix:"7",sFieldIndex:"26",unit:"",joinCode:""},{sFieldTitle:"外后视镜自动防眩目",sType:"fieldPara",sPid:"1022",sTrPrefix:"7",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"隐私玻璃",sType:"fieldPara",sPid:"796",sTrPrefix:"7",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"后排侧遮阳帘",sType:"fieldPara",sPid:"797",sTrPrefix:"7",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"后遮阳帘",sType:"fieldPara",sPid:"595",sTrPrefix:"7",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"前雨刷器",sType:"fieldMultiValue",sPid:"606",sTrPrefix:"7",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"后雨刷器",sType:"fieldMultiValue",sPid:"596",sTrPrefix:"7",sFieldIndex:"16",unit:"",joinCode:""},{sFieldTitle:"电吸门",sType:"fieldPara",sPid:"821",sTrPrefix:"7",sFieldIndex:"17",unit:"",joinCode:""},{sFieldTitle:"电动侧滑门",sType:"fieldPara",sPid:"1023",sTrPrefix:"7",sFieldIndex:"18",unit:"",joinCode:""},{sFieldTitle:"电动行李厢",sType:"fieldMultiValue",sPid:"556",sTrPrefix:"7",sFieldIndex:"19",unit:"",joinCode:""},{sFieldTitle:"车顶行李架",sType:"fieldPara",sPid:"627",sTrPrefix:"7",sFieldIndex:"20",unit:"",joinCode:""},{sFieldTitle:"中控锁",sType:"fieldMultiValue",sPid:"493",sTrPrefix:"7",sFieldIndex:"21",unit:"",joinCode:""},{sFieldTitle:"智能钥匙",sType:"fieldMultiValue",sPid:"952",sTrPrefix:"7",sFieldIndex:"22",unit:"",joinCode:""},{sFieldTitle:"远程遥控功能",sType:"fieldMultiValue",sPid:"1024",sTrPrefix:"7",sFieldIndex:"23",unit:"",joinCode:""},{sFieldTitle:"尾翼/扰流板",sType:"fieldPara",sPid:"1025",sTrPrefix:"7",sFieldIndex:"24",unit:"",joinCode:""},{sFieldTitle:"运动外观套件",sType:"fieldPara",sPid:"793",sTrPrefix:"7",sFieldIndex:"25",unit:"",joinCode:""},{sFieldTitle:"内部配置",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-innerconfig"},{sFieldTitle:"内饰材质",sType:"fieldMultiValue",sPid:"1026",sTrPrefix:"8",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"车内氛围灯",sType:"fieldPara",sPid:"795",sTrPrefix:"8",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"遮阳板化妆镜",sType:"fieldPara",sPid:"512",sTrPrefix:"8",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"方向盘材质",sType:"fieldMultiValue",sPid:"548",sTrPrefix:"8",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"多功能方向盘",sType:"fieldPara",sPid:"528",sTrPrefix:"8",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"方向盘调节",sType:"fieldMultiValue",sPid:"799",sTrPrefix:"8",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"方向盘加热",sType:"fieldPara",sPid:"956",sTrPrefix:"8",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"方向盘换挡",sType:"fieldPara",sPid:"547",sTrPrefix:"8",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"前排空调",sType:"fieldMultiValue",sPid:"839",sTrPrefix:"8",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"后排空调",sType:"fieldMultiValue",sPid:"838",sTrPrefix:"8",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"香氛系统",sType:"fieldPara",sPid:"1027",sTrPrefix:"8",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"空气净化",sType:"fieldPara",sPid:"905",sTrPrefix:"8",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"车载冰箱",sType:"fieldPara",sPid:"485",sTrPrefix:"8",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"主动降噪",sType:"fieldPara",sPid:"1043",sTrPrefix:"8",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"座椅配置",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-chair"},{sFieldTitle:"座椅材质",sType:"fieldMultiValue",sPid:"544",sTrPrefix:"9",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"运动风格座椅",sType:"fieldPara",sPid:"546",sTrPrefix:"9",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"主座椅电动调节",sType:"fieldMultiValue",sPid:"508",sTrPrefix:"9",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"副座椅电动调节",sType:"fieldMultiValue",sPid:"503",sTrPrefix:"9",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"主座椅调节方式",sType:"fieldMultiValue",sPid:"1028",sTrPrefix:"9",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"副座椅调节方式",sType:"fieldMultiValue",sPid:"1029",sTrPrefix:"9",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"第二排座椅电动调节",sType:"fieldMultiValue",sPid:"833",sTrPrefix:"9",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"第二排座椅调节方式",sType:"fieldMultiValue",sPid:"1030",sTrPrefix:"9",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"前排座椅功能",sType:"fieldMultiValue",sPid:"504",sTrPrefix:"9",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"后排座椅功能",sType:"fieldMultiValue",sPid:"1031",sTrPrefix:"9",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"前排中央扶手",sType:"fieldPara",sPid:"514",sTrPrefix:"9",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"后排中央扶手",sType:"fieldPara",sPid:"475",sTrPrefix:"9",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"第三排座椅",sType:"fieldPara",sPid:"805",sTrPrefix:"9",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"座椅放倒方式",sType:"fieldMultiValue",sPid:"482",sTrPrefix:"9",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"后排杯架",sType:"fieldPara",sPid:"474",sTrPrefix:"9",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"后排折叠桌板",sType:"fieldPara",sPid:"1032",sTrPrefix:"9",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"信息娱乐",sType:"bar",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-pastime"},{sFieldTitle:"中控彩色液晶屏",sType:"fieldMultiValue",sPid:"488",sTrPrefix:"10",sFieldIndex:"0",unit:"",joinCode:""},{sFieldTitle:"液晶屏尺寸",sType:"fieldMultiValue",sPid:"1042",sTrPrefix:"10",sFieldIndex:"18",unit:"",joinCode:""},{sFieldTitle:"全液晶仪表盘",sType:"fieldPara",sPid:"988",sTrPrefix:"10",sFieldIndex:"1",unit:"",joinCode:""},{sFieldTitle:"行车电脑显示屏",sType:"fieldMultiValue",sPid:"832",sTrPrefix:"10",sFieldIndex:"2",unit:"",joinCode:""},{sFieldTitle:"HUD平视显示",sType:"fieldPara",sPid:"518",sTrPrefix:"10",sFieldIndex:"3",unit:"",joinCode:""},{sFieldTitle:"GPS导航",sType:"fieldMultiValue",sPid:"516",sTrPrefix:"10",sFieldIndex:"4",unit:"",joinCode:""},{sFieldTitle:"智能互联定位",sType:"fieldPara",sPid:"1033",sTrPrefix:"10",sFieldIndex:"5",unit:"",joinCode:""},{sFieldTitle:"语音控制",sType:"fieldPara",sPid:"1035",sTrPrefix:"10",sFieldIndex:"6",unit:"",joinCode:""},{sFieldTitle:"手机互联(Carplay&Android)",sType:"fieldMultiValue",sPid:"1036",sTrPrefix:"10",sFieldIndex:"7",unit:"",joinCode:""},{sFieldTitle:"手机无线充电",sType:"fieldPara",sPid:"1037",sTrPrefix:"10",sFieldIndex:"8",unit:"",joinCode:""},{sFieldTitle:"手势控制系统",sType:"fieldPara",sPid:"1034",sTrPrefix:"10",sFieldIndex:"9",unit:"",joinCode:""},{sFieldTitle:"CD/DVD",sType:"fieldMultiValue",sPid:"510",sTrPrefix:"10",sFieldIndex:"10",unit:"",joinCode:""},{sFieldTitle:"蓝牙/WIFI连接",sType:"fieldMultiValue",sPid:"479",sTrPrefix:"10",sFieldIndex:"11",unit:"",joinCode:""},{sFieldTitle:"外接接口",sType:"fieldMultiValue",sPid:"810",sTrPrefix:"10",sFieldIndex:"12",unit:"",joinCode:""},{sFieldTitle:"车载行车记录仪",sType:"fieldPara",sPid:"1044",sTrPrefix:"10",sFieldIndex:"19",unit:"",joinCode:""},{sFieldTitle:"车载电视",sType:"fieldPara",sPid:"559",sTrPrefix:"10",sFieldIndex:"13",unit:"",joinCode:""},{sFieldTitle:"音响品牌",sType:"fieldMultiValue",sPid:"473",sTrPrefix:"10",sFieldIndex:"14",unit:"",joinCode:""},{sFieldTitle:"扬声器数量[个]",sType:"fieldMultiValue",sPid:"523",sTrPrefix:"10",sFieldIndex:"15",unit:"",joinCode:""},{sFieldTitle:"后排液晶屏/娱乐系统",sType:"fieldMultiValue",sPid:"477",sTrPrefix:"10",sFieldIndex:"16",unit:"",joinCode:""},{sFieldTitle:"车载220V电源",sType:"fieldMultiValue",sPid:"467",sTrPrefix:"10",sFieldIndex:"17",unit:"",joinCode:""},{sFieldTitle:"选配包",sType:"optional",sPid:"",sFieldIndex:"",unit:"",joinCode:"",scrollId:"params-optional"}"""
    for str in data.split('},{'):
        print(str)

# def updateDict(d={}):
#     d1 = {'a':11}
#     d.update(d1)
# d = {1:1}
# updateDict(d)
# print(d)

# d1 = {1:2}
# d2 = {}
# z = d1.copy()
# z.update(d2)
# print(z)

# def test():
#     data = r'[[["128811","1.2T CVT GL 智享版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2018","在产","在销","","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["12.28万","11.08-12.30万","","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","23","3","2018","三厢","汽油"],["4620","1775","1480","2700","1300","5","426","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.4","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","无","有","无"],["卤素","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","无","有","塑料","无","上下调节,前后调节","无","无","手动空调","手动空调","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["128812","1.2T CVT GL-i 智辉版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2018","在产","在销","","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["13.68万","12.48-13.70万","","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","23","3","2018","三厢","汽油"],["4620","1775","1480","2700","1315","5","452","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.6","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["LED","有","自动开闭","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","无","有","塑料","有","上下调节,前后调节","无","无","手动空调","手动空调","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["普通液晶屏","无","有","无","无","无","无","Android","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["128813","双擎 1.8L E-CVT 智尚版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2018","在产","在销","","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["15.28万","14.08-15.30万","","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","23","3","2018","三厢","油电混合"],["4630","1775","1485","2700","1405","5","","45","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","有","有","无","有","无"],["LED","有","自动开闭","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["皮质","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","无","有","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123737","改款 1.2T 手动 GL","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","6.8","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["10.98万","9.78-10.98万","1.30万","3年或10万公里","1.2","涡轮增压","","6","手动","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1280","5","426","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","手动","6","","","5.7","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","无","无","无"],["卤素","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","无","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","2-4","无","无","","无"]],[["123739","改款 1.2T 手动 GL-i","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","7.4","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["11.98万","10.78-11.98万","1.30万","3年或10万公里","1.2","涡轮增压","","6","手动","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1295","5","452","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","手动","6","","","5.8","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","无","无"],["卤素","无","无","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","有","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","2-4","无","无","8.0","无"]],[["123741","改款 1.2T 手动 GL-i真皮版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","6.32","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["12.68万","11.48-12.68万","1.30万","3年或10万公里","1.2","涡轮增压","","6","手动","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1295","5","452","53","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","手动","6","","","5.8","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","无","无"],["卤素","无","无","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","皮质","有","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["皮质","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["123738","改款 1.2T CVT GL","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","6.52","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["11.98万","10.78-11.98万","1.30万","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1300","5","426","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.4","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","无","有","无"],["卤素","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","无","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","2-4","无","无","","无"]],[["123740","改款 1.2T CVT GL-i","http://img1.bitautoimg.com/autoalbum/files/20170518/998/14493999833564_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","7.15","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["12.98万","11.78-12.98万","1.30万","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1315","5","452","53","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.6","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["卤素","无","无","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","有","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","2-4","无","无","8.0","无"]],[["123742","改款 1.2T CVT GL-i真皮版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","6.91","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["13.68万","12.48-13.68万","1.30万","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1315","5","452","53","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.6","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["卤素","无","无","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","皮质","有","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["皮质","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["123743","改款 1.2T CVT GLX-i","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","8","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["14.38万","13.18-14.38万","1.30万","3年或10万公里","1.2","涡轮增压","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1320","5","452","53","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1197","1.2","85","116","5200-5600","185","1500-4000","直列","4","涡轮增压","直喷","10.0","92号","有","CVT无级变速","8","","","5.6","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["卤素","无","自动开闭","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","无","自动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["123735","改款 1.6L 手动 GL","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","6.55","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["10.78万","9.58-10.78万","1.30万","3年或10万公里","1.6","自然吸气","","5","手动","","18","4","2017","三厢","汽油"],["4630","1775","1480","2700","1265","5","426","55","195/65 R15","195/65 R15","全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1598","1.6","90","122","6000","154","5200","直列","4","自然吸气","多点电喷","10.2","92号","无","手动","5","","","6.3","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","无","无","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","无","无","无","无","无","无","无","无","无"],["卤素","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","无","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123736","改款 1.6L CVT GL","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","8.4","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["11.78万","10.58-11.78万","1.30万","3年或10万公里","1.6","自然吸气","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4630","1775","1480","2700","1285","5","426","55","195/65 R15","195/65 R15","全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1598","1.6","90","122","6000","154","5200","直列","4","自然吸气","多点电喷","10.2","92号","无","CVT无级变速","8","","","5.9","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","无","无","有","有","无","有","无","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","无","无","无","无","无","无","无","无","无"],["卤素","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无","无","无","无","无"],["塑料","无","有","塑料","无","上下调节,前后调节","无","无","手动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123730","改款 双擎 1.8L E-CVT 先锋版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","5","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["13.98万","12.88-13.98万","1.00万","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","18","4","2017","三厢","油电混合"],["4630","1775","1485","2700","1375","5","","45","195/65 R15","195/65 R15","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","无","有","无"],["LED","无","无","有","高度调节","无","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无钥匙启动","无","无","无","无"],["塑料","有","有","塑料","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123731","改款 双擎 1.8L E-CVT 领先版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","4.9","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["14.38万","13.28-14.38万","1.00万","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","18","4","2017","三厢","油电混合"],["4630","1775","1485","2700","1405","5","","45","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","无","有","无"],["LED","无","无","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无钥匙启动","无","无","无","无"],["塑料","有","有","塑料","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","无","无","无","无","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123732","改款 双擎 1.8L E-CVT 精英版","http://img1.bitautoimg.com/autoalbum/files/20170722/332/01145433274068_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","4.63","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["14.98万","13.78-14.98万","1.00万","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","18","4","2017","三厢","油电混合"],["4630","1775","1485","2700","1405","5","","45","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","有","有","无","有","无"],["LED","无","自动开闭","有","高度调节","单天窗","有","有","电动调节,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["皮质","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","无","有","无"],["无","无","有","无","无","无","无","无","无","无","单碟cd","无","AUX,USB","无","无","5-6","无","无","","无"]],[["123744","改款 1.8L CVT GLX-i","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","停产","在销","4.6","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["15.38万","14.18-15.38万","1.30万","3年或10万公里","1.8","自然吸气","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1315","5","452","53","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1798","1.8","103","140","6400","173","4000","直列","4","自然吸气","多点电喷","10.0","92号","有","CVT无级变速","8","","","5.9","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","无","无"],["LED","有","自动开闭","有","高度调节","单天窗","有","有","电动调节,电动折叠,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","无","自动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["123733","改款 双擎 1.8L E-CVT 豪华版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","4.75","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["16.08万","14.98-16.08万","1.00万","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","18","4","2017","三厢","油电混合"],["4630","1775","1485","2700","1405","5","","45","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["无","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["LED","有","自动开闭","有","高度调节","单天窗","有","有","电动调节,电动折叠,后视镜加热","","有","有","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["织物","无","无","无","靠背调节,高低调节,前后调节","靠背调节,前后调节","无","无","无","无","有","有","无","无","有","无"],["触控式液晶屏","无","有","无","无","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["121233","改款 1.8L CVT Premium 至高版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","停产","在销","5.8","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["16.38万","15.08-16.38万","1.30万","3年或10万公里","1.8","自然吸气","","8","CVT无级变速","","18","4","2017","三厢","汽油"],["4620","1775","1480","2700","1320","5","452","53","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8","145"],["1798","1.8","103","140","6400","173","4000","直列","4","自然吸气","多点电喷","10.0","92号","有","CVT无级变速","8","","","5.9","国五","","","","","","","","","","","","","","","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","有","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","无","无"],["LED","有","自动开闭","有","高度调节","单天窗","有","有","电动调节,电动折叠,后视镜加热","","无","无","无","无","无","有","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","无","自动空调","无","无","有","无","无"],["织物","无","电动调节","无","靠背调节,高低调节,腰部调节,前后调节","靠背调节,前后调节","无","无","加热","无","有","有","无","按比例放倒","有","无"],["触控式液晶屏","无","有","无","有","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]],[["123734","改款 双擎 1.8L E-CVT 旗舰版","http://img3.bitautoimg.com/autoalbum/files/20171128/885/20171128173247324799324_2.jpg","1879","卡罗拉","卡罗拉","kaluola","2017","在产","在销","","http://baa.bitauto.com/corolla/","紧凑型车","黑云母色,#131718|深棕云母金属色,#4c4334|铂青铜金属色,#7a613f|红云母金属色,#9E2A33|浅黄云母金属色,#cbbda3|银金属色,#d8dde0|珍珠白色,#f8fbf4|超级白色,#FFFFFF"],["17.58万","16.48-17.58万","1.00万","3年或10万公里","1.8","自然吸气","","无","E-CVT无级变速","180","18","4","2017","三厢","油电混合"],["4630","1775","1485","2700","1410","5","","45","205/55 R16","205/55 R16","非全尺寸","3年或10万公里","","","","","","","","","","","10.8",""],["1798","1.8","73","99","5200","142","4000","直列","4","自然吸气","多点电喷","13.0","92号","无","E-CVT无级变速","无","180","","4.2","国五","53","207","","","","","","","","","","","","100","","","","",""],["前轮驱动","麦弗逊式独立悬架","扭力梁式非独立悬架","无","通风盘","盘式","手拉式","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","有","无","无","无","无","无","有"],["定速巡航","无","无","无","无","无","无","无","有","无","无","无","无","无","后方影像","有","无"],["LED","有","自动开闭,自动远近光","有","高度调节","单天窗","有","有","电动调节,电动折叠,后视镜加热","","有","有","无","无","无","感应雨刷","无","无","无","无","无","遥控中控","智能进入,无钥匙启动","无","无","无","无"],["塑料","有","有","皮质","有","上下调节,前后调节","无","有","自动空调","无","无","有","无","无"],["织物","无","电动调节","无","靠背调节,高低调节,腰部调节,前后调节","靠背调节,前后调节","无","无","加热","无","有","有","无","无","有","无"],["触控式液晶屏","无","有","无","有","无","无","无","无","无","无","蓝牙","AUX,USB","无","无","5-6","无","无","8.0","无"]]]'
#     # data = r'[[["110883","3.9T 基本版","http://img3.bitautoimg.com/autoalbum/files/20160415/246/04493824620365_2.jpg","2716","California T","法拉利California T","falalicalifornia","2015","停产","在销","18.9","http://baa.bitauto.com/crossblue/","中型跑车","红色,#FF0000"],["308.80万","308.80-308.80万","","3年或不限里程","3.9","涡轮增压","","7","双离合","316","20","4","2014","跑车","汽油"],["4570","1910","1322","2670","1730","4","240","78","245/40 R19","285/40 R19","无备胎","3年或不限里程","","","","","","","","340","","","",""],["3855","3.9","412","560","7500","755","4750","V型","8","涡轮增压","直喷","9.4","98号","有","双离合","7","316","3.6","10.9","国五","","","","","","","","","","","","","","","","","","",""],["后轮驱动","双叉臂式独立悬架","多连杆式独立悬架","有","碳纤维陶瓷","碳纤维陶瓷","电子驻车","承载式","无","","","","","","","","","","",""],["有","有","有","有","有","有","有","无","有","无","无","无","无","有","无","无"],["定速巡航","无","无","无","无","无","无","有","有","选配","无","无","选配","选配","无,后方影像|0","有","无"],["LED","有","自动开闭,自动转向|0","无","高度调节,大灯清洗","无","有","无","电动调节,电动折叠,后视镜记忆,后视镜加热","","有","无","无","无","无","感应雨刷","无","无","无","无","无","遥控中控","无钥匙启动","无","无","有","无"],["皮质","无","有","皮质","有","电动上下前后调节,记忆","无","有","双温区自动空调","手动空调","无","无","无","无"],["皮质","有","带记忆电动调节","电动调节","靠背调节,高低调节,腰部调节,腿托调节,前后调节,腰夹调节","靠背调节,高低调节,腰部调节,腿托调节,前后调节,腰夹调节","无","无","无,加热|0,通风|0","无","有","无","无","全部放倒","无","无"],["触控式液晶屏","无","有","无","有","无","无","无","无","无","多碟dvd","蓝牙","AUX,USB,SD卡槽","无","JBL","7-8","无","无","","无"]]]'
#     print(data)
#     data = data[1:-3]
#     datas = data.split(']],')
#     carList = []
#     for oneCarStr in datas:
#         oneCarStr = oneCarStr[2:]
#         items = oneCarStr.split('],[')
#         oneData = []
#         for result in items:
#             item = item[1:-1]
#             oneList = [item[1:-1] for item in result.split(r'","')]
#             oneData.append(oneList)
#         # print(oneData)
#         carList.append(oneData)
#     print(carList)

# test()
# countCaluateTime(test)

# def generateUniqueId(str):
#     md5 = hashlib.md5()
#     md5.update(str.encode('utf-8'))
#     return md5.hexdigest()


# print('[Warnning:%s]' % time.asctime(time.localtime(time.time())))

# class RenRenChe:
#     baseURL = 'https://renrenche.com/'
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#         'Host':'www.renrenche.com'
#     }
#     cityMap = {}
#
#     @staticmethod
#     def getContent():
#         return RenRenChe.baseURL
#
#     @staticmethod
#     def getCityMap():
#         RenRenChe.cityMap['1'] = 1
#         return RenRenChe.cityMap
#
# print(RenRenChe.getContent())
# print(RenRenChe.getCityMap())

# d = {}
# print(len(d))
# if len(d) == 0:
#     print('empty')


# class Utility:
#     @staticmethod
#     def getFloatFromStr(str):
#         results = re.findall(r'\d+\.?\d*', str)
#         return float(results[0]) if len(results) != 0 else 0.0
#
# priceWithTax = ['新车万', '税2.74万']
# print(Utility.getFloatFromStr(priceWithTax[0]))
# print(Utility.getFloatFromStr(priceWithTax[1]))

# def changeList(list):
#     list = []
#     list += [1,2,3]
#
# intList = [1,2]
# changeList(intList)
# print(intList)

# str = '/cd/feiyate/'
# list = str.split('/')
# print(list)