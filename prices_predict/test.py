#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'


import numpy as np, pandas as pd

# print('-'*100)
# arr1 = np.arange(10)
# print(arr1)
# print(type(arr1))
#
# print('-'*100)
# s1 = pd.Series(arr1)
# print(s1)
# print(type(s1))
#
# print('-'*100)
# dic1 = {'a':10,'b':20,'c':30,'d':40,'e':50}
# s2 = pd.Series(dic1)
# print(s2)
# print(type(s2))

# print('-'*100)
# arr2 = np.array(np.arange(12)).reshape(4,3)
# print(arr2)
# print(type(arr2))
#
# print('-'*100)
# df1 = pd.DataFrame(arr2)
# print(df1)
# print(type(df1))


# print('-'*100)
# dic2 = {'a':[1,2,3,4], 'b':[5,6,7,8], 'c':[9,10,11,12], 'd':[13,14,15,16]}
# print(dic2)
# print(type(dic2))
#
# print('-'*100)
# df2 = pd.DataFrame(dic2)
# print(df2)
# print(type(df2))

# print('-'*100)
# dic3 = {'one':{'a':1,'b':2,'c':3,'d':4}, 'two':{'a':5,'b':6,'c':7,'d':8}, 'three':{'a':9,'b':10,'c':11,'d':12}}
# print(dic3)
# print(type(dic3))
#
# print('-'*100)
# df3 = pd.DataFrame(dic3)
# print(df3)
# print(type(df3))
#
# print('-'*100)
# df4 = df3[['one','three']]
# print(df4)
# print(type(df4))
#
# print('-'*100)
# s3 = df3['one']
# print(s3)
# print(type(s3))

# print('-'*100)
# s4 = pd.Series(np.array([1,1,2,3,5,8]))
# print(s4)
# print(s4.index)
# s4.index = ['a','b','c','d','e','f']
# print(s4)
#
# print('-'*100)
# print(s4[3])
# print('-'*10)
# print(s4['e'])
# print('-'*10)
# print(s4[[1,3,5]])
# print('-'*10)
# print(s4[['a','b','d','f']])
# print('-'*10)
# print(s4[:4])
# print('-'*10)
# print(s4['c':])
# print('-'*10)
# print(s4['b':'e'])

# print('-'*100)
# s5 = pd.Series(np.array([10,15,20,30,55,80]), index = ['a','b','c','d','e','f'])
# print(s5)
# s6 = pd.Series(np.array([12,11,13,15,14,16]), index = ['a','c','g','b','d','f'])
# print(s6)
# print(s5 + s6)
# print(s5/s6)

np.random.seed(1234)
d1 = pd.Series(2*np.random.normal(size = 100)+3)
d2 = np.random.f(2,4,size = 100)
d3 = np.random.randint(1,100,size = 100)
# print(d1.count()) #非空元素计算
# print(d1.min()) #最小值
# print(d1.max()) #最大值
# print(d1.idxmin()) #最小值的位置，类似于R中的which.min函数
# print(d1.idxmax()) #最大值的位置，类似于R中的which.max函数
# print('-'*100)
# print('10%分位数', d1.quantile(0.1)) #10%分位数
# print(d1.sum()) #求和
# print(d1.mean()) #均值
# print(d1.median()) #中位数
# print('-'*100)
# print(d1.mode()) #众数
# print('-'*100)
# print('方差', d1.var()) #方差
# print(d1.std()) #标准差
# print(d1.mad()) #平均绝对偏差
# print(d1.skew()) #偏度
# print(d1.kurt()) #峰度
# print('-'*100)
# print(d1.describe()) #一次性输出多个描述性统计指标

def stats(x):
    return pd.Series([x.count(),x.min(),x.idxmin(),
                        x.quantile(.25),x.median(),
                        x.quantile(.75),x.mean(),
                        x.max(),x.idxmax(),
                        x.mad(),x.var(),
                        x.std(),x.skew(),x.kurt()],
                        index = ['Count','Min','Whicn_Min',
                        'Q1','Median','Q3','Mean',
                        'Max','Which_Max','Mad',
                        'Var','Std','Skew','Kurt'])
# result = stats(d1)
# print(result)


df = pd.DataFrame(np.array([d1,d2,d3]).T, columns=['x1','x2','x3'])
print('-'*100)
print(df.head())
print('-'*100)
print(df.apply(stats))
print('-'*100)
print(df.corr()) # 连续变量的相关系数（corr）和协方差矩阵（cov）的求解
print('-'*100)
print(df.cov())
print('-'*100)
print(df.corr('spearman')) # 相关系数的计算可以调用pearson方法或kendell方法或spearman方法，默认使用pearson方法
print('-'*100)
print(df.corrwith(df['x1'])) # 只想关注某一个变量与其余变量的相关系数的话，可以使用corrwith, 这里只关心x1与其余变量的相关系数




