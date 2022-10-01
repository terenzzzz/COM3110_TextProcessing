# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 19:52:05 2022

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
        
# dictionary: 键值对
# 用{}表示
tel = {}

# 添加数据
tel['alf'] = 123456
print(tel) # {'alf': 123456}
tel['bobby'] = 222
print(tel) # {'alf': 123456, 'bobby': 222}
tel = {'alf':111, 'bobby':222, 'calvin':333 }
print(tel) # {'alf': 111, 'bobby': 222, 'calvin': 333}

# 更新数据
tel['alf'] = 321
print(tel) # {'alf': 321, 'bobby': 222, 'calvin': 333}

# 删除
del tel['bobby']
print(tel) # {'alf': 321, 'calvin': 333}

# 获取key tel.keys() non-standard
print(tel.keys()) # dict_keys(['alf', 'calvin'])

# 获取标准keys列表 list(tel.keys())
print(list(tel.keys())) # ['alf', 'calvin']

# 检索key是否存在
print('alf' in tel) # True

# 排序(默认升序)
# sorted() 返回列表的排序副本
# .sort() 修改原数组
x = [7,11,3,9,2]
y = sorted(x)
print('original:',x)
print('sorted:',y)

x.sort()
print('x:',x)

# 降序排序
print('Descending: ',sorted(x,reverse=True))

# λ符号 for key
# 输入一个x 会返回(x*x)+1的值
tuple = [('a', 3), ('c', 1), ('b', 5)]
# 默认按第一个值排序
print(sorted(tuple)) # [('a', 3), ('b', 5), ('c', 1)]
# 用第二个值排序
print(sorted(tuple,key=lambda s:s[1])) # [('a', 3), ('b', 5), ('c', 1)]
