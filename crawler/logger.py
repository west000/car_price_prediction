#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import time


class Logger(object):
    @staticmethod
    def getLogger(logFileName, loggerName, logLevel=logging.INFO, when='D', interval=1,
                logFormatStr='%(asctime)s - %(name)s - %(levelname)s - [%(message)s] - [%(filename)s:%(lineno)d]'):
        logger = logging.getLogger(loggerName)
        logger.setLevel(logLevel)

        logFileName = 'logs/' + logFileName
        fileHandler = logging.handlers.TimedRotatingFileHandler(filename=logFileName, when=when, interval=interval)
        fileHandler.setLevel(logLevel)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logLevel)

        logFormat = logging.Formatter(logFormatStr)
        fileHandler.setFormatter(logFormat)
        consoleHandler.setFormatter(logFormat)
        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)

        return logger


if __name__ == '__main__':
    Log = Logger.getLogger(logFileName='test.log', loggerName='test')
    count = 300
    i = 0
    while i < count:
        Log.info(('第%s个：' % i, time.asctime(time.localtime(time.time()))))
        time.sleep(1)
        i += 1
