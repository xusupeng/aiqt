import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI
from config import API_KEY, API_SECRET, PASSPHRASE

# 创建一个OkxClient实例
client = OkxClient(api_key=API_KEY, api_secret=API_SECRET, passphrase=PASSPHRASE)

# 创建一个MarketAPI实例
market = MarketAPI(client)

# 获取指定交易对的最新价格信息
ticker = market.get_ticker(instId='BTC-USDT')

# 打印结果
print(ticker)
