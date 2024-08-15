import websockets
import json
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/okx')
from config import API_KEY, API_SECRET, PASSPHRASE

from okx.okxclient import OkxClient
import okx.PublicData as PublicData
import okx.Account as Account
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘:1

publicDataAPI = PublicData.PublicAPI(flag=flag)
# 获取交易产品基础信息  
# 产品类型 SPOT：币币   MARGIN：币币杠杆   SWAP：永续合约   FUTURES：交割合约   OPTION：期权
result = publicDataAPI.get_instruments(instType="SWAP")
for i, item in enumerate(result):
    if i >= 10: 
        break
        print("获取交易产品基础信息(SWAP永续合约)：" + item)

# 获取持仓总量
marketDataAPI =  MarketData.MarketAPI(flag=flag)
# 获取指数行情
result = marketDataAPI.get_index_tickers(
    instId="BTC-USD"
)
print("获取持仓总量:获取指数行情:BTC-USD:")
print(result)

# 查看账户余额
accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
result = accountAPI.get_account_balance()
print("查看账户余额" + result)



