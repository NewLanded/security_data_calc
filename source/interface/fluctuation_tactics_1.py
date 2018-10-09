import datetime

from source.util.util_data.Security import Security
from source.util.util_data.date import Date
from source.util.util_data.dml import Dml
from source.util.util_data.result import Result
from source.util.util_data.security_data import SecurityData

"""
数据使用涨跌幅
不能连续跌, 按天, 比前一天涨的要大于40%
至少有20%的次数涨幅超过1.5%
期间不能有涨停, 避免这种风险
最后5天跌的比涨的多
"""


def calc_point_data(security_point_data):
    date_pct_change_list = [[trade_date, value["pct_change"]] for trade_date, value in security_point_data.items()]
    date_pct_change_list.sort(key=lambda x: x[0])
    pct_change_list = [i[1] for i in date_pct_change_list]

    raise_percent_list, raise_list, daily_limit = [], [], []
    for pct_change in pct_change_list:
        if pct_change > 0:
            raise_list.append(pct_change)

        if pct_change > 0.015:
            raise_percent_list.append(pct_change)

        if pct_change >= 0.08:
            daily_limit.append(pct_change)

    b_point, s_point, quantity = 0, 0, 0
    last_days_sum_pct_change = sum(pct_change_list[-5:])
    if len(raise_list) / len(pct_change_list) > 0.4 and len(raise_percent_list) / len(pct_change_list) > 0.2 and not daily_limit \
            and last_days_sum_pct_change < 0:
        pass_flag = True
    else:
        pass_flag = False

    return b_point, s_point, quantity, pass_flag


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code(["tactics_2_status", "tactics_3_status", "tactics_4_status", "tactics_5_status"])
        for ts_code in ts_codes:
            try:
                start_date, end_date = date_now - datetime.timedelta(days=90), date_now
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                b_point, s_point, quantity, pass_flag = calc_point_data(security_point_data)

                if pass_flag is True:
                    code_info = Security().get_code_info_by_ts_code(ts_code)
                    Result().insert_result_data(code_info["code"], b_point, s_point, quantity, tactics_code="fluctuation_tactics_1")
            except Exception as e:
                Dml().store_failed_message(ts_code, "fluctuation_tactics_1", str(e), date_now)


if __name__ == "__main__":
    start()
