#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

pool = redis.ConnectionPool(host='192.168.56.102', port=6379)
RedisManager = redis.Redis(connection_pool=pool)

# print(RedisManager.exists('yiche-carprice'))



# print(RedisManager.delete('2018/04/20-city-brand-finished'))
# print(RedisManager.delete('rrc-notsalecar'))

# RedisManager.sadd('rrc-id', 'a')
# print(RedisManager.srem('rrc-id', 'a'))
# print(RedisManager.srem('rrc-id', 'a'))
# RedisManager.sadd('rrc-id', 'b')
# RedisManager.sadd('rrc-id', 'c')
# RedisManager.sadd('rrc-id', 'd')
# RedisManager.sadd('rrc-id', 'e')
# print(RedisManager.scard('rrc-id'))
# print(RedisManager.sismember('rrc-id', 'a'))
# print(RedisManager.sismember('rrc-id', 'f'))

# RedisManager.sadd('finished-city', 'as')
# print(RedisManager.smembers('finished-city'))
# print(RedisManager.srem('rrc-id', '0c787bd524850c98'))
# RedisManager.sadd('rrc-id', '0c787bd524850c98')

# print(RedisManager.sismember('yiche-info-carid', '104326'))
# print(RedisManager.srem('yiche-info-carid', '104326'))

# print(RedisManager.sismember('yiche-info-carid', '127225'))

# print(RedisManager.delete('carpolicy'))
# print(RedisManager.srem('carpolicy', '1805032147'))

# 只清除报价即可，yiche-dealerid就不用了，免得重新爬取经销商的具体数据
# print(RedisManager.delete('yiche-carprice'))
# print(RedisManager.sismember('yiche-dealerid', '100069933'))
# print(RedisManager.sismember('yiche-dealerid', '100056499'))

# print(RedisManager.delete('yiche-carprice'))
# print(RedisManager.delete('yiche-dealerid'))

# print(RedisManager.smembers('yiche-dealerid'))
# if RedisManager.scard('yiche-dealerid') != 0:
#     print(RedisManager.srem('yiche-dealerid', *RedisManager.smembers('yiche-dealerid')))

# print(RedisManager.smembers('yiche-info-carid'))
# if RedisManager.scard('yiche-info-carid') != 0:
#     print(RedisManager.srem('yiche-info-carid', *RedisManager.smembers('yiche-info-carid')))

# print(RedisManager.smembers('rrc-id'))
# if RedisManager.scard('rrc-id') != 0:
#     RedisManager.srem('rrc-id', *RedisManager.smembers('rrc-id'))
# print(RedisManager.smembers('rrc-id'))