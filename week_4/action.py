# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 21:29:05 2020

@author: kehao
"""


import pandas as pd
import numpy as np
# from efficient_apriori import apriori
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

def get_transaction(data):
    """
    读入原始数据，去除NaN值得到交易记录
    
    Parameters:
        data (DataFrame): 原始数据
        
    Returns:
        transaction (二维list): 去除NaN值的交易记录
    """

    transaction = []
    for index,row in data.iterrows():
        row.dropna(inplace=True)
        transaction.append(row.tolist())
    return transaction


def transaction_encoder(transaction):
    """
    读入交易记录，转化为0-1编码交易记录
    
    Parameters:
        transaction (二维list): 交易记录
        
    Returns:
        encoded_transaction (DataFrame): 0-1编码的交易记录
    """
    te = TransactionEncoder()	# 定义模型
    df_tf = te.fit_transform(transaction)
    encoded_transaction = pd.DataFrame(df_tf, columns=te.columns_)
    return encoded_transaction


def get_rule(encoded_transaction, min_support=0.05, min_threshold=1):
    """
    读入转化为0-1编码交易记录，用apriori算法得到频繁项集和关联规则并打印
    
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
    data = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
    # 清洗数据，获得交易记录条目
    transaction = get_transaction(data)
    # 对交易记录进行布尔编码
    encoded_transaction = transaction_encoder(transaction)
    # 用apriori算法得到频繁项集和关联规则并打印
    frequent_itemsets, rules = get_rule(encoded_transaction, min_support=0.05, min_threshold=1)
    

if __name__ == "__main__":
    main()