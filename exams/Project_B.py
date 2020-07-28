# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:38:30 2020

@author: kehao2
"""


import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# from mlxtend.preprocessing import TransactionEncoder


def get_products(data):
    """
    将订单表按照客户分组，得到每个客户的订单

    Parameters:
        data (DataFrame):原始订单表

    Returns:
        products (DataFrame): 按照客户分组的、0-1编码订单记录
    """
    products = data.groupby(data['客户ID'])['产品名称'].value_counts().unstack()
    products[products > 1] = 1
    products[np.isnan(products)] = 0
    return products


def get_rule(encoded_transaction, min_support=0.05, min_threshold=1):
    """
    读入转化为0-1编码订单记录，用apriori算法得到频繁项集和关联规则并打印

    Parameters:
        encoded_transaction (DataFrame): 0-1编码的交易记录
        min_support (float)： 最小支持度，默认为0.05
        min_threshold (float)：最小提升度，默认为1

    Returns:
        frequent_itemsets (DataFrame): 频繁项集
        rules (DataFrame): 关联规则
    """
    # 挖掘频繁项集
    frequent_itemsets = apriori(encoded_transaction, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=min_threshold)

    frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
    print('频繁项集：', frequent_itemsets)

    pd.options.display.max_columns = 100
    rules = rules.sort_values(by='lift', ascending=False)
    print('关联规则：', rules)

    return frequent_itemsets, rules


def main():
    # 读入原始数据
    data = pd.read_csv('./订单表.csv', encoding='gbk')
    # 清洗数据，获得每个客户的订单
    products = get_products(data)
    # 用apriori算法得到频繁项集和关联规则并打印
    frequent_itemsets, rules = get_rule(products, min_support=0.05, min_threshold=1)


if __name__ == "__main__":
    main()