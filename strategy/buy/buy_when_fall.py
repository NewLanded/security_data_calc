"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime

from util.util_data.date import Date
from util.util_data.result import Result
from util.util_data.security_data import SecurityData


def buy(data):
    if data["close"].iloc[-1] < data["close"].iloc[-2] < data["close"].iloc[-3]:
        buy_flag = True
    else:
        buy_flag = False

    """
    得第二天涨了再买, 因为没有实时数据, 所以只能每天肉眼看
    """

    return buy_flag


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
        start_date, end_date = date_now - datetime.timedelta(days=50), date_now
        for ts_code in ['600406.SH', '600298.SH', '000001.SZ', '600346.SH', '600104.SH', '601088.SH', '600028.SH', '600340.SH', '600031.SH', '600967.SH',
                        '002216.SZ', '600498.SH', '600176.SH', '002487.SZ', '600857.SH', '603959.SH', '002242.SZ', '603160.SH']:
            try:
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                buy_flag = buy(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "buy_when_fall", "B", date_now)
            except Exception as e:
                pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2016, 12, 7), datetime.datetime(2016, 5, 8)
    start(start_date)
