import websocket
import json
from okex import AccountAPI, MarketAPI


# 安装websocket库和pythonSDK库：pip install websocket-client okex-python-sdk-api


# 创建API对象
market_api = MarketAPI(api_key, secret_key, passphrase, False)

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
    ticker = market_api.get_ticker('eth-usd')
    print(f"ETH/USD 最新价格: {ticker['last']}")

    # 获取ETH/USD的深度数据
    depth = market_api.get_depth('eth-usd', 5)
    print(f"ETH/USD 深度数据: {depth}")