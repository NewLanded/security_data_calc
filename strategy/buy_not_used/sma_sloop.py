"""
当点位下跌一段时间或一定百分比后买入
"""
import datetime

import talib as ta

from util.util_data.date import Date
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
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        start_date, end_date = date_now - datetime.timedelta(days=50), date_now
        # ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
        # for ts_code in ts_codes:
        for ts_code in ['600481.SH', '601699.SH', '002061.SZ', '002424.SZ', '600436.SH', '002796.SZ', '600810.SH', '000510.SZ', '601600.SH', '600218.SH', '002414.SZ', '002302.SZ', '000877.SZ', '002451.SZ', '600355.SH', '600760.SH', '600679.SH', '000656.SZ', '600148.SH', '000935.SZ', '002208.SZ', '600516.SH', '002602.SZ', '002696.SZ', '002050.SZ', '000557.SZ', '002460.SZ', '600230.SH', '002877.SZ', '002243.SZ', '600235.SH', '000403.SZ', '000576.SZ', '600997.SH', '600581.SH', '600690.SH', '600507.SH', '600019.SH', '000513.SZ', '002346.SZ', '600966.SH', '000612.SZ', '000966.SZ', '600438.SH', '002382.SZ', '600388.SH', '603993.SH', '601636.SH', '000898.SZ', '601028.SH', '000739.SZ', '002258.SZ', '002760.SZ', '603288.SH', '600782.SH', '600720.SH', '002708.SZ', '603027.SH', '000785.SZ', '600141.SH', '000001.SZ', '600783.SH', '600519.SH', '002072.SZ', '600280.SH', '600874.SH', '603859.SH', '601003.SH', '601918.SH', '000732.SZ', '600083.SH', '601933.SH', '600425.SH', '002034.SZ', '600346.SH', '000528.SZ', '601360.SH', '002679.SZ', '601318.SH', '002124.SZ', '603444.SH', '002606.SZ', '002157.SZ', '600596.SH', '600761.SH', '002408.SZ', '600815.SH', '603180.SH', '000725.SZ', '600641.SH', '000830.SZ', '600128.SH', '002056.SZ', '600196.SH', '600104.SH', '600080.SH', '002545.SZ', '601012.SH', '600776.SH', '000717.SZ', '000690.SZ', '600053.SH', '601100.SH', '002415.SZ']:
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
