import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI


from okx.okxclient import OkxClient
from config import API_KEY, API_SECRET, PASSPHRASE

# 创建一个OkxClient实例
client = OkxClient(api_key="7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4", api_secret_key="3430205DBFB07579E48EE2063FDB02A0", passphrase="Aiqt@2024")

# 创建一个MarketAPI实例
market = MarketAPI(client)

# 获取指定交易对的最新价格信息
ticker = market.get_ticker(instId='BTC-USDT')

# 打印结果
print(ticker)
