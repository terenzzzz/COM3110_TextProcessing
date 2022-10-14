# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

- 方法定义

"""

def convertDistance(miles):
    kilometers = (miles * 8.0) / 5.0
    print('Distance in miles:',miles)
    print('Distance in kilometers:',kilometers)
    return kilometers

print(convertDistance(1))