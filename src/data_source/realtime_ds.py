from data.equity import *
from datetime import datetime
import requests
import json
# import googlefinance
import logging

logger = logging.getLogger(__name__)


class RealTimeDataSource:

    def __init__(self, exchange, symbols):
        self.exchange = exchange
        self.symbols = symbols

    def get_tick(self):
        pass


# class RealTimeGoogleDataSource(RealTimeDataSource):
#
#     def get_tick(self):
#         symbols = [self.exchange + ':' + str(symbol) for symbol in self.symbols]
#         quotes = googlefinance.getQuotes(symbols)
#         logger.debug(f'quotes from Google: {quotes}')
#         return [RealTimeGoogleDataSource.convert_from_google_quote(quote) for quote in quotes]
#
#     @staticmethod
#     def convert_from_google_quote(quote):
#         return StockQuote(symbol=quote['StockSymbol'],
#                           price=quote['LastTradePrice'],
#                           ts=quote['LastTradeDateTime'])


class RealTimeYahooDataSource(RealTimeDataSource):

    def __init__(self, exchange, symbols):
        super(RealTimeYahooDataSource, self).__init__(exchange, symbols)
        if self.exchange == 'SHA':
            self.exchange = 'SS'

    def get_tick(self):
        symbols = [str(symbol) + '.' + self.exchange for symbol in self.symbols]
        symbols_segment = ','.join(symbols)
        r = requests.get('https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields=symbol,longName,shortName,priceHint,regularMarketPrice,regularMarketChange,regularMarketChangePercent,currency,regularMarketTime,regularMarketVolume,quantity,averageDailyVolume3Month,regularMarketDayHigh,regularMarketDayLow,regularMarketPrice,regularMarketOpen,fiftyTwoWeekHigh,fiftyTwoWeekLow,regularMarketPrice,regularMarketOpen,sparkline,marketCap&symbols=' + symbols_segment + '&formatted=false')
        content = json.loads(r.text)
        logger.debug(f'quotes from Yahoo: {content}')
        quotes = RealTimeYahooDataSource.convert_from_yahoo_json(content)
        return quotes

    @staticmethod
    def convert_from_yahoo_json(json):
        return [StockQuote(symbol=RealTimeYahooDataSource.convert_symbol(quote['symbol']),
                           price=quote['regularMarketPrice'],
                           ts=RealTimeYahooDataSource.convert_ts(quote['regularMarketTime'] + quote['gmtOffSetMilliseconds'] / 1000))
                for quote in json['quoteResponse']['result']]

    @staticmethod
    def convert_symbol(symbol):
        return symbol.split('.')[0]

    @staticmethod
    def convert_ts(ts):
        return datetime.utcfromtimestamp(ts).isoformat() + 'Z'
