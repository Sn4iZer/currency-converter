from .api import ExchangeClient
_singleton = ExchangeClient()

def currencies():
    return sorted(_singleton.get_rates().keys())

def exchange(from_cur:str, to_cur:str, amount:float|int):
    return _singleton.convert(from_cur.upper(), to_cur.upper(), amount)