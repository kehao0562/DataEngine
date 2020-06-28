# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:30:39 2020

@author: kehao
"""


from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt


def training_data_norm(data):
    """
    原始数据转化为[0,1]规范化的训练数据 
    
    Parameters:
        data (DataFrame): 原始数据

    Returns:
        train_data_norm (DataFrame): [0,1]规范化的训练数据 
    """
    # 获取加个维度数据
    train_data = data.iloc[:, 1:]
    # 规范化到 [0,1] 空间
    min_max_scaler = preprocessing.MinMaxScaler()
    train_data_norm = min_max_scaler.fit_transform(train_data)
    return train_data_norm


def K_means(data, n_clusters=4):
    """
    在原数据后增加聚类结果，并打印聚类结果
    
    Parameters:
        train_data (DataFrame): 原始数据
        n_clusters (int): 聚类数量，默认值为4

    Returns:
        result (DataFrame): 原数据后增加聚类 
    """
    train_data_norm = training_data_norm(data)
    # 使用KMeans聚类
    kmeans = KMeans(n_clusters)
    kmeans.fit(train_data_norm)
    predict_y = kmeans.predict(train_data_norm)
    # 合并聚类结果，插入到原数据最后一列
    result = data.copy()
    result['聚类结果'] = predict_y
    # 打印分组情况
    for item in sorted(result['聚类结果'].unique()):
        print('第{}组: '.format(item+1))
        # 筛选同组纪录
        record = result[result['聚类结果']==item]
        print(record['地区'].values)
    return result 


# K-Means手肘法：统计不同K取值的误差平方和
def elbow_method(data):
    """
    统计不同K取值的误差平方和
    
    Parameters:
        data (DataFrame): 原始数据

    Returns:
        
    """
    train_data_norm = training_data_norm(data)
    sse = []
    for k in range(1, 11):
        # K-Means算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_data_norm)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    x = range(1, 11)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()


def main():
    # 原始数据获取
    data = pd.read_csv('car_data.csv', encoding='gbk')
    # K-Means处理
    n_clusters = 4
    result = K_means(data, n_clusters)
    # 将结果导出到CSV文件中
    result.to_csv("car_data_cluster_result.csv", index=False, encoding='gbk')
    # 手肘法
    elbow_method(data)

if __name__ == "__main__":
    main()
