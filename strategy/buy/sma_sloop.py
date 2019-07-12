"""
当点位下跌一段时间或一定百分比后买入
"""
import datetime

import talib as ta

from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def buy(data):
    sma_data = ta.MA(data["close"], timeperiod=5, matype=0)
    slope = ta.LINEARREG_SLOPE(sma_data, timeperiod=11)

    if slope.iloc[-2] < 0 and slope.iloc[-1] > 0:
        buy_flag = True
    else:
        buy_flag = False

    return buy_flag


def sell(data):
    sma_data = ta.MA(data["close"], timeperiod=5, matype=0)
    slope = ta.LINEARREG_SLOPE(sma_data, timeperiod=11)

    if slope.iloc[-2] > 0 and slope.iloc[-1] < 0:
        sell_flag = True
    elif (data["close"].iloc[-1] - max(data["close"].iloc[-40:])) / max(data["close"].iloc[-40:]) > -0.02:
        if data["close"].iloc[-1] < data["close"].iloc[-2] < data["close"].iloc[-3] < data["close"].iloc[-4]:
            sell_flag = True
        else:
            sell_flag = False
    else:
        sell_flag = False

    return sell_flag


def start(date_now=None):
    if date_now is None:
        date_now = datetime.datetime.now()
        date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    start_date, end_date = date_now - datetime.timedelta(days=50), date_now

    ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
    for ts_code in ts_codes:
        try:
            security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
            buy_flag = buy(security_point_data)

            if buy_flag is True:
                Result().insert_strategy_result_data(ts_code, "sma_sloop", "B", date_now)
        except Exception as e:
            pass

    ts_codes = Result().get_hold_data('sma_sloop')
    for ts_code in ts_codes:
        try:
            security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
            sell_flag = sell(security_point_data)

            if sell_flag is True:
                Result().insert_strategy_result_data(ts_code, "sma_sloop", "S", date_now)
        except Exception as e:
            pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2016, 12, 6), datetime.datetime(2016, 5, 8)
    start(start_date)
