import asyncio
from fastapi import FastAPI
import aiohttp
import os
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
sys.path.append('./aiqtEnv/Lib/site-packages/')
from typing import Union
from app.dataCollect import DataCollect
from app.bt_Strategy_Start import MyStrategy
app = FastAPI()

# 查询公共数据中的BTC-USD代码
@app.get("/publicData")
async def publicData():
    return DataCollect.publicData()

# 查询市场数据ETH-USD
@app.get("/marketData")
async def marketData():
    return DataCollect.marketData()

# 查看账户余额
@app.get("/accountBalance")
async def accountBalance():
    result = DataCollect.accountBalance()
    return result

# 启动策略的API端点
@app.post("/start_Strategy")
async def start_strategy():
    global strategy_running, cerebro_instance
    if not strategy_running:
        strategy_running = True
        await MyStrategy.run_strategy()
        return {"message": "Strategy策略已经启动！"}
    else:
        return {"message": "Strategy策略正在运行中，不需要再启动！"}

# 停止策略的API端点
@app.post("/stop_Strategy")
async def stop_strategy():
    global strategy_running
    if strategy_running:
        # 这里需要你实现停止策略的逻辑，Backtrader没有内置的停止机制，
        # 因此这可能需要你根据实际情况来实现，例如通过修改某个变量来中断循环
        strategy_running = False
        return {"message": "Strategy已经停止！"}
    else:
        return {"message": "Strategy未运行，不需要停止！"}

# 运行FastAPI应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

