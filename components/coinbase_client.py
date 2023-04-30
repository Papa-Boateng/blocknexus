import config
from coinbase.wallet.client import Client

#initialize coinbase
cb_client_init = Client(config.coinbase_api_key, config.coinbase_api_secret)

def type_payment(data):  
    _type_payment = {}
    accounts = cb_client_init.get_accounts()
    supported_currency = config.currency
    for itm in supported_currency:
        for x in accounts["data"]:
            if x['currency']==itm:
                _type_payment[itm]=x['id']
    return _type_payment[data]