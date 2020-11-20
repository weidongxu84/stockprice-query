from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StockQuote:

    _attr = {'symbol', 'ts', 'price'}

    def __init__(self, *args, **kwargs):
        self.symbol = None
        self.price = None
        self.ts = None
        for d in args:
            for key, value in d.items():
                if key in StockQuote._attr:
                    setattr(self, key, value)
        for key in kwargs:
            if key in StockQuote._attr:
                setattr(self, key, kwargs[key])
        if self.price:
            if isinstance(self.price, str):
                self.price = self.price.replace(',', '')
                self.price = float(self.price)

    def __repr__(self):
        return '{0!s}{1!r}'.format(self.__class__, self.__dict__)

    def __eq__(self, other):
        return self.symbol == other.symbol and self.ts == other.ts

    def to_dict(self):
        d = {}
        for attr in StockQuote._attr:
            d[attr] = getattr(self, attr)
        return d

    def datetime(self):
        return datetime.strptime(self.ts, '%Y-%m-%dT%H:%M:%SZ')


class Stock:

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
