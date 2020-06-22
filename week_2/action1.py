# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:33:27 2020

@author: kehao
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

table_head = ['id', 'brand', 'car_model', 'type', 'description', 'problem', 'datetime', 'status']

def get_content(request_url):
    # 得到页面的内容
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

def content_analysis(soup):
    # table_head = ['id', 'brand', 'car_model', 'type', 'description', 'problem', 'datetime', 'status']
    global table_head
    df = pd.DataFrame(columns=table_head)
    # 获得表格内容
    table = soup.find('div', class_='tslb_b')
    # 获取表格所有tr标签
    tr_list = table.find_all('tr')
    for tr in tr_list:
        # 获取每行信息
        td_list = tr.find_all('td')
        # 用于保存每行结果的字典
        item = {}
        if len(td_list) > 0:
            for i in range(len(td_list)):
                item[table_head[i]] = td_list[i].text
        df = df.append(item, ignore_index=True)
    df.drop(0, axis=0, inplace=True)
    return df

def complaint_scrap():
    # 获取抱怨信息
    page_num = 20
    base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
    # table_head = ['id', 'brand', 'car_model', 'type', 'description', 'problem', 'datetime', 'status']
    global table_head
    result = pd.DataFrame(columns=table_head)
    for i in range(page_num):
        # 生成每页url
        request_url = base_url + str(i+1) + '.shtml'
        # 抓取每页内容
        soup = get_content(request_url)
        # 解析每页内容，结果添加在DataFrame最后
        df = content_analysis(soup)
        result = result.append(df)
    print(result)
    # 保存结果至csv文件
    result.to_csv('result.csv', index=False, encoding='utf-8')

def main():
    complaint_scrap()

if __name__ == "__main__":
    main()
    