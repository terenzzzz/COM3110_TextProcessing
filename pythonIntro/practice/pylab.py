# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 19:51:18 2022

@author: pc
"""

# Pylab Numeric Arrays
# Pylab 提供数值数组的特殊数据类型
from pylab import *

# zeros function： 创建指定大小的数组
array = zeros(5)
print('zeros function:',array) # [0., 0., 0., 0., 0.]

# arange function: 创建初始化数组的值序列
array2 = arange(0,2,0.3)
print('arange function:',array2) # [ 0. , 0.3, 0.6, 0.9, 1.2, 1.5, 1.8]

# 多维数组
array3 = zeros((3,5)) # 3行5列
print('multi-dimensional:',array3)
# shape属性可以获取维度
print(array3.shape)

# 遍历多维数组
(d1,d2) = array3.shape
val = 0
for row in range(d1):
    for col in range(d2):
        val = val + 0.01
        array3[row][col] = val
print('new multi-dimensional:',array3)
        
