import requests
import threading
import time

# OKEx API URL
API_URL = "https://www.okex.com/api/v5/market/tickers?instType=SPOT"

# 获取数据的函数
def fetch_data():
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred: {e}")
        time.sleep(60)  # 每隔1分钟获取一次数据

# 创建并启动5个线程
threads = []
for i in range(5):
    thread = threading.Thread(target=fetch_data)
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()


    #连接mysql数据库，并写入数据库
    