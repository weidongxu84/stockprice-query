from datetime import datetime
from datetime import timedelta
import logging
from logutils import BraceMessage as __

logger = logging.getLogger(__name__)


class Analysis:

    def __init__(self, exchange):
        self.exchange = exchange

    def update(self, history, quote):
        pass


class SimpleTrendAnalysis(Analysis):

    def update(self, history, quotes):
        close_quote_by_symbol = SimpleTrendAnalysis.close_quotes_last_day(history, quotes)
        quote_by_symbol = {quote.symbol: quote for quote in quotes}
        for close_quote in close_quote_by_symbol.values():
            symbol = close_quote.symbol
            price_delta = quote_by_symbol[symbol].price - close_quote_by_symbol[symbol].price
            percentage = price_delta / close_quote_by_symbol[symbol].price

            gesture = ''
            if percentage > 5:
                gesture = '▲▲▲'
            elif percentage > 2:
                gesture = '▲▲'
            elif percentage > 1:
                gesture = '▲'
            elif percentage < -1:
                gesture = '▼'
            elif percentage < -2:
                gesture = '▼▼'
            elif percentage < -5:
                gesture = '▼▼▼'

            print('{:s} {:8s} {:8.2f} {:+7.2f} {:+5.1f}% {:3s}'
                  .format(symbol, self.exchange.stock_name(symbol),
                          quote_by_symbol[symbol].price, price_delta,
                          percentage * 100, gesture))

    @staticmethod
    def close_quotes_last_day(history, quotes):
        partition_by_day = history.partition_by_day()
        close_quote_by_symbol = {}
        for quote in quotes:
            symbol = quote.symbol
            if not history.contains(quote) and not symbol in close_quote_by_symbol:
                partition = partition_by_day[symbol]
                today = datetime.today()
                for num_days in range(1, 30):   # check up to a month
                    day = today - timedelta(days=num_days)
                    day_str = day.strftime('%Y-%m-%d')
                    if day_str in partition and partition[day_str]:
                        close_quote_by_symbol[symbol] = partition[day_str][-1]
                        break
        return close_quote_by_symbol
