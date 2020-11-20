from data.equity import *
import os, operator
import logging
import csv

logger = logging.getLogger(__name__)


class HistoryDataSource:

    def __init__(self, exchange, symbols, repository_dir='.'):
        self.exchange = exchange
        self.symbols = symbols
        self.repository_dir = repository_dir
        self.history_by_symbol = {symbol: [] for symbol in symbols}

    def add_latest(self, quotes):
        for quote in quotes:
            if quote.symbol in self.symbols:
                quotes = self.history_by_symbol[quote.symbol]
                if not quotes or not quotes[-1] == quote:
                    self.history_by_symbol[quote.symbol].append(quote)

    def contains(self, quote):
        if quote.symbol in self.symbols:
            quotes = self.history_by_symbol[quote.symbol]
            return quotes and quote in quotes

    def partition_by_day(self):
        return {symbol: partition_by_day(self.history_by_symbol[symbol]) for symbol in self.symbols}

    def load(self):
        exchange_dir = os.path.join(self.repository_dir, self.exchange)
        if os.path.isdir(exchange_dir):
            for dir1 in os.listdir(exchange_dir):
                equity_dir = os.path.join(exchange_dir, dir1)
                symbol = dir1
                if os.path.isdir(equity_dir) and symbol in self.symbols:
                    for file1 in os.listdir(equity_dir):
                        filename, file_ext = os.path.splitext(file1)
                        if file_ext == '.csv':
                            self.history_by_symbol[symbol].extend(load_csv(os.path.join(equity_dir, file1)))
        self.sort()

    def save(self):
        self.sort()
        exchange_dir = os.path.join(self.repository_dir, self.exchange)
        if not os.path.isdir(exchange_dir):
            os.mkdir(exchange_dir)
        for symbol in self.symbols:
            equity_dir = os.path.join(exchange_dir, symbol)
            if not os.path.isdir(equity_dir):
                os.mkdir(equity_dir)
            history_by_month = partition_by_month(self.history_by_symbol[symbol])
            for key, quotes in history_by_month.items():
                save_csv(os.path.join(equity_dir, key + '.csv'), quotes)

    def sort(self):
        for h in self.history_by_symbol.values():
            h.sort(key=operator.attrgetter('ts'))


def load_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        quotes = [StockQuote(row) for row in reader]
    return quotes


def save_csv(filename, quotes):
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=StockQuote._attr, delimiter=',')
        writer.writeheader()
        for quote in quotes:
            writer.writerow(quote.to_dict())


def partition_by_month(quotes):
    partition = {}
    for quote in quotes:
        ts = quote.datetime()
        date = ts.date().strftime('%Y-%m')
        if date not in partition:
            partition[date] = []
        partition[date].append(quote)
    return partition


def partition_by_day(quotes):
    partition = {}
    for quote in quotes:
        ts = quote.datetime()
        date = ts.date().strftime('%Y-%m-%d')
        if date not in partition:
            partition[date] = []
        partition[date].append(quote)
    return partition
