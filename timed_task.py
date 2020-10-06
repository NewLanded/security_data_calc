import logging
import time
from logging import handlers

import schedule

from strategy.buy import buy_when_holder_number_fall, future_bs_when_trend_start, buy_when_30_days_change_to_up

logger = logging.getLogger('/home/stock/app/security_data_calc/timed_task.log')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def stock_job():
    logger.info('starting buy_when_holder_number_fall')
    try:
        buy_when_holder_number_fall.start()
    except Exception as e:
        logger.error('error buy_when_holder_number_fall, error = {0}'.format(str(e)))
    logger.info('finished buy_when_holder_number_fall')

    logger.info('starting buy_when_30_days_change_to_up')
    try:
        buy_when_30_days_change_to_up.start()
    except Exception as e:
        logger.error('error buy_when_30_days_change_to_up, error = {0}'.format(str(e)))
    logger.info('finished buy_when_30_days_change_to_up')


def future_job():
    logger.info('starting future_bs_when_trend_start')
    try:
        future_bs_when_trend_start.start()
    except Exception as e:
        logger.error('error future_bs_when_trend_start, error = {0}'.format(str(e)))
    logger.info('finished future_bs_when_trend_start')


def run():
    schedule.every().day.at("19:40").do(stock_job)
    schedule.every().day.at("21:20").do(future_job)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
