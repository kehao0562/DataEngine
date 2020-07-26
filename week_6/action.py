# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:06:11 2020

@author: kehao
"""


import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt


def daily_collect(df):
    """
    读入原始数据集，将乘客数据按天聚合，并将时间和乘客数量列名修改符合Prophet要求

    Parameters:
        df (DataFrame): 原始数据集

    Returns:
        daily_df (DataFrame): 按天聚合的乘客数据

    """
    df['Datetime'] = pd.to_datetime(df.Datetime, format='%d-%m-%Y %H:%M')
    df.index = df.Datetime
    df.drop(['ID', 'Datetime'], axis=1, inplace=True)
    # 按天聚合
    daily_df = df.resample('D').sum()
    # 将时间顺序列名修改符合Prophet要求
    daily_df['ds'] = daily_df.index
    daily_df['y'] = daily_df.Count
    daily_df.drop('Count', axis=1, inplace=True)
    # daily_df.head()
    return daily_df


def model_forcast(daily_df, day=213):
    """
    读入按天聚合的乘客数据，利用Prophet进行预测，输出预测模型及图像

    Parameters:
        daily_df (DataFrame): 按天聚合的数据
        day (int): 预测天数

    Returns:
        model: 预测模型

    """
    # 拟合Prophet模型
    model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
    model.fit(daily_df)
    # 预测未来七个月（213天）
    future = model.make_future_dataframe(periods=213)
    forcast = model.predict(future)
    # print(forcast)
    # 绘制预测
    model.plot(forcast)
    # 查看预测各成份
    model.plot_components(forcast)
    return model


def main():
    # 读入数据集
    df = pd.read_csv('./train.csv')
    # 将乘客数量集以天为单位聚合
    daily_df = daily_collect(df)
    # 利用Prophet预测之后的乘客数量
    model = model_forcast(daily_df, day=213)


if __name__ == "__main__":
    main()