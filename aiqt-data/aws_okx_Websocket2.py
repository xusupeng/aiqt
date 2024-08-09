import websocket
import json
import sys
sys.path.append('/aiqt/myenv/lib/python3.12/site-packages/okx/')
from okx.MarketData import MarketAPI
from okx.Account import AccountAPI


from okx.okxclient import OkxClient
from config import API_KEY, API_SECRET, PASSPHRASE




import okx.PublicData as PublicData

flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)

# 获取交易产品基础信息  
# 产品类型 SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权
result = publicDataAPI.get_instruments(
    instType="SWAP"
)

for i, item in enumerate(result):
    if i >= 50:
        break
    print(item)

# 获取持仓总量
import okx.MarketData as MarketData


marketDataAPI =  MarketData.MarketAPI(flag=flag)

# 获取指数行情
result = marketDataAPI.get_index_tickers(
    instId="BTC-USD"
)
print(result)


# 创建一个OkxClient实例
#子账户
#client = OkxClient(api_key="7f27a0b4-ceb3-4e4f-bcf1-f33ce44854d4", api_secret_key="3430205DBFB07579E48EE2063FDB02A0", passphrase="Aiqt@2024")
#主账户
#client = OkxClient(api_key="f2b08d9f-35c9-4b5d-b3bb-12f00b82a52d", api_secret_key="7CC4B437BAFAE692E7EEC9449FB54FAA", passphrase="Aiqt@2024")

# 
# client = OkxClient(
#     api_key=API_KEY,
#     api_secret_key=API_SECRET,
#     passphrase=PASSPHRASE,
#     use_server_time=True,
#     flag="1",
    #base_api=c.API_URL,
  #   debug=True,
    # proxy=None
# )

# 创建一个MarketAPI实例
# market = MarketAPI(client)

# 获取指定交易对的最新价格信息
# ticker = market.get_ticker(instId='BTC-USDT')

# 打印结果
# print(ticker)
# 

#account = AccountAPI(client)
#response = account.get_account_balance()
#print(response)
