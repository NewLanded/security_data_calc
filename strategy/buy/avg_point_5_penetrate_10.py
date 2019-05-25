import datetime

import talib as ta

from util.util_data.date import Date
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def calc_bs_data(security_point_data):
    if security_point_data.iloc[-1]["close"] > 40:
        return False

    sma_data_5 = ta.MA(security_point_data["close"], timeperiod=7, matype=0)
    sma_data_10 = ta.MA(security_point_data["close"], timeperiod=14, matype=0)

    if sma_data_5[-1] > sma_data_10[-1]:
        return True
    else:
        return False


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
        for ts_code in ts_codes:
            try:
                start_date, end_date = date_now - datetime.timedelta(days=30), date_now
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                buy_flag = calc_bs_data(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "a_p_5_p_10", "B", date_now)
            except Exception as e:
                pass


if __name__ == "__main__":
    # 没屌用
    start(datetime.datetime(2019, 5, 20))
