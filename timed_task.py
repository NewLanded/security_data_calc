import logging
import threading
import time
from logging import handlers

import schedule

from strategy.buy import strategy_1

logger = logging.getLogger('/home/stock/app/security_data_calc/timed_task.log')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def job1():
    logger.info('starting fluctuation_tactics_1')
    try:
        strategy_1.start()
    except Exception as e:
        logger.error('error fluctuation_tactics_1, error = {0}'.format(str(e)))
    logger.info('finished fluctuation_tactics_1')


def job1_task():
    threading.Thread(target=job1).start()


def run():
    schedule.every().day.at("1:00").do(job1_task)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
