import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI


# 用你的API密钥替换下面的'YOUR_API_KEY'和'YOUR_API_SECRET'
api_key = "7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4" # "Aiqt@2024"

api_secret = "3430205DBFB07579E48EE2063FDB02A0"

# 创建Account和Order对象
account = AccountAPI(api_key, api_secret)
#order = Order(api_key, api_secret)

# 获取账户余额

balance = account.get_balance()
print(balance)


