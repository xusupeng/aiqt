from fastapi import FastAPI
import backtrader as bt
import threading
import asyncio

app = FastAPI()

# 定义一个全局变量来存储策略的状态
strategy_running = False

# 定义一个全局变量来存储Cerebro实例
cerebro_instance = None

# 定义一个函数来启动策略
def run_strategy():
    global strategy_running, cerebro_instance
    cerebro = bt.Cerebro()
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # 这里添加你的策略和数据源等设置
    # cerebro.addstrategy(YourStrategy)
    # cerebro.adddata(YourDataFeed)

    cerebro.run()
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strategy_running = False

# 启动策略的API端点
@app.post("/start_strategy/")
async def start_strategy():
    global strategy_running, cerebro_instance
    if not strategy_running:
        strategy_running = True
        cerebro_instance = bt.Cerebro()
        threading.Thread(target=run_strategy).start()
        return {"message": "Strategy策略已经启动！"}
    else:
        return {"message": "Strategy策略正在运行中，不需要再启动！"}

# 停止策略的API端点
@app.post("/stop_strategy/")
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