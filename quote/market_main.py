from jpm_config import (
    EXCHANGE_BN,
    EXCHANGE_OKX,
    EXCHANGE_JU,
    MAIN_QUOTE_EXCHANGE,
    BACKUP_QUOTE_EXCHANGE
)


MARKET_CLIENT = get_market_client(MAIN_QUOTE_EXCHANGE)
BACKUP_CLIENT = get_market_client(BACKUP_QUOTE_EXCHANGE)

def get_market_client(exchange: str):
    """ create market client subscribing public websocket
    """
    if exchange == EXCHANGE_BN:
        
