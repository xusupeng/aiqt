import websockets
import json
import os
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/okx')
sys.path.append('./aiqtEnv/Lib/site-packages/okx')
from config import API_KEY, API_SECRET, PASSPHRASE

from okx.okxclient import OkxClient
import okx.PublicData as PublicData
import okx.Account as Account
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘:1

#publicDataAPI = PublicData.PublicAPI(flag=flag)
# 获取交易产品基础信息  
# 产品类型 SPOT：币币   MARGIN：币币杠杆   SWAP：永续合约   FUTURES：交割合约   OPTION：期权

#result = publicDataAPI.get_instruments(instType="SWAP")
#print("获取交易产品基础信息(SWAP永续合约)：%s" % result)
#for i, item in enumerate(result['data']):
#    print("获取交易产品基础信息(SWAP永续合约%s)：%s" % (i, item))
#    if i >= 5:  break

def dataCollect():
    # 获取持仓总量
    marketDataAPI =  MarketData.MarketAPI(flag=flag)
    # 获取所有指数行情
    try:
        result = marketDataAPI.get_index_tickers(instId="ETH-USD")
        print("获取行情:ETH-USD:%s" % result)
        #return result
    except Exception as e:
        print("获取行情:ETH-USD:%s" % e)




# 查看账户余额
# accountAPI = Account.AccountAPI(API_KEY, API_SECRET, PASSPHRASE, False, flag)
# result = accountAPI.get_account_balance()
# print("查看账户余额")
# print(result)



