import asyncio
import backtrader as bt
import aiohttp
import os
import sys
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
sys.path.append('./aiqtEnv/Lib/site-packages/')
from typing import Union
from app.dataCollect import DataCollect


# 定义一个全局变量来存储策略的状态
strategy_running = False

# 定义一个全局变量来存储Cerebro实例
cerebro_instance = None

# 定义一个函数来启动策略
class MyStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def __init__(self):
        # 保存收盘价数据
        self.dataclose = self.datas[0].close

        # 添加移动平均线指标
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def next(self):
        if self.dataclose[0] > self.sma[0]:
            self.buy()
        elif self.dataclose[0] < self.sma[0]:
            self.sell()
        print('Close, %.2f' % self.dataclose[0])
        print('SMA, %.2f' % self.sma[0])
        print('')

    # 定义一个静态函数来运行策略
    @staticmethod
    def run_strategy():
        global strategy_running, cerebro_instance
        cerebro = bt.Cerebro()
        print('tarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
        # 这里添加你的策略和数据源等设置
        # cerebro.addstrategy(YourStrategy)
        # cerebro.adddata(YourDataFeed)

        cerebro.run()
    
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        strategy_running = False

