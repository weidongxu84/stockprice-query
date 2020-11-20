import asyncio
import yaml
from exchange.exchange import StockExchangeFactory
from data_source.history_ds import HistoryDataSource
from data_source.realtime_ds import RealTimeYahooDataSource
from analysis.analysis import SimpleTrendAnalysis
import logging

logger = logging.getLogger(__name__)


@asyncio.coroutine
def run(loop, watchlist_filename, interval):
    with open(watchlist_filename, 'r', encoding='utf-8') as f:
        watch_list = yaml.safe_load(f)
        exchange_name = watch_list['exchange']
        exchange = StockExchangeFactory.create_stock_exchange(exchange_name)
        exchange.load()

        stocks = watch_list['watch']
        symbols = [str(stock['symbol']) for stock in stocks]

        history = HistoryDataSource(exchange_name, symbols)
        history.load()

        ds = RealTimeYahooDataSource(exchange_name, symbols)

        analysis = SimpleTrendAnalysis(exchange)

    try:
        while True:
            quotes = ds.get_tick()
            analysis.update(history, quotes)
            history.add_latest(quotes)
            yield from asyncio.sleep(interval)
    except asyncio.CancelledError:
        pass
    finally:
        history.save()
