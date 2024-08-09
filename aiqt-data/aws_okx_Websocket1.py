import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI


# 安装websocket库和pythonSDK库：pip install websocket-client python_okx
# 创建API对象

market_api = MarketAPI("7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4", "3430205DBFB07579E48EE2063FDB02A0", "Aiqt@2024", False)

def on_message(ws, message):
    data = json.loads(message)
    if 'table' in data and data['table'] == 'spot/ticker':
        for ticker in data['data']:
            if ticker['instrument_id'] == 'eth-usd':
                print(f"ETH/USD 最新价格: {ticker['last']}")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("连接已关闭")

def on_open(ws):
    # 订阅ETH/USD的行情数据
    subscribe_message = {
        "op": "subscribe",
        "args": ["spot/ticker:eth-usd"]
    }
    ws.send(json.dumps(subscribe_message))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://wsaws.okx.com:8443/ws/v5/public",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

    # 获取ETH/USD的行情数据
    ticker = market_api.get_ticker('ETH/USD')
    #print(f"ETH/USD 最新价格: {ticker['last']}")
    print(f"ETH/USD 最新价格: {ticker}")
    # 获取ETH/USD的深度数据
    #depth = market_api.get_depth('eth-usd', 5)
    #print(f"ETH/USD 深度数据: {depth}")
