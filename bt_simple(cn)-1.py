from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # 用于处理日期时间对象
import os.path  # 用于管理路径
import sys  # 用于获取脚本名称（在 argv[0]）


# 导入 backtrader 平台
import backtrader as bt


# 创建一个策略
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' 这个策略的日志函数 '''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保留对数据[0]数据系列中 "close" 行的引用
        self.dataclose = self.datas[0].close

        # 记录买入价格和佣金
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 添加一个简单移动平均线指标
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 买入/卖出订单提交/接受到经纪商 - 无需操作
            return

        # 检查订单是否完成
        # 注意：如果资金不足，经纪商可能会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '买入执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # 卖出
                self.log('卖出执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金/拒绝')

        # 记录：没有待处理的订单
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('交易利润，毛利润 %.2f，净利润 %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # 仅记录系列中关闭价格的参考值
        self.log('Close, %.2f' % self.dataclose[0])

        # 检查是否在市场
        if not self.position:

            # 尚未 ... 我们可能买入 if ...
            if self.dataclose[0] > self.sma[0]:

                # 买入，买入，买入！！！（使用所有可能的默认参数）
                self.log('买入创建，%.2f' % self.dataclose[0])

                # 记录创建的订单以避免第二个订单
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # 卖出，卖出，卖出！！！（使用所有可能的默认参数）
                self.log('卖出创建，%.2f' % self.dataclose[0])

                # 记录创建的订单以避免第二个订单
                self.order = self.sell()
def stop(self):
        self.log('（MA周期 %2d）结束价值 %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)


if __name__ == '__main__':
    # 创建一个 cerebro 实体
    cerebro = bt.Cerebro()

    # 添加一个策略
    strats = cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10, 31))

    # 数据在 samples 的子文件夹中。需要找到脚本所在的位置，因为它可能从任何地方被调用
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    # 创建一个数据源
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # 不要在日期范围内传递值之前
        fromdate=datetime.datetime(2000, 1, 1),
        # 不要在日期范围内传递值之后
        todate=datetime.datetime(2000, 12, 31),
        # 不要反向传递值
        reverse=False)

    # 将数据源添加到 cerebro
    cerebro.adddata(data)

    # 添加一个固定大小的大小器，根据赌注
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # 设置佣金
    cerebro.broker.setcommission(commission=0.0)

    # 运行 everything
    cerebro.run(maxcpus=1)
