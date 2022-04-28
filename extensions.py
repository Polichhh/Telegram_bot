import requests
import json
from config import keys


class ConvExcep(Exception):
    pass

class CripConverter:
    @staticmethod
    def get_price (base: str, quote: str, amount: str):

        if base == quote:
            raise ConvExcep(f'Нельзя переводить {base} в {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvExcep(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvExcep(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvExcep(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = json.loads(r.content)[keys[quote]]

        return total*amount
