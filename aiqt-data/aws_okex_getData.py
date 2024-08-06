import requests
import time
import socket
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from mySQL_Data import create_connection, execute_query

def fetch_okex_data():
    url = "https://www.okex.com/api/spot/v3/instruments/ETH-USDT/candles?granularity=60"
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:
        ip_address = '104.16.160.75'  # 假设这是 www.okex.com 的IP地址
        response = session.get(url, headers={'Host': 'www.okex.com'}, verify=False)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        return None

# 其他代码保持不变

def insert_data(connection, data):
    if data is None:
        print("没有数据可插入")
        return
    cursor = connection.cursor()
    for entry in data:
        timestamp, open_price, high_price, low_price, close_price, volume, _ = entry
        query = f"""
        INSERT INTO ethUSD (timestamp, open_price, high_price, low_price, close_price, volume)
        VALUES ('{timestamp}', {open_price}, {high_price}, {low_price}, {close_price}, {volume})
        """
        try:
            cursor.execute(query)
        except Error as e:
            print(f"插入数据错误： '{e}' occurred")
    connection.commit()
    print("插入数据成功！")

# 创建数据库连接
connection = create_connection("35.175.245.164", "aiqt", "Aiqt@2024", "aiqt")

# 创建表
create_table_query = """
CREATE TABLE IF NOT EXISTS ethUSD (
  id INT AUTO_INCREMENT, 
  timestamp VARCHAR(255) NOT NULL, 
  open_price FLOAT, 
  high_price FLOAT, 
  low_price FLOAT, 
  close_price FLOAT, 
  volume FLOAT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""
execute_query(connection, create_table_query)

# 获取并插入数据
while True:
    data = fetch_okex_data()
    insert_data(connection, data)
    time.sleep(60)  # 每分钟获取一次数据