# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:53:43 2020

@author: kehao
"""


import pandas as pd
import numpy as np

# 导入数据
result = pd.read_csv('car_complain.csv')

# 数据预处理
result = result.drop('problem', 1).join(result.problem.str.get_dummies(','))
problems = result[result.columns[7:]]   # 故障
problems_count = problems.sum(axis = 1) # 每个字段故障数量求和
new_result = result.loc[:,['brand','car_model']]
new_result['problem_count'] = problems_count

# 品牌投诉总数
# df = result.groupby(['brand'])['id'].agg(['count']).sort_values('count', ascending = False)
df_new = new_result.groupby(['brand'])['problem_count'].agg(['sum']).sort_values('sum', ascending = False)
print("品牌投诉总数")
# print(df)
print(df_new)

# 车型投诉总数
# df1 = result.groupby(['car_model'])['id'].agg(['count']).sort_values('count', ascending = False)
df1_new = new_result.groupby(['car_model'])['problem_count'].agg(['sum']).sort_values('sum', ascending = False)
print("车型投诉总数")
# print(df1)
print(df1_new)

# 品牌的平均车型投诉
# df2 = result.groupby(['brand','car_model'])['id'].agg(['count']).groupby(['brand']).mean().sort_values('count', ascending = False)
df2_new = new_result.groupby(['brand','car_model'])['problem_count'].agg(['sum']).groupby(['brand']).mean().sort_values('sum', ascending = False)
print("品牌的平均车型投诉")
# print(df2)
print(df2_new)