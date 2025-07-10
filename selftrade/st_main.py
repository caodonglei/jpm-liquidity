""" JumpMaker Self-Trader
"""
import os
import sys
import time
import asyncio
import random

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from common.utils.log_utils import create_logger
from common.configer import Configer
from selftrade.selftrader import self_trade


LOGGER = create_logger(CURR_DIR, "jpm_selftrade.log", 'JPM_SELFTRADE', backup_cnt=10)


def gen_cached_random_number(size: int):
    # cached random number pool: range 0..100
    _random_index = 0
    _random_values = random.shuffle(list(range(100)))[:size]
    while 1:
        if _random_index >= size:
            _random_index = 0
        yield _random_values[_random_index]
        _random_index += 1


async def main():
    """ main workflow of self-trader
    """
    if len(sys.argv) != 2:
        print('python3 %s <APP_NAME>' % sys.argv[0])
        return

    app_name = sys.argv[1]
    configer = Configer(app_name)
    config = configer.get_config()
    LOGGER.info('start JPM self-trade with config: %s', config)

    # previous operation timestamp
    _last_operating_ts = {}
    # previous self trade price and timestamp
    _prev_st = {}
    # random int generator
    _randint = gen_cached_random_number(97)

    while 1:
        if configer.has_update():
            config = configer.get_config()
            LOGGER.info('update config: %s', conf)

        tasks = []
        ts = time.time()
        for symbol, param in config['TOKENS'].items():
            # check self-trade frequency
            if _last_operating_ts.get(symbol, 0) + param['interval'] > ts:
                continue

            tasks.append(asyncio.create_task(self_trade(symbol, param, next(_randint))))
            _last_operating_ts[symbol] = ts

        if tasks:
            await asyncio.gather(*tasks)
        else:
            await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(main())
