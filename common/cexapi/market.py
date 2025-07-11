from jpm_config import QUOTE_SOURCE, API_REDIS, API_RESTFUL
from common.utils import DATA_REDIS_CLIENT

class MarketProxy:
    """ load market data, including depth, ticker
    """
    def __init__(self):
        if QUOTE_SOURCE == API_REDIS:
            self.source = DATA_REDIS_CLIENT
        elif QUOTE_SOURCE == API_RESTFUL:
            self.source = REST_CLIENT
        else:
            raise Excpetion("Invalid Market API")

    def get_ticker(self, exchange: str, symbol: str) -> dict:
        """ get latest ticker
        """
        return self.source.get_dict(f'{exchange}{symbol}')

    def get_tickers(self, exchange: str, symbols: list = None) -> dict:
        """ get latest ticker
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.source.get_dict(f'{exchange}{symbol}')
        return results


MAEKET_PROXY = MarketProxy()

def get_ticker(self, exchange: str, symbol: str) -> dict:
    """ get latest ticker
    """
    MAEKET_PROXY.get_ticker(exchange, symbol)

def get_tickers(self, exchange: str, symbols: list = None) -> dict:
    """ get latest tickers of multiple symbols
    """
    MAEKET_PROXY.get_tickers(exchange, symbols)