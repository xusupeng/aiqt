
import os
import asyncio
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
sys.path.append('./aiqtEnv/Lib/site-packages/')
from typing import Union
from fastapi import FastAPI
from app.dataCollect import DataCollect

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
    result = DataCollect.publicData()
    return {"DataCollect.publicData: %s" %result}

# 查询市场数据ETH-USD
@app.get("/marketData")
async def marketData():
    result = DataCollect.marketData()
    return {"DataCollect.marketData: %s" %result}

# 查看账户余额
@app.get("/accountBalance")
async def marketData():
    result = DataCollect.accountBalance()
    return {"DataCollect.accountBalance: %s" %result}