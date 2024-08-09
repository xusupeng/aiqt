import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI






# 用你的API密钥替换下面的'YOUR_API_KEY'和'YOUR_API_SECRET'
api_key = "7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4" # "Aiqt@2024"

api_secret = "3430205DBFB07579E48EE2063FDB02A0"



# 初始化Market对象
market = MarketAPI()

# 获取交易对列表
symbols = market.get_symbols()

# 查找BTC-USDT交易对的交易对ID
for symbol in symbols:
    if symbol['instId'] == 'BTC-USDT':
        print(f"BTC-USDT的交易对ID为: {symbol['instId']}")


