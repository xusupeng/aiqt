import websocket
import json
import time
import hmac
import hashlib
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from mySQL_Data import create_connection, execute_query

def fetch_okex_data(api_key, api_secret):
    # 创建签名
    timestamp = int(time.time() * 1000)
    message = f"{timestamp}GET/api/v5/market/candles?symbol=ETH-USDT&granularity=60"
    signature = requests.utils.quote(hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest())

    # 设置请求头
    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": str(timestamp),
        "OK-ACCESS-PASSPHRASE": "Aiqt@2024"
    }

    # 发送 GET 请求
    response = requests.get("https://www.okx.com/api/v5/public/websocket-token", headers=headers)
    if response.status_code == 200:
        data = response.json()
        token = data["data"][0]["token"]
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None

    # 创建WebSocket连接
    ws = websocket.WebSocketApp("wss://real.okex.com:8443/ws/v5/public",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

def on_message(ws, message):
    data = json.loads(message)
    if data["table"] == "spot/ticker":
        for entry in data["data"]:
            timestamp = entry["ts"]
            open_price = entry["open"]
            high_price = entry["high"]
            low_price = entry["low"]
            close_price = entry["close"]
            volume = entry["vol"]
            insert_data(connection, (timestamp, open_price, high_price, low_price, close_price, volume))

def on_error(ws, error):
    print(f"WebSocket错误：{error}")

def on_close(ws):
    print("WebSocket连接关闭")

def on_open(ws):
    ws.send('{"op": "subscribe", "args": ["spot/ticker:ETH-USDT"]}')

def insert_data(connection, data):
    if data is None:
        print("没有数据可插入")
        return
    cursor = connection.cursor()
    timestamp, open_price, high_price, low_price, close_price, volume = data
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
fetch_okex_data("your api key", "your api secret")
