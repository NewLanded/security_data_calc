"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime

from util.util_data.date import Date
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData
import talib as ta


def buy(security_point_data):
    sma_data_30 = ta.MA(security_point_data.iloc[-60:]["close"], timeperiod=30, matype=0)

    if sma_data_30.iloc[-3] <= sma_data_30.iloc[-4] and sma_data_30.iloc[-3] <= sma_data_30.iloc[-2] <= sma_data_30.iloc[-1]:
        avg_point = security_point_data["close"].sum() / len(security_point_data["close"])
        if sma_data_30.iloc[-1] < avg_point * 1.2:
            return True

    return False


def sell(data):
    """
    """
    pass


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status", "tactics_7_status"])
        start_date, end_date = date_now - datetime.timedelta(days=1000), date_now
        for ts_code in ts_codes:
            try:
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                buy_flag = buy(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "buy_when_30_days_change_to_up", "B", date_now)
            except Exception as e:
                pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2020, 9, 30), datetime.datetime(2016, 5, 8)
    start(start_date)
