# 导入所需的库和模块
import math
import time
from decimal import Decimal
from typing import Tuple, List

# 导入自定义的模块
from okx_market_maker.market_data_service.model.Instrument import Instrument
from okx_market_maker.market_data_service.model.OrderBook import OrderBook
from okx_market_maker.order_management_service.model.OrderRequest import PlaceOrderRequest, AmendOrderRequest, \
    CancelOrderRequest
from okx_market_maker.strategy.BaseStrategy import BaseStrategy, StrategyOrder, TRADING_INSTRUMENT_ID
from okx_market_maker.utils.InstrumentUtil import InstrumentUtil
from okx_market_maker.utils.OkxEnum import TdMode, OrderSide, OrderType, PosSide, InstType
from okx_market_maker.utils.WsOrderUtil import get_request_uuid

# 定义一个名为SampleMM的市场做市商策略类，继承自BaseStrategy
class SampleMM(BaseStrategy):
    def __init__(self):
        super().__init__()

    # 定义一个名为order_operation_decision的方法，用于根据当前市场数据和策略参数proposed_orders，current_orders，side，instrument生成一组订单操作请求
    def order_operation_decision(self) -> \
            Tuple[List[PlaceOrderRequest], List[AmendOrderRequest], List[CancelOrderRequest]]:
        """
        自定义市场做市商逻辑 -> 提出一组做市商订单
        :return:
        """
        # 获取交易对盘口数据
        order_book: OrderBook = self.get_order_book()
        # 获取买一和卖一的价格和数量
        bid_level = order_book.bid_by_level(1)
        ask_level = order_book.ask_by_level(1)
        # 如果买一和卖一的价格和数量都为空，则抛出异常
        if not bid_level and not ask_level:
            raise ValueError("Empty order book!")
        # 如果只有买一没有卖一，则将卖一设置为买一
        if bid_level and not ask_level:
            ask_level = order_book.bid_by_level(1)
        # 如果只有卖一没有买一，则将买一设置为卖一
        if ask_level and not bid_level:
            bid_level = order_book.ask_by_level(1)
        # 获取交易对信息
        instrument = InstrumentUtil.get_instrument(TRADING_INSTRUMENT_ID, self.trading_instrument_type)
        # 获取策略参数
        step_pct = self.params_loader.get_strategy_params("step_pct")
        num_of_order_each_side = self.params_loader.get_strategy_params("num_of_order_each_side")
        single_order_size = max(
            self.params_loader.get_strategy_params("single_size_as_multiple_of_lot_size") * instrument.lot_sz,
            instrument.min_sz)
        strategy_measurement = self.get_strategy_measurement()
        buy_num_of_order_each_side = num_of_order_each_side
        sell_num_of_order_each_side = num_of_order_each_side
        max_net_buy = self.params_loader.get_strategy_params("maximum_net_buy")
        max_net_sell = self.params_loader.get_strategy_params("maximum_net_sell")
        
        if strategy_measurement.net_filled_qty > 0:
            buy_num_of_order_each_side *= max(1 - strategy_measurement.net_filled_qty / max_net_buy, 0)
            buy_num_of_order_each_side = math.ceil(buy_num_of_order_each_side)
        if strategy_measurement.net_filled_qty < 0:
            sell_num_of_order_each_side *= max(1 + strategy_measurement.net_filled_qty / max_net_sell, 0)
            sell_num_of_order_each_side = math.ceil(sell_num_of_order_each_side)
        # 计算 proposed_buy_orders 和 proposed_sell_orders
        proposed_buy_orders = [(bid_level.price * (1 - step_pct * (i + 1)), single_order_size)
                               for i in range(buy_num_of_order_each_side)]
        proposed_sell_orders = [(ask_level.price * (1 + step_pct * (i + 1)), single_order_size)
                                for i in range(sell_num_of_order_each_side)]
        # 计算 adjusted_buy_orders 和 adjusted_sell_orders
        proposed_buy_orders = [(InstrumentUtil.price_trim_by_tick_sz(price_qty[0], OrderSide.BUY, instrument),
                                InstrumentUtil.quantity_trim_by_lot_sz(price_qty[1], instrument))
                               for price_qty in proposed_buy_orders]
        proposed_sell_orders = [(InstrumentUtil.price_trim_by_tick_sz(price_qty[0], OrderSide.SELL, instrument),
                                 InstrumentUtil.quantity_trim_by_lot_sz(price_qty[1], instrument))
                                for price_qty in proposed_sell_orders]
        # 获取当前策略订单
        current_buy_orders = self.get_bid_strategy_orders()
        current_sell_orders = self.get_ask_strategy_orders()
        # 比较 adjusted_buy_orders 和 current_buy_orders，根据比较结果生成 buy_to_place，buy_to_amend 和 buy_to_cancel 订单操作请求
        buy_to_place, buy_to_amend, buy_to_cancel = self.get_req(
            proposed_buy_orders, current_buy_orders, OrderSide.BUY, instrument)
        # 比较 adjusted_sell_orders 和 current_sell_orders，根据比较结果生成 sell_to_place，sell_to_amend 和 sell_to_cancel 订单操作请求
        sell_to_place, sell_to_amend, sell_to_cancel = self.get_req(
            proposed_sell_orders, current_sell_orders, OrderSide.SELL, instrument)
        # 返回 buy_to_place，buy_to_amend，buy_to_cancel，sell_to_place，sell_to_amend 和 sell_to_cancel
        return buy_to_place + sell_to_place, buy_to_amend + sell_to_amend, buy_to_cancel + sell_to_cancel
    
    # 定义一个名为get_req的方法，用于比较 proposed_orders 和 current_orders，根据比较结果生成订单操作请求
    def get_req(self, propose_orders: List[Tuple[str, str]],
                current_orders: List[StrategyOrder], side: OrderSide, instrument: Instrument) -> \
            Tuple[List[PlaceOrderRequest], List[AmendOrderRequest], List[CancelOrderRequest]]:
        """
        Compare proposed orders(PO) with current orders(CO), all with the same OrderSide (buy or sell orders)
        1. if the price-size pair from PO exists in CO, keep the order intact.
        2. if more PO than CO, PLACE new orders in PO' tail. i.e. if PO has (a, b, c), CO has (a1, b1),
        place a new order for order c.
        3. if more CO than PO, CANCEL existing orders in CO' tail. i.e. if PO has (a, b), CO has (a1, b1, c1),
        cancel order c1.
        4. For other PO, AMEND existing CO with new price or new size or both.
        将拟议订单（PO）与当前订单（CO）进行比较，所有订单都具有相同的OrderSide（买入或卖出订单）
        1.如果订单中的价格-尺寸对存在于CO中，请保持订单完整。
        2.如果订单多于CO，在订单尾部下新订单。即，如果PO具有（a，b，c），CO具有（a1，b1），为c订单下一个新订单。
        3.如果CO多于PO，取消CO尾部的现有订单。即，如果PO具有（a，b），CO具有（a1，b1，c1），取消订单c1。
        4.对于其他订单，以新价格或新尺寸或两者兼而有之的方式修改现有CO。
        :return: Tuple[List[PlaceOrderRequest], List[AmendOrderRequest], List[CancelOrderRequest]]
        """
        # 初始化订单操作请求列表
        to_place: List[PlaceOrderRequest] = []
        to_amend: List[AmendOrderRequest] = []
        to_cancel: List[CancelOrderRequest] = []
        # 遍历 current_orders
        for strategy_order in current_orders.copy():
            # 获取价格和数量
            price = strategy_order.price
            remaining_size = float(strategy_order.size) - float(strategy_order.filled_size)
            remaining_size = InstrumentUtil.quantity_trim_by_lot_sz(remaining_size, instrument)
            # 如果价格和数量不在 proposed_orders 中，则取消订单
            if (price, remaining_size) in propose_orders:
                current_orders.remove(strategy_order)
                propose_orders.remove((price, remaining_size))
        # 遍历propose_orders和current_orders列表，处理订单的提交、取消和修改
        for i in range(max(len(propose_orders), len(current_orders))):
             # 如果propose_orders列表比current_orders长，那么提交新的订单
            if i + 1 > len(current_orders):
                price, size = propose_orders[i]
                order_req = PlaceOrderRequest(
                    inst_id=instrument.inst_id, td_mode=self.decide_td_mode(instrument), side=side,
                    ord_type=OrderType.LIMIT,
                    size=size,
                    price=price,
                    client_order_id=get_request_uuid("order"),
                    pos_side=PosSide.net,
                    ccy=(instrument.base_ccy if side == OrderSide.BUY else instrument.quote_ccy)
                    if instrument.inst_type == InstType.MARGIN else ""
                )
                to_place.append(order_req)
                continue  # 跳过当前循环，继续下一次循环
      
            # 如果current_orders列表比propose_orders长，那么取消当前的订单
            if i + 1 > len(propose_orders):
                strategy_order = current_orders[i]
        cid = strategy_order.client_order_id
        inst_id = strategy_order.inst_id
        cancel_req = CancelOrderRequest(inst_id=inst_id, client_order_id=cid)
        to_cancel.append(cancel_req)
        continue  # 跳过当前循环，继续下一次循环
    # 如果propose_orders和current_orders列表长度相等，那么修改订单
    strategy_order = current_orders[i]
    new_price, new_size = propose_orders[i]
    remaining_size = (Decimal(strategy_order.size) - Decimal(strategy_order.filled_size)).to_eng_string()
    cid = strategy_order.client_order_id
    amend_req = AmendOrderRequest(strategy_order.inst_id, client_order_id=cid,
                                  req_id=get_request_uuid("amend"))
    # 如果修改后的订单价格和数量与原始订单不同，则添加到修改订单列表
    if new_price != strategy_order.price:
        amend_req.new_price = new_price
    if new_size != remaining_size:
        amend_req.new_size = (Decimal(strategy_order.filled_size) + Decimal(new_size)).to_eng_string()
    to_amend.append(amend_req)

        # 返回订单操作请求列表
