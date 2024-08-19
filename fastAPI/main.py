from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



from fastapi import FastAPI
from backtrader import Cerebro, Strategy
import pandas as pd

app = FastAPI()

class MyStrategy(Strategy):
    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.bar_executed = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return

        if self.position.size == 0:
            self.order = self.buy()

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

def run_cerebro():
    cerebro = Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    data = pd.read_csv('data.csv', index_col=0, parse_dates=True)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()

@app.get('/run_cerebro')
async def run_cerebro_api():
    run_cerebro()
    return {'message': 'Cerebro run successfully'}
