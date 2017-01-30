import csv
import logging
from logutils import BraceMessage as __
from data.equity import Stock


class StockExchangeFactory:

    @staticmethod
    def create_stock_exchange(name):
        switch = {
            'SHA': SHAStockExchange
        }
        return switch.get(name, None)()


class StockExchange:

    def __init__(self):
        self.stock_by_symbol = {}

    def stock_name(self, symbol):
        return self.stock_by_symbol[symbol].name


class SHAStockExchange(StockExchange):

    def load(self):
        with open('SHA.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                symbol = row['Code']
                name = row['Short Name(In Chinese)']
                self.stock_by_symbol[symbol] = Stock(symbol, name)

    def stock_name(self, symbol):
        if symbol == '000001':
            return '上证综指'
        else:
            return super(SHAStockExchange, self).stock_name(symbol)
