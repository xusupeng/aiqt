import websockets
import json
import os
import asyncio
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/okx')
sys.path.append('./aiqtEnv/Lib/site-packages/okx')
sys.path.append('./app')
from config import API_KEY, API_SECRET, PASSPHRASE

import okx.PublicData as PublicData
import okx.Account as Account
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘:1

class DataCollect():
    def publicData():
        try:
            publicDataAPI = PublicData.PublicAPI(flag=flag)
            # 获取交易产品基础信息  
            # 产品类型 SPOT：币币   MARGIN：币币杠杆   SWAP：永续合约   FUTURES：交割合约   OPTION：期权
            result = publicDataAPI.get_instruments(instType="SWAP")
            for i, item in enumerate(result['data']):
                if i >= 5:  
                    return item
                    break
            return result['data'][0]
        except Exception as e:
            return "publicData错误： %s" % e

    def marketData():
        marketDataAPI =  MarketData.MarketAPI(flag=flag)
        # 获取 ETH-USD 指数行情
        try:
            result = marketDataAPI.get_index_tickers(instId="ETH-USD")
            return f"获取 ETH-USD 指数行情：{result}"
        except Exception as e:
            return ("错误: %s" % e)





    # 查看账户余额
    def accountBalance():
        accountAPI = Account.AccountAPI(API_KEY, API_SECRET, PASSPHRASE, False, flag)
        result = accountAPI.get_account_balance()
        return result
  


