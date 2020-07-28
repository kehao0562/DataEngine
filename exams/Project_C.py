# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:45:45 2020

@author: kehao2
"""


from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./CarPrice_Assignment.csv')


def training_data_norm(data):
    """
    在原始数据上生成训练数据，将Categorical数据编码，同时将训练数据各列进行minmax变换

    Parameters:
        data (DataFrame): 原始数据

    Returns:
        train_data_norm (DataFrame)：训练数据

    """
    symbolic_index = ['fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'cylindernumber', 'fuelsystem']
    data_numeric = data.copy()
    for item in symbolic_index:
        symbols = data[item].unique()
        for i in range(len(symbols)):
            symbol = symbols[i]
            data_numeric.loc[data_numeric[item] == symbol, item] = i
    # 提取用于聚类的数据
    # train_data = data_numeric.iloc[:, 3:]
    train_data = data_numeric.copy()
    train_data.drop(['car_ID', 'CarName'], inplace=True, axis=1)
    # 规范化到 [0,1] 空间
    min_max_scaler = preprocessing.MinMaxScaler()
    train_data_norm = min_max_scaler.fit_transform(train_data)
    return train_data_norm


def elbow_method(data):
    """
    K-Means手肘法：统计不同K取值的误差平方和

    Parameters:
        data (DataFrame): 原始数据

    Returns:

    """
    train_data_norm = training_data_norm(data)
    N = range(1, 20)
    sse = []
    for k in N:
        # K-Means算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_data_norm)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    x = N
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()


def K_means(data, n_clusters):
    """
    在原数据后增加品牌和聚类结果

    Parameters:
        train_data (DataFrame): 原始数据
        n_clusters (int): 聚类数量

    Returns:
        result (DataFrame): 原数据后增加品牌和聚类
    """
    train_data_norm = training_data_norm(data)
    # 使用KMeans聚类
    kmeans = KMeans(n_clusters)
    kmeans.fit(train_data_norm)
    predict_y = kmeans.predict(train_data_norm)

    result = data.copy()
    # 提取车辆品牌
    result['CarBrand'] = [x.split(' ')[0] for x in result['CarName']]
    # 合并聚类结果，插入到原数据最后一列
    result['聚类结果'] = predict_y
    # # 打印分组情况
    # for item in sorted(result['聚类结果'].unique()):
    #     print('第{}组: '.format(item+1))
    #     # 筛选同组纪录
    #     record = result[result['聚类结果']==item]
    #     # print(record['CarName'].values)
    #     print(record['CarBrand'].values)
    return result


def vw_competetor(result):
    """
    根据聚类结果获得Volkswagen品牌竞品
    
    Parameters:
        result (DataFrame): 带有品牌和聚类信息的数据

    Returns:
        competetor (list): Volkswagen品牌竞品
    """
    # 提取品牌为volkswagen的记录
    result_vw = pd.concat([result[result['CarBrand'] == 'volkswagen'],
                           result[result['CarBrand'] == 'vw'],
                           result[result['CarBrand']=='vokswagen']])
    competetor = []
    # 获取和volkswagen品牌相同聚类结果的品牌
    for i in result_vw['聚类结果'].unique():
        competetor += list(result[result['聚类结果'] == i]['CarBrand'].unique())
    # 品牌去重
    competetor = list(set(competetor))
    # 去掉volkswagen自身
    competetor.remove('volkswagen')
    competetor.remove('vw')
    competetor.remove('vokswagen')
    return competetor


def main():
    elbow_method(data)
    result = K_means(data, n_clusters=6)
    competetor = vw_competetor(result)
    print("Volkswagen品牌竞品：")
    print(competetor)


if __name__ == "__main__":
    main()
