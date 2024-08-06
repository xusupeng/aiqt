#<<<<<<<<<<<<<<<<<<<<<<<< CodeGeeX Inline Diff>>>>>>>>>>>>>>>>>>>>>>>>
import threading
import time
import requests

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
num_threads = SQ
interval = 5  # 每隔5秒获取一次数据

# 创建一个线程列表
threads = []

# 创建并启动多线程
for i in range(num_threads):
    t = threading.Thread(target=timer_get_ticker_data, args=(interval,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("所有线程已完成")

#<<<<<<<<<<<<<<<<<<<<<<<< CodeGeeX Inline Diff>>>>>>>>>>>>>>>>>>>>>>>>

