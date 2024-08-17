from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # 用于处理日期时间对象
import os.path  # 用于管理路径
import sys  # 用于获取脚本名称（在 argv[0]）

# 导入 backtrader 平台
import backtrader as bt


# 创建一个策略
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' 这个策略的日志函数 '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保留对数据[0]数据系列中 "close" 行的引用
        self.dataclose = self.datas[0].close

    def next(self):
        # 仅记录系列中关闭价格的参考值
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            # 当前关闭价格小于前一个关闭价格

            if self.dataclose[-1] < self.dataclose[-2]:
                # 前一个关闭价格小于前前一个关闭价格

                # 买入，买入，买入！！！（使用所有可能的默认参数）
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


if __name__ == '__main__':
    # 创建一个 Cerebro 实体
    cerebro = bt.Cerebro()

    # 添加策略
    cerebro.addstrategy(TestStrategy)

    # 数据位于 samples 的子文件夹中。需要找到脚本所在的路径，因为它可能从任何地方调用
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    # 创建一个数据源
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # 不传递此日期之前的值
        fromdate=datetime.datetime(2000, 1, 1),
        # 不传递此日期之前的值
        todate=datetime.datetime(2000, 12, 31),
        # 不传递此日期之后的值
        reverse=False)

    # 将数据源添加到 Cerebro
    cerebro.adddata(data)

    # 设置我们想要的现金起始值
    cerebro.broker.setcash(100000.0)

    # 打印起始条件
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 运行 everything
    cerebro.run()

    # 打印最终结果
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
