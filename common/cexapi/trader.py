
class Account:
	__slots__ = ('_base_url', 'api_key', 'api_secret')
	def __init__(self, base_url: str, api_key: str, api_secret: str):
		self._base_url = base_url
		self._api_key = api_key
		self._api_secret = api_secret

class Order:

	def __init__(self, )

def new_order(account: Account, symbol: str, price: str, qty: str, side: str, type: str = 'LIMIT', tif: str = 'GTC'):
	""" make a new order
	""" 

def cancel_order(account: Account, order_id: str) -> dict:
	""" cancel an order
	"""

def order_status(account: Account, order_id: str) -> dict:
	""" check the status of an order
	"""

def open_orders(account: Account, symbol: str) -> dict:
	""" show open orders
	"""

def mock_trade(account: Account, symbol: str, pric: str, qty: str, side: str):
	""" mock a self-trade
	"""