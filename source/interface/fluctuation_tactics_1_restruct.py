import datetime

from source.module_struct.base_class import BSBase
from source.util.util_data.date import Date
from source.util.util_data.dml import Dml
from source.util.util_data.security import Security
from source.util.util_data.security_data import SecurityData

"""
数据使用涨跌幅
不能连续跌, 按天, 比前一天涨的要大于40%
至少有20%的次数涨幅超过1.5%
期间不能有涨停, 避免这种风险
最后5天跌的比涨的多
"""


class BS(BSBase):
    def __init__(self, ts_code, date, tactics_code):
        super().__init__(ts_code=ts_code, date=date, tactics_code=tactics_code)
        self._start_date, self._end_date = date - datetime.timedelta(days=90), date

    def buy(self):
        security_point_data = SecurityData().get_security_point_data(self._ts_code, self._start_date, self._end_date)
        date_pct_chg_list = [[trade_date, value["pct_chg"]] for trade_date, value in security_point_data.items()]
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

        self._buy_flag, self._buy_point, self._buy_amount = buy_flag, 0, 0

    def sell(self):
        pass

    def loss_stop(self):
        pass


def start():
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code(["tactics_2_status", "tactics_3_status", "tactics_4_status", "tactics_5_status"])
        for ts_code in ts_codes:
            try:
                buy_flag, sell_flag, buy_point, sell_point, buy_amount, sell_amount = BS(ts_code, date_now, "fluctuation_tactics_1").start()

                if buy_flag is True:
                    code_info = Security().get_code_info_by_ts_code(ts_code)
                    # Result().insert_result_data(code_info["code"], 'b', buy_point, None, buy_amount, tactics_code="fluctuation_tactics_1",
                    #                             forecast_date=date_now)
                    print(ts_code, code_info, buy_point, buy_amount, buy_flag)
            except Exception as e:
                Dml().store_failed_message(ts_code, "fluctuation_tactics_1", str(e), date_now)


if __name__ == "__main__":
    start()
