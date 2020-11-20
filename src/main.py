import logging
import logging.config
import asyncio
import yaml
import task.realtime_monitor as rt_monitor

logger = logging.getLogger(__name__)


def main():
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(rt_monitor.run(loop, 'watchlist.yaml', interval=5*60))
    ]
    logger.debug(f'async tasks {tasks}')
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        logger.debug('interrupt, cancel all tasks')
        for task in asyncio.all_tasks(loop):
            task.cancel()
    finally:
        tasks = asyncio.all_tasks(loop)
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()


if __name__ == '__main__':
    main()
