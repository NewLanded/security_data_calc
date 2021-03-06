import datetime

from util.util_base.date_util import convert_pd_timestamp_to_datetime
from util.util_data.date import Date
from util.util_data.dml import Dml
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData

"""
数据使用涨跌幅
不能连续跌, 按天, 比前一天涨的要大于40%
至少有20%的次数涨幅超过1.5%
期间不能有涨停, 避免这种风险
最后5天跌的比涨的多
"""


def calc_point_data(security_point_data):
    date_pct_chg_list = []
    for trade_date, row in security_point_data.iterrows():
        date_pct_chg_list.append([convert_pd_timestamp_to_datetime(trade_date), row["pct_chg"]])

    date_pct_chg_list.sort(key=lambda x: x[0])
    pct_chg_list = [i[1] for i in date_pct_chg_list]

    raise_percent_list, raise_list, daily_limit = [], [], []
    for pct_chg in pct_chg_list:
        if pct_chg > 0:
            raise_list.append(pct_chg)

        if pct_chg > 0.015:
            raise_percent_list.append(pct_chg)

        if pct_chg >= 0.08:
            daily_limit.append(pct_chg)

    last_days_sum_pct_chg = sum(pct_chg_list[-5:])
    if len(raise_list) / len(pct_chg_list) > 0.4 and len(raise_percent_list) / len(pct_chg_list) > 0.2 and not daily_limit \
            and last_days_sum_pct_chg < 0:
        buy_flag = True
    else:
        buy_flag = False

    return buy_flag


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(
            ["tactics_2_status", "tactics_3_status", "tactics_4_status", "tactics_5_status"])
        for ts_code in ts_codes:
            try:
                start_date, end_date = date_now - datetime.timedelta(days=90), date_now
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                buy_flag = calc_point_data(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "buy_strategy_1", "B", date_now)
            except Exception as e:
                Dml().store_failed_message(ts_code, "buy_strategy_1", str(e), date_now)


if __name__ == "__main__":
    start(date_now=datetime.datetime(2018, 10, 24))