return to_place, to_amend, to_cancel



""" 
 XXXX
这段代码是一个名为`SampleMM`的市场做市商策略类，继承自`BaseStrategy`。
`SampleMM`类中定义了一个名为`order_operation_decision`的方法，
用于根据当前市场数据和策略参数 proposed_orders，current_orders，side，instrument 生成一组订单操作请求。

首先，从`order_book`中获取买一和卖一的价格和数量，然后根据策略参数计算出 proposed_buy_orders 和 proposed_sell_orders。
接着，将 proposed_buy_orders 和 proposed_sell_orders 按照 instrument 的价格和数量进行调整，得到 adjusted_buy_orders 和 adjusted_sell_orders。

然后，比较 adjusted_buy_orders 和 current_buy_orders，根据比较结果生成 buy_to_place，buy_to_amend 和 buy_to_cancel 订单操作请求。
同样地，比较 adjusted_sell_orders 和 current_sell_orders，根据比较结果生成 sell_to_place，sell_to_amend 和 sell_to_cancel 订单操作请求。

最后，将 buy_to_place，buy_to_amend 和 buy_to_cancel 合并返回。

`get_req`方法用于比较 proposed_orders 和 current_orders，根据比较结果生成订单操作请求。
首先，从 proposed_orders 中移除已经在 current_orders 中的订单。
然后，对于剩余的 proposed_orders，如果长度大于 current_orders，则生成 PlaceOrderRequest 订单操作请求。
对于剩余的 current_orders，如果长度大于 proposed_orders，则生成 CancelOrderRequest 订单操作请求。
最后，对于剩余的 proposed_orders 和 current_orders，如果长度相等，则根据 proposed_orders 中的价格和数量生成 AmendOrderRequest 订单操作请求。

 """