# aiqt_data_test1.py

import threading
import time
import requests
from mySQL_Data import create_connection, execute_query

# OKEx API URL
url = "https://www.okex.com/api/spot/v3/instruments/ETH-USDT/ticker"

# 定义一个函数，用于获取交易数据
def get_ticker_data():
    response = requests.get(url)
    data = response.json()
    print("当前交易数据：", data)

# 定义一个函数，用于定时获取交易数据
def timer_get_ticker_data(interval):
    while True:
        get_ticker_data()
        time.sleep(interval)

# 设置多线程参数
num_threads = 5
interval = 5  # 每隔5秒获取一次数据

# 创建一个线程列表
threads = []

# 创建并启动多线程
for i in range(num_threads):
    t = threading.Thread(target=timer_get_ticker_data, args=(interval,))
    threads.append(t)

# MySQL 连接配置
connection = create_connection("35.175.245.164", "aiqt", "Dowin@2011", "aiqt")

# 示例查询：插入数据
insert_data_query = """
INSERT INTO test_table (name, age) VALUES ('Jane Doe', 30)
"""
execute_query(connection, insert_data_query)