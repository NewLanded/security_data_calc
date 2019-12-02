import logging
import time
from logging import handlers

import schedule

from strategy.buy import buy_when_holder_number_fall, future_bs_when_trend_start

logger = logging.getLogger('/home/stock/app/security_data_calc/timed_task.log')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def job1():
    # logger.info('starting bband')
    # try:
    #     bband.start()
    # except Exception as e:
    #     logger.error('error bband, error = {0}'.format(str(e)))
    # logger.info('finished bband')

    # logger.info('starting sma_sloop')
    # try:
    #     sma_sloop.start()
    # except Exception as e:
    #     logger.error('error sma_sloop, error = {0}'.format(str(e)))
    # logger.info('finished sma_sloop')
    #
    # logger.info('starting buy_when_fall')
    # try:
    #     buy_when_fall.start()
    # except Exception as e:
    #     logger.error('error buy_when_fall, error = {0}'.format(str(e)))
    # logger.info('finished buy_when_fall')

    # logger.info('starting avg_point_5_penetrate_10')
    # try:
    #     avg_point_5_penetrate_10.start()
    # except Exception as e:
    #     logger.error('error avg_point_5_penetrate_10, error = {0}'.format(str(e)))
    # logger.info('finished avg_point_5_penetrate_10')

    logger.info('starting future_bs_when_trend_start')
    try:
        future_bs_when_trend_start.start()
    except Exception as e:
        logger.error('error future_bs_when_trend_start, error = {0}'.format(str(e)))
    logger.info('finished future_bs_when_trend_start')

    logger.info('starting buy_when_holder_number_fall')
    try:
        buy_when_holder_number_fall.start()
    except Exception as e:
        logger.error('error buy_when_holder_number_fall, error = {0}'.format(str(e)))
    logger.info('finished buy_when_holder_number_fall')


def run():
    schedule.every().day.at("19:20").do(job1)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
