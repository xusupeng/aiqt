import requests
import time
from mySQL_Data import create_connection, execute_query

def fetch_okex_data():
    url = "https://www.okex.com/api/spot/v3/instruments/ETH-USDT/candles?granularity=60"
    response = requests.get(url)
    data = response.json()
    return data

def insert_data(connection, data):
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
            print(f"The error '{e}' occurred")
    connection.commit()
    print("Data inserted successfully")

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