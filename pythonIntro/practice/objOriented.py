# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 19:54:22 2022

@author: pc
"""

# objects: 既包含数据也包含功能functionality
# 定义一个类
class Person:
    # class需要初始化方法
    def __init__(self, firstname, surname, age):
        self.firstname = firstname
        self.surname = surname
        self.age = age
        # self.species 以上物种指“本实例的物种属性”
        self.species = 'homo sapiens'
    
    # 定义class方法
    def greting(self):
        print('Hi',self.firstname)


# 创建对象实例
p1 = Person('John','Smith',37)
print(p1.species)
print(p1)
p1.greting()

# class继承
class Wizard(Person):
    # 重写Person中的init方法
    def __init__(self, firstname, surname, age):
        """
        self.firstname = firstname
        self.surname = surname
        self.age = age
        """
        # 只重写一部分
        Person.__init__(self, firstname, surname, age)
        self.species = 'homo magicus'
        
w1 = Wizard('John','Smith',37)
print(w1.firstname)
w1.greting()
