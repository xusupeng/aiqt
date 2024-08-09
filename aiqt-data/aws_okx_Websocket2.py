import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI


from okx.okxclient import OkxClient
from config import API_KEY, API_SECRET, PASSPHRASE

# 创建一个OkxClient实例
#子账户
#client = OkxClient(api_key="7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4", api_secret_key="3430205DBFB07579E48EE2063FDB02A0", passphrase="Aiqt@2024")
#主账户
#client = OkxClient(api_key="f2b08d9f-35c9-4b5d-b3bb-12f00b82a52d", api_secret_key="7CC4B437BAFAE692E7EEC9449FB54FAA", passphrase="Aiqt@2024")

from okxclient import OkxClient

client = OkxClient(
    api_key=API_KEY,
    api_secret_key=API_SECRET,
    passphrase=PASSPHRASE,
    use_server_time=True,
    flag="1",
    base_api=c.API_URL,
    debug=True,
    proxy=None
)

# 创建一个MarketAPI实例
market = MarketAPI(client)

# 获取指定交易对的最新价格信息
ticker = market.get_ticker(instId='BTC-USDT')
response = client.get_account_balance()
print(response)
# 打印结果
print(ticker)
