"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime

from util.util_base.date_util import get_date_range
from util.util_data.date import Date
from util.util_data.market_info import MarketInfo
from util.util_data.result import Result
from util.util_data.security_data import SecurityData


def buy(security_point_data):
    security_point_data['close_change'] = security_point_data['close'] - security_point_data['pre_close']
    highest_point_index, lowest_point_index = security_point_data['close'].idxmax(axis=0, skipna=True), security_point_data['close'].idxmin(axis=0, skipna=True)
    highest_point, lowest_point = security_point_data['close'][highest_point_index], security_point_data['close'][lowest_point_index]

    point_now = security_point_data['close'].iloc[-1]

    point_extreme = highest_point if highest_point_index > lowest_point_index else lowest_point

    max_interval_point_change = highest_point - lowest_point
    now_interval_point_change = abs(point_now - point_extreme)

    change_percent = now_interval_point_change / max_interval_point_change

    if point_now > point_extreme:
        if security_point_data['close_change'].iloc[-1] > 0 and \
                security_point_data['close_change'].iloc[-2] < 0 and \
                security_point_data['close_change'].iloc[-4] > 0 and \
                security_point_data['close_change'].iloc[-5] > 0:
            # 最后5天, 涨涨*跌涨
            pass
        else:
            return False
    else:
        if security_point_data['close_change'].iloc[-1] < 0 and \
                security_point_data['close_change'].iloc[-2] > 0 and \
                security_point_data['close_change'].iloc[-4] < 0 and \
                security_point_data['close_change'].iloc[-5] < 0:
            # 最后5天, 跌跌*涨跌
            pass
        else:
            return False

    if 0.1 < change_percent < 0.7:
        print(change_percent, point_now, point_extreme, highest_point, lowest_point)
        return True
    else:
        return False


def sell(data):
    """
    """
    pass


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        ts_codes = MarketInfo().get_future_main_code_filter_by_manual(date_now)
        start_date, end_date = date_now - datetime.timedelta(days=365), date_now
        for ts_code in ts_codes:
            # try:
            #     security_point_data = SecurityData().get_future_security_point_data(ts_code, start_date, end_date)
            #     buy_flag = buy(security_point_data)
            #
            #     if buy_flag is True:
            #         Result().insert_strategy_result_data(ts_code, "future_buy_when_trend_start", "B", date_now)
            # except Exception as e:
            #     pass

            # ts_code = 'SR2001.ZCE'
            security_point_data = SecurityData().get_future_security_point_data(ts_code, start_date, end_date)
            buy_flag = buy(security_point_data)
            if buy_flag is True:
                print(ts_code, buy_flag)
            # break


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2019, 10, 1), datetime.datetime(2019, 10, 20)
    for date in get_date_range(start_date, end_date):
        print(date)
        start(date)
