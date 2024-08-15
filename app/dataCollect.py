import websockets
import json
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/okx')
from okx.MarketData import MarketAPI    #需要安装：pip3 install python-okx
from okx.okxclient import OkxClient
from config import API_KEY, API_SECRET, PASSPHRASE
import okx.PublicData as PublicData
import okx.Account as Account

# API 初始化
apikey = "f2b08d9f-35c9-4b5d-b3bb-12f00b82a52d"
secretkey = "7CC4B437BAFAE692E7EEC9449FB54FAA"
passphrase = "Aiqt@2024"

flag = "0"  # 实盘:0 , 模拟盘:1

publicDataAPI = PublicData.PublicAPI(flag=flag)
# 获取交易产品基础信息  
# 产品类型 SPOT：币币   MARGIN：币币杠杆   SWAP：永续合约   FUTURES：交割合约   OPTION：期权
result = publicDataAPI.get_instruments(
    instType="SWAP"
)

for i, item in enumerate(result):
    if i >= 10:
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

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
# 查看账户余额
result = accountAPI.get_account_balance()
print(result)



