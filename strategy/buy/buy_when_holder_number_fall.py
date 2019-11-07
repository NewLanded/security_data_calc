"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime

from util.util_data.date import Date
from util.util_data.market_data import MarketData
from util.util_data.result import Result
from util.util_data.security import Security
from util.util_data.security_data import SecurityData


def get_four_holder_number_data(holder_number_data):
    if not holder_number_data:
        return []

    result = []
    the_last_data_date = holder_number_data[-1][2]
    deadline_date_list = [the_last_data_date - datetime.timedelta(days=90), the_last_data_date - datetime.timedelta(days=60), the_last_data_date - datetime.timedelta(days=30),
                          the_last_data_date]
    deadline_date_index = 3
    for index in range(len(holder_number_data) - 1, -1, -1):
        if holder_number_data[index][2] <= deadline_date_list[deadline_date_index]:
            result.insert(0, holder_number_data[index])
            deadline_date_index -= 1

        if deadline_date_index < 0:
            break

    return result


def buy(security_point_data, holder_number_data):
    holder_number_data = get_four_holder_number_data(holder_number_data)
    if len(holder_number_data) >= 4:
        holder_number_data_date = [i[2] for i in holder_number_data]
        holder_number_data_date = [Date().get_previous_workday_with_today(i) for i in holder_number_data_date]
        holder_number_data = [i[3] for i in holder_number_data]

        holder_number_date_point = security_point_data.loc[security_point_data["trade_date"].apply(lambda x: x in holder_number_data_date)]

        if holder_number_data == sorted(holder_number_data, reverse=True):
            # if sum([security_point_data["close"].iloc[-1], security_point_data["close"].iloc[-2], security_point_data["close"].iloc[-3]]) > sum(
            #         [security_point_data["close"].iloc[-4],
            #          security_point_data["close"].iloc[-5],
            #          security_point_data["close"].iloc[-6]]):  时间拖得太久了, 涨的时间段都已经过去了
            if security_point_data["close"].iloc[-1] > security_point_data["close"].iloc[-2] and security_point_data["close"].iloc[-1] > security_point_data["close"].iloc[-3]:
                # if security_point_data["close"].iloc[-1] > holder_number_date_point['close'].iloc[-1]:  没道理啊, 不一定披露日就是最低的点位
                if holder_number_date_point['close'].iloc[-1] < holder_number_date_point['close'][-2] < holder_number_date_point['close'][-3] < \
                        holder_number_date_point['close'][-4]:
                    return True

    return False


def sell(data):
    """
    """
    pass


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = Security().get_efficient_ts_code_by_column_name_list(["normal_status", "tactics_5_status", "tactics_7_status"])
        start_date, end_date = date_now - datetime.timedelta(days=465), date_now
        for ts_code in ts_codes:
            # for ts_code in '000592.SZ', '603800.SH', '603700.SH', '002547.SZ', '000709.SZ', '002006.SZ', '002375.SZ', '002009.SZ', '002873.SZ', '002883.SZ', '002911.SZ', '002862.SZ', '601005.SH':
            try:
                security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
                holder_number_data = MarketData().get_holder_number_data(ts_code, start_date, end_date)
                buy_flag = buy(security_point_data, holder_number_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "buy_when_holder_number_fall", "B", date_now)
            except Exception as e:
                pass

            # try:
            #     security_point_data = SecurityData().get_security_point_data(ts_code, start_date, end_date)
            #     holder_number_data = MarketData().get_holder_number_data(ts_code, start_date, end_date)
            #     buy_flag = buy(security_point_data, holder_number_data)
            #     if buy_flag is True:
            #         print(ts_code, buy_flag)
            # except Exception as e:
            #     pass


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2019, 11, 6), datetime.datetime(2016, 5, 8)
    start(start_date)
