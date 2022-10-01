# 嵌套循环: 一个循环包含另一个循环
# 对于外部循环的每次迭代，内部循环都运行到完成
outer_vals = [1, 2, 3]
inner_vals = ['A', 'B', 'C']
for oval in outer_vals:
    for ival in inner_vals:
        print(oval, ival)
"""
1 A
1 B
1 C
2 A
2 B
2 C
3 A
3 B
3 C
"""

# 排序
# 冒泡排序
# 方法沿着列表移动，比较相邻值
# 如果相邻值顺序不对，则交换它们
values = [4, 3, 6, 5, 2, 1] # original: [4, 3, 6, 5, 2, 1]
print ('original:',values) 
N = len(values)
for j in range(N-1):
    for i in range(N-1-j):
        if values[i] > values[i+1]:
            tmp = values[i]
            values[i] = values[i+1]
            values[i+1] = tmp
print ('sorted:',values) # sorted: [1, 2, 3, 4, 5, 6]



 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
