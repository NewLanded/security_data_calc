"""
上穿布林线下线后, 第一天跌, 那么后5天会赚的几率
上穿布林线下线后, 第一天涨幅较小(<=2%), 那么后5天会赚的几率
上穿布林线下线后, 第一天涨幅较大(>2%), 那么后5天会赚的几率
"""

import datetime
import math

import pandas as pd
import talib as ta
from sklearn.linear_model import LinearRegression

from util.util_base.date_util import get_date_range, convert_datetime_to_str
from util.util_data.date import Date
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def get_std(security_point_data):
    std = ta.STDDEV(security_point_data["close"], timeperiod=15, nbdev=2)
    return std


def get_slope(security_point_data):
    def _get_first_point_multiplying_power_by_1(point):
        return point / 100

    def _get_point_list(sma_data, period=6):
        sma_data = sma_data[-period:]
        first_point = sma_data[0]
        multiplying_power = _get_first_point_multiplying_power_by_1(first_point)

        point_list = []
        for index in range(0, len(sma_data)):
            if not math.isnan(sma_data[index]) and not math.isnan(first_point):
                point_list.append([index, sma_data[index] / multiplying_power])
        return point_list

    def _calc_slope(point_list):
        if not point_list:
            return float("nan")

        point_df = pd.DataFrame(point_list, columns=["abscissa", "ordinate"])
        abscissa = point_df["abscissa"]
        ordinate = point_df["ordinate"]

        abscissa = abscissa.values.reshape(-1, 1)
        ordinate = ordinate.values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(abscissa, ordinate)
        slope = model.coef_
        return slope[0][0]

    sma_data_10 = ta.MA(security_point_data["close"], timeperiod=10, matype=0)
    sma_data_30 = ta.MA(security_point_data["close"], timeperiod=30, matype=0)

    point_list_sma10 = _get_point_list(sma_data_10)
    point_list_sma30 = _get_point_list(sma_data_30)

    slope_10 = _calc_slope(point_list_sma10)
    slope_30 = _calc_slope(point_list_sma30)
    return slope_10, slope_30


def get_bband(security_point_data):
    upperband, middleband, lowerband = ta.BBANDS(security_point_data["close"], timeperiod=15, nbdevup=2, nbdevdn=2, matype=0)
    return upperband, middleband, lowerband


def calc_bs_data(security_point_data):
    if security_point_data.iloc[-1]["close"] > 40:
        return False

    std = get_std(security_point_data)
    slope_10, slope_30 = get_slope(security_point_data)
    upperband, middleband, lowerband = get_bband(security_point_data)

    if security_point_data.iloc[-1]["close"] < lowerband.iloc[-1] * 1.01 and std.iloc[-1] / middleband.iloc[-1] > 0.04 and slope_30 >= 0:
        return True
    else:
        return False


def start(date_now, result):
    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
        # ts_codes = ['002062.SZ', '002565.SZ']
        for ts_code in ts_codes:
            try:
                start_date, end_date = date_now - datetime.timedelta(days=90), date_now
                security_point_data = SecurityData().get_qfq_security_point_data(ts_code, start_date, end_date)
                buy_flag = calc_bs_data(security_point_data)

                if buy_flag is True:
                    security_point_data = SecurityData().get_qfq_security_point_data(ts_code, end_date, end_date + datetime.timedelta(days=25))
                    result_now = pd.DataFrame(
                        [security_point_data.iloc[0], security_point_data.iloc[1], security_point_data.iloc[2], security_point_data.iloc[5], security_point_data.iloc[10]],
                        index=[['next_0_day', 'next_1_day', 'next_2_day', 'next_5_day', 'next_10_day'], [1, 1, 1, 1, 1]])
                    result_now = result_now.unstack(level=0)
                    # print(result_now)
                    result.append(result_now)
                    # result = pd.concat([result, result_now])

            except Exception as e:
                pass
    return result


if __name__ == "__main__":
    result = []
    for date in get_date_range(datetime.datetime(2016, 5, 3), datetime.datetime(2019, 1, 31)):
        print(date, datetime.datetime.now())
        # with open('./date_now_log', "w") as f:
        #     f.write(convert_datetime_to_str(date))
        start(date, result)
        # break
    result = pd.concat(result)

    result.to_csv('./penetrate_lower_bband.csv')
    # result = pd.read_csv('./penetrate_lower_bband.csv')
    print(result[['close', 'open', 'pct_chg']])
