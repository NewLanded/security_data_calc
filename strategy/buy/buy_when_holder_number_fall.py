"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime

from util.util_data.date import Date
from util.util_data.market_data import MarketData
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def buy(security_point_data, holder_number_data):
    holder_number_data = [i[3] for i in holder_number_data]
    holder_number_data = holder_number_data[-3:]
    if holder_number_data and holder_number_data == sorted(holder_number_data, reverse=True):
        if sum([security_point_data["close"].iloc[-1], security_point_data["close"].iloc[-2], security_point_data["close"].iloc[-3]]) > sum([security_point_data["close"].iloc[-7],
                                                                                                                                             security_point_data["close"].iloc[-8],
                                                                                                                                             security_point_data["close"].iloc[
                                                                                                                                                 -9]]):
            return True

    return False


def sell(data):
    """
    持仓 >= 3 天

    或者

    损益超过2%
    """
    pass


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
        start_date, end_date = date_now - datetime.timedelta(days=30), date_now
        for ts_code in ts_codes:
            try:
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                holder_number_data = MarketData().get_holder_number_data(ts_code, end_date - datetime.timedelta(days=365), end_date)
                buy_flag = buy(security_point_data, holder_number_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "buy_when_holder_number_fall", "B", date_now)
            except Exception as e:
                pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2016, 12, 7), datetime.datetime(2016, 5, 8)
    start(start_date)
