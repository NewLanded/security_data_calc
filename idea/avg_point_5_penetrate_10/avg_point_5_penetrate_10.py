import datetime

import pandas as pd
import talib as ta

from util.util_base.date_util import get_date_range, convert_datetime_to_str
from util.util_data.date import Date
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def calc_bs_data(security_point_data):
    sma_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=0)
    sma_data_10 = ta.MA(security_point_data["close"], timeperiod=10, matype=0)

    if sma_data_5 > sma_data_10:
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
                    previous_work_day = Date().get_previous_workday(end_date)
                    previous_2_work_day = Date().get_previous_workday(previous_work_day)
                    security_point_data = SecurityData().get_qfq_security_point_data(ts_code, previous_2_work_day, end_date + datetime.timedelta(days=20))
                    result_now = pd.DataFrame(
                        [security_point_data.loc[previous_2_work_day], security_point_data.loc[previous_work_day], security_point_data.iloc[2], security_point_data.iloc[3],
                         security_point_data.iloc[4],
                         security_point_data.iloc[5], security_point_data.iloc[6], security_point_data.iloc[7]],
                        index=[['previous_2_day', 'previous_1_day', 'next_0_day', 'next_1_day', 'next_2_day', 'next_3_day', 'next_4_day', 'next_5_day'], [1, 1, 1, 1, 1, 1, 1, 1]])
                    result_now = result_now.unstack(level=0)
                    result.append(result_now)

            except Exception as e:
                pass
    return result


if __name__ == "__main__":
    result = []
    # for date in get_date_range(datetime.datetime(2016, 5, 3), datetime.datetime(2019, 1, 31)):
    for date in get_date_range(datetime.datetime(2016, 5, 3), datetime.datetime(2016, 5, 5)):
        print(date, datetime.datetime.now())
        with open('./date_now_log', "w") as f:
            f.write(convert_datetime_to_str(date))
        start(date, result)
    result = pd.concat(result)
    result = result.reset_index(drop=True)

    result.to_csv('./avg_point_5_penetrate_10.csv')
    print(result[['close', 'open', 'pct_chg']])
