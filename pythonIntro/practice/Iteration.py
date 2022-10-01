# -*- coding: utf-8 -*-

def splitLine():
    print('\n')
    print("{:-^20s}".format("分割线"))
    print('\n')

# while: 只要条件满足，重复就会继续
# for: 循环重复预设次数
def triangular(n):
    trinum = 0
    while n > 0:
        trinum = trinum + n
        n = n - 1
    return trinum
print(triangular(5)) # 5+4+3+2+1=15
splitLine()

# for: 循环重复预设次数
values = ['this', 55, 'that']
for i in values:
    print(i)
splitLine()

# range: 包前不包后
# range(len(values)) = range(3); 0,1,2;  end
# range(2,5) gives: 2, 3, 4;  start and end
# range(3,10,2) gives: 3, 5, 7, 9;  start, end and step
for i in range(3):
    print(i)
splitLine()

# break: 立即终止当前迭代,并结束整个循环
# continue: 立即终止当前迭代,并开始下一个迭代
"""
while True:
    name = input('Enter name: ')
    if name == 'done':
        break
    print('Hello', name)
"""

# import: 导入第三方包
# import module: 导入整个包
# from pylab import *: 导入包中的特定项
# import pylab as pl： 给导入的包一个别名

# Lists: 列表是一个可以保存多个值的单一变量, Python列表可以混合不同类型的值
# 可以根据项目在列表中的位置(索引)访问它们
# 访问不存在的位置会报错
# 第一个项目的索引为0
list = ['this', 55, 'that']
print(list[0])  # this
splitLine()

# list中数据可以修改
list1 = ['this', 55, 'that']
list1[1] = 'and'
print(list1) # ['this', 'and', 'that']
splitLine()

# list可以扩展 通过appending关键字
list1.append('again')
print(list1) # ['this', 'and', 'that', 'again']
splitLine()

# 使用+计算两个列表的连接
list2 = ['the', 'cat', 'sat']
list3 = ['on', 'the', 'mat']
print(list2 + list3) # ['the', 'cat', 'sat', 'on', 'the', 'mat']
splitLine()

# 获取list的一个片段(包前不包后)
list4 = ['this', 'and', 'that', 'once', 'again']
print(list4[1:4]) # ['and', 'that', 'once']
splitLine()

# 获取list的长度用len方法
nums = [8, 12, 10]
print(len(nums))
splitLine()

# tuple: 元组 e.g.('this',55),括号包住
# 有顺序，可以访问通过索引，但不能修改
# 无法将新值赋给现有元组中的位置
# 不能附加到现有的元组
# 元组内存效率更高

# File Input/Output
# open(<filename>,<mode>), default mode is ’r’
# f = open('foo.txt','r') # read only
# f = open('foo.txt','w') # write only
# f = open('foo.txt','a') # append only

# 读文件
f = open('foo.txt','r')
for line in f:
    print(line, end='')
# 写入文件(覆盖原文件)
f = open('foo.txt','w')
# Print还有其他可选参数:
# end -指定在结束时添加的字符串(默认为换行符)
# sep -指定在表达式之间添加的字符串(默认为1个空格)
print('Hello World!', file=f)





















