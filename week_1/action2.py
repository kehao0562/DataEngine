# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:16:14 2020

@author: kehao
"""


import pandas as pd
import numpy as np

# 创建DataFrame
data = np.array([[68, 65, 30],
                 [95, 76, 98],
                 [98, 86, 88],
                 [90, 88, 77],
                 [80, 90, 90]])
df = pd.DataFrame(data, index = ['张飞','关羽','刘备','典韦','许褚'],
                  columns = ['语文','数学','英语'])
df.index.name = '姓名'

# 输出各科平均成绩、最小成绩、最大成绩、方差和标准差
print("课程 | 平均成绩 | 最小成绩 | 最大成绩 |  方差  |  标准差")
for item in df.columns:
    print("{0} {1:^12.2f} {2:^7} {3:^10} {4:.2f} {5:^12.2f}"
          .format(item, np.mean(df[item]), np.min(df[item]), np.max(df[item]), np.var(df[item]), np.std(df[item])))
    
# 总成绩排序进行成绩输出
df['总分'] = df.sum(axis = 1)
df1 = df.sort_values('总分', ascending = False)
df1['排名'] = np.arange(1, data.shape[0]+1)
print('总成绩排序：')
print(df1)