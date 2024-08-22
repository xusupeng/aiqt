import logging
import asyncio
import backtrader as bt
from fastapi import FastAPI, HTTPException
import threading
from threading import Lock
import aiohttp
import os
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
sys.path.append('./aiqtEnv/Lib/site-packages/')
from typing import Union
from app.dataCollect import DataCollect
from app.myStrategy import MyStrategy


app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello, AIQT!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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


# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# 确保在模块级别声明了 strategy_running、cerebro_instance 和锁
strategy_running = False
cerebro_instance = None
lock = Lock()
# 启动策略的API端点
@app.post("/start_Strategy")
def start_strategy():
    global strategy_running, cerebro_instance
    if strategy_running:
        return {"message": "策略已经启动，不需要再启动!"}
    else:
        try:
            with lock:  # 使用锁来确保线程安全
                if strategy_running:
                    return {"message": "策略已经在运行中。"}
                strategy_running = True
                strategy_thread = threading.Thread(target=MyStrategy.run_strategy)
                strategy_thread.start()
                logger.info("策略启动成功。")
                return {"message": "策略已经启动!"}
        except Exception as e:
            logger.error(f"策略启动失败: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            return {"message": f"策略启动失败: {str(e)}"} 

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
    