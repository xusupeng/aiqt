import asyncio
import backtrader as bt




# 定义一个全局变量来存储策略的状态
strategy_running = False

# 定义一个全局变量来存储Cerebro实例
cerebro_instance = None


class MyStrategy(bt.Strategy):
    # 定义一个函数来启动策略
    def run_strategy():
        global strategy_running, cerebro_instance
        cerebro = bt.Cerebro()
        print('tarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
        # 这里添加你的策略和数据源等设置
        # cerebro.addstrategy(YourStrategy)
        # cerebro.adddata(YourDataFeed)

        cerebro.run()
    
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        strategy_running = True
