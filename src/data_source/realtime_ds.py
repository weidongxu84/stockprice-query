from data.equity import *
import googlefinance
import logging
from logutils import BraceMessage as __

logger = logging.getLogger(__name__)


class RealTimeDataSource:

    def __init__(self, exchange, symbols):
        self.exchange = exchange
        self.symbols = symbols

    def get_tick(self):
        pass


class RealTimeGoogleDataSource(RealTimeDataSource):

    def get_tick(self):
        symbols = [self.exchange + ':' + str(symbol) for symbol in self.symbols]
        quotes = googlefinance.getQuotes(symbols)
        logger.debug(__('quotes from Google: {}', quotes))
        return [RealTimeGoogleDataSource.convert_from_google_quote(quote) for quote in quotes]

    @staticmethod
    def convert_from_google_quote(quote):
        return StockQuote(symbol=quote['StockSymbol'], price=quote['LastTradePrice'], ts=quote['LastTradeDateTime'])
