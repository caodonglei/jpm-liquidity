from env import DATA_REDIS


### Constants
EXCHANGE_BN  = 'Binance'
EXCHANGE_OKX = 'OKX'
EXCHANGE_JU  = 'Jucoin'

API_REDIS = 'redis'
API_RESTFUL = 'restful'

### Configer
CONF_TYPE = 'LOCAL_FILE'	# LOCAL_FILE or REDIS


### Quoter
MAIN_QUOTE_EXCHANGE = EXCHANGE_BN
BACKUP_QUOTE_EXCHANGE = ''
QUOTE_SOURCE = DB_REDIS


### Self-Trade strategies
ST_STRATEGY = ['random_quantity']