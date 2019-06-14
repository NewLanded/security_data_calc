"""
当点位下跌一段时间或一定百分比后买入
"""
import datetime

from util.util_base.date_util import get_date_range
from util.util_data.date import Date
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def start(start_date, end_date):
    ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status"])
    # ts_codes = ['002062.SZ', '002565.SZ']
    for ts_code in ts_codes:
        security_point_data = SecurityData().get_qfq_security_point_data(ts_code, start_date, end_date)
        for date_now in get_date_range(start_date, end_date):
            try:
                start_date, end_date = date_now - datetime.timedelta(days=90), date_now
                security_point_data_now = security_point_data.loc[start_date: end_date]
                calc_

            except Exception as e:
                pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2016, 5, 3), datetime.datetime(2016, 5, 8)
    start(start_date, end_date)



