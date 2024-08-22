from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # 用于日期时间对象
import os.path  # 用于管理路径
import sys  # 用于找出脚本名称（在argv[0]中）

# 导入backtrader平台
import backtrader as bt

# 创建一个策略
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        '''记录此策略的日志函数'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保留对data[0]数据系列中“收盘”行的引用
        self.dataclose = self.datas[0].close

        # 用于跟踪待处理的订单
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单提交/被经纪人接受 - 无需操作
            return

        # 检查订单是否已完成
        # 注意：如果现金不足，经纪人可能会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买入执行, %.2f' % order.executed.price)
            elif order.issell():
                self.log('卖出执行, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金/被拒绝')

        # 记下：没有待处理的订单
        self.order = None

    def next(self):
        # 简单地记录来自引用的系列的收盘价格
        self.log('收盘, %.2f' % self.dataclose[0])

        # 检查是否有待处理的订单...如果有，我们不能发送第二个
        if self.order:
            return

        # 检查我们是否在市场中
        if not self.position:

            # 还没有...我们可能会买入，如果...
            if self.dataclose[0] < self.dataclose[-1]:

                if self.dataclose[-1] < self.dataclose[-2]:

                    # 当前收盘低于上一个收盘

                    # 上一个收盘也低于上上个收盘

                    # 买入，买入，买入!!!（使用默认参数）
                    self.log('买入创建, %.2f' % self.dataclose[0])

                    # 跟踪创建的订单，以避免第二个订单
                    self.order = self.buy()

        else:

            # 已经在市场中...我们可能会卖出
            if len(self) >= (self.bar_executed + 5):
                # 卖出，卖出，卖出!!!（使用所有可能的默认参数）
                self.log('卖出创建, %.2f' % self.dataclose[0])

                # 跟踪创建的订单，以避免第二个订单
                self.order = self.sell()

if __name__ == '__main__':
    # 创建一个 cerebro 实体
    cerebro = bt.Cerebro()

    # 添加一个策略
    cerebro.addstrategy(TestStrategy)

    # 数据位于samples子文件夹中。需要找到脚本的位置，因为它可能从任何地方被调用
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    # 创建一个数据源
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # 不要传递此日期之前的值
        fromdate=datetime.datetime(2000, 1, 1),
        # 不要传递此日期之后的值
        todate=datetime.datetime(2000, 12, 31),
        # 逆向数据
        reverse=False)

    # 将数据源添加到Cerebro
    cerebro.adddata(data)

    # 设置我们希望的起始现金
    cerebro.broker.setcash(100000.0)

    # 打印出起始条件
    print('起始投资组合价值: %.2f' % cerebro.broker.getvalue())

    # 运行所有内容
    cerebro.run()

    # 打印出最终结果
    print('最终投资组合价值: %.2f' % cerebro.broker.getvalue())