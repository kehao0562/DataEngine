# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:00:04 2020

@author: kehao
"""


import pandas as pd
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt


def text_cut(data):
    """
    读入交易记录，用word_tokenize函数进行分词

    Parameters:
        data (DataFrame): 交易记录

    Returns:
        cut_text (list): 分词结果，第一个元素为一个单词
    """
    transaction = ""
    for index, row in data.iterrows():
        row.dropna(inplace=True)
        transaction += " ".join(item for item in row)
    cut_text = word_tokenize(transaction)
    return cut_text


def create_word_cloud(cut_text, max_words=10):
    """
    读入分词结果，并根据单词频率绘制词云

    Parameters:
        cut_text (list): 分词结果

    Returns:

    """
    cut_text = " ".join(cut_text)
    wc = WordCloud(max_words=max_words, width=2000, height=1200)
    wordcloud = wc.generate(cut_text)
    wordcloud.to_file("wordcloud.jpg")
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def main():
    # 读入原始数据
    data = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
    # 将交易记录进行分词
    cut_text = text_cut(data)
    # 生成交易记录的词云
    create_word_cloud(cut_text, max_words=10)


if __name__ == "__main__":
    main()
