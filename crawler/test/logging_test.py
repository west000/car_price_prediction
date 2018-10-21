#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import logging
# import logging.handlers
# import time
#
# logger = logging.getLogger('yiche')
# logger.setLevel('INFO')
#
# logFileName = 'logs/test.log'
# fileHandler = logging.handlers.TimedRotatingFileHandler(filename=logFileName, when='M', interval=1)
# fileHandler.setLevel('INFO')
# consoleHandler = logging.StreamHandler()
# consoleHandler.setLevel('INFO')
# logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(message)s] - [%(filename)s:%(lineno)d]')
#
# fileHandler.setFormatter(logFormat)
# consoleHandler.setFormatter(logFormat)
#
# logger.addHandler(fileHandler)
# logger.addHandler(consoleHandler)
#
# count = 300
# i = 0
# while i < count:
#     logger.info(('第%s个：' % i, time.asctime( time.localtime(time.time()))))
#     time.sleep(1)
#     i += 1

from logger import Logger
import time

Log = Logger.getLogger('test.log', 'test')
handlerList = Log.handlers
print(handlerList)


Log2 = Logger.getLogger('test.log', 'test')
handlerList = Log2.handlers
print(handlerList)