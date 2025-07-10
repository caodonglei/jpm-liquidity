import time
import random
import traceback
from logging import Logger

#from utils.libs import get_config, get_config_version
#from .safe_jcspot_api import (
#    local_logger as jc_safe_logger,
#    safe_self_trade as jc_safe_self_trade,
#    safe_top_askbid as jc_safe_order_book,
#)
from common.cexapi.market import get_ticker
from jpm_config import ST_STRATEGY



async def self_trade(symbol: str, param: dict, rand_val: int) -> bool:
    ### strategy assembly

    # random_coef in [0.9995 ~ 1.0005]
    qty_random_coef = 0.9995 + 0.00001 * rand_val

    base_price = 0
    # get recent trade from hedge
    trade = get_ticker(param['quote_exchange'], param['quote_symbol'])

    # minute: the minute of last selftrade
    # price:  the price of last selftrade
    # qty:    the quantity of last selftrade
    pre_st_minute = self._prev_st.setdefault(symbol, {'price':0,'minute':0,'qty':0})['minute']
    current_minute = int(int(time.time()) / 60) % 60
    # self-trade at least once for each minute
    if not trade and (current_minute == pre_st_minute or self._prev_st[symbol]['price'] == 0):
        self.logger.warning('skip self-trade due to no ticker %s: previous st %s',
            symbol, self._prev_st[symbol])
        return False

    pre_st_status = self._prev_st[symbol]
    if trade:
        base_price = trade['price']
        self.logger.debug('gate ticker %s %s', base_price, trade)
        qty = trade['qty'] * (1 - 0.0001 * param['qty_discount'])
        self.logger.debug('bn ticker %s %s', base_price, qty)

    ob = jc_safe_order_book(symbol)
    if not ob or not ob[0]['ap'] or not ob[0]['bp']:
        self.logger.warning('no order book %s', symbol)
        return False

    top_ask, top_ask_qty = float(ob[0]['ap']), float(ob[0]['aq'])
    top_bid, top_bid_aty = float(ob[0]['bp']), float(ob[0]['bq'])
    price_decimals = param['price_decimals']
    if base_price:
        # copy binance trade price
        price = base_price
        # for real ticker, make little change for sequent st price
        if pre_st_status['price'] == price:
            # this turn self-trade price = pre turn price, change a little
            if price == top_ask:
                price -= 1.0 / 10 ** price_decimals
            else:
                price += 1.0 / 10 ** price_decimals
        elif pre_st_status['price'] > 0:
            if abs(price / pre_st_status['price'] - 1) > param['price_divergence']:
                self.logger.error("Abnormal Ticker Volatility %s: pre price=%s, price=%s",
                    symbol, pre_st_status['price'], price)
                if price > pre_st_status['price']:
                    price = pre_st_status['price'] * (1 + param['price_divergence'])
                else:
                    price = pre_st_status['price'] * (1 - param['price_divergence'])
        qty *= qty_random_coef
    else:
        # mock trade using previous st price
        price = pre_st_status['price']
        qty = 0.5 * (top_ask_qty + top_bid_aty) * qty_random_coef

    price = round(price, price_decimals)
    self.logger.debug('symbol %s ,price %s,qty %s', symbol, price, qty)
    qty = min(round(max(1.0 / 10 ** param['qty_decimals'], qty), param['qty_decimals']),
              float(param['max_qty_per_order']))
    if qty > 0 and price > 0:
        self.logger.info('put self-trade %s %s %s %s %s',
                         symbol, price, qty, top_bid, top_ask)
        # the close of minute N must equals to the open of minute N+1
        if current_minute != pre_st_status['minute']:
            # a new minute is started, so we need to use the previous trade price
            price = pre_st_status['price']

        pre_st_status['minute'] = current_minute
        price = max(min(price, top_ask), top_bid)
        pre_st_status['price'] = price
        if qty == pre_st_status['qty']:
            qty *= 1.0001
        pre_st_status['qty'] = qty
        res = jc_safe_self_trade(param['api_key'], param['api_secret'], symbol,
                           'BUY' if rand_val % 2 == 0 else 'SELL',
                           str(round(price, price_decimals) if price_decimals else int(price)),
                           str(round(qty, param['qty_decimals']) if param['qty_decimals'] else int(qty)),
                           self.app_name)
        self.logger.info(res)
        return True
    return False


