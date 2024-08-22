import asyncio
import backtrader as bt
import aiohttp
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import os
sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
sys.path.append('./aiqtEnv/Lib/site-packages/')
from typing import Union
from app.dataCollect import DataCollect
from app.myStrategy_Test1 import TestStrategy

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

        cerebro.broker.setcash(100000.0) # 设置初始资金
        print('tarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
        # 这里添加你的策略和数据源等设置
        # cerebro.addstrategy(YourStrategy)
        cerebro.addstrategy(TestStrategy) # 添加策略
        cerebro.adddata(MyStrategy.getData()) # 添加数据源

        cerebro.run()
    
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        strategy_running = False
    
    @staticmethod
    def getData():  # 获取数据
        # 数据位于samples的子文件夹中。需要找到脚本的位置，因为它可能从任何地方被调用
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        datapath = os.path.join(modpath, 'binance_eth_usd_ohlcv.csv') # 数据文件路径

        # 创建一个数据源
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            # 不传递此日期之前的值
            fromdate=datetime.datetime(2024, 6, 20),
            # 不传递此日期之后的值
            todate=datetime.datetime(2024, 8, 20),
            reverse=False)

        # 将数据源添加到Cerebro
        return data

# Create a Stratey
class TestStrategy_Old(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])