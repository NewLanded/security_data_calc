"""
下跌几天后买入, 回撤或收入到一定程度卖出
"""
import datetime
import talib as ta
from util.util_base.date_util import get_date_range
from util.util_data.date import Date
from util.util_data.market_info import MarketInfo
from util.util_data.result import Result
from util.util_data.security_data import SecurityData


def buy(security_point_data):
    ema_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=1)
    sma_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=0)
    sma_data_30 = ta.MA(security_point_data["close"], timeperiod=30, matype=0)

    sma_5_t, sma_5_t_1, sma_5_t_2 = sma_data_5.iloc[-1], sma_data_5.iloc[-2], sma_data_5.iloc[-3]
    ema_5_t, ema_5_t_1, ema_5_t_2 = ema_data_5.iloc[-1], ema_data_5.iloc[-2], ema_data_5.iloc[-3]
    sma_30_t, sma_30_t_1, sma_30_t_2 = sma_data_30.iloc[-1], sma_data_30.iloc[-2], sma_data_30.iloc[-3]

    sma_5_slope_symbol_t = 0b100 if sma_5_t - sma_5_t_1 > 0 else 0b010 if sma_5_t - sma_5_t_1 < 0 else 0b001
    ema_5_slope_symbol_t = 0b100 if ema_5_t - ema_5_t_1 > 0 else 0b010 if ema_5_t - ema_5_t_1 < 0 else 0b001
    sma_30_slope_symbol_t = 0b100 if sma_30_t - sma_30_t_1 > 0 else 0b010 if sma_30_t - sma_30_t_1 < 0 else 0b001

    sma_5_slope_symbol_t_1 = 0b100 if sma_5_t_1 - sma_5_t_2 > 0 else 0b010 if sma_5_t_1 - sma_5_t_2 < 0 else 0b001
    ema_5_slope_symbol_t_1 = 0b100 if ema_5_t_1 - ema_5_t_2 > 0 else 0b010 if ema_5_t_1 - ema_5_t_2 < 0 else 0b001
    sma_30_slope_symbol_t_1 = 0b100 if sma_30_t_1 - sma_30_t_2 > 0 else 0b010 if sma_30_t_1 - sma_30_t_2 < 0 else 0b001

    if sma_5_slope_symbol_t != 0b001 and sma_30_slope_symbol_t != 0b001 and ema_5_slope_symbol_t != 0b001:
        if not sma_5_slope_symbol_t_1 & sma_30_slope_symbol_t_1:  # 昨天的方向不同
            if sma_5_slope_symbol_t & sma_30_slope_symbol_t:  # 今天的方向相同
                return True

        if sma_5_slope_symbol_t_1 & sma_30_slope_symbol_t_1:  # 昨天的方向相同
            if sma_5_slope_symbol_t & sma_30_slope_symbol_t:  # 今天的方向相同
                if not ema_5_slope_symbol_t_1 & sma_30_slope_symbol_t_1:  # 昨天的方向不同
                    if ema_5_slope_symbol_t & sma_30_slope_symbol_t:  # 今天的方向相同
                        return True

    return False


def sell(security_point_data):
    ema_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=1)
    sma_data_30 = ta.MA(security_point_data["close"], timeperiod=30, matype=0)

    ema_5_t, ema_5_t_1, ema_5_t_2 = ema_data_5.iloc[-1], ema_data_5.iloc[-2], ema_data_5.iloc[-3]
    sma_30_t, sma_30_t_1, sma_30_t_2 = sma_data_30.iloc[-1], sma_data_30.iloc[-2], sma_data_30.iloc[-3]

    ema_5_slope_symbol_t = 0b100 if ema_5_t - ema_5_t_1 > 0 else 0b010 if ema_5_t - ema_5_t_1 < 0 else 0b001
    sma_30_slope_symbol_t = 0b100 if sma_30_t - sma_30_t_1 > 0 else 0b010 if sma_30_t - sma_30_t_1 < 0 else 0b001

    ema_5_slope_symbol_t_1 = 0b100 if ema_5_t_1 - ema_5_t_2 > 0 else 0b010 if ema_5_t_1 - ema_5_t_2 < 0 else 0b001
    sma_30_slope_symbol_t_1 = 0b100 if sma_30_t_1 - sma_30_t_2 > 0 else 0b010 if sma_30_t_1 - sma_30_t_2 < 0 else 0b001

    if not ema_5_slope_symbol_t & ema_5_slope_symbol_t_1:  # 5日线方向变化的时候, 平仓
        return True

    if not sma_30_slope_symbol_t & sma_30_slope_symbol_t_1:  # 30日线方向变化的时候, 平仓
        return True

    return False


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        start_date, end_date = date_now - datetime.timedelta(days=365), date_now

        ts_codes = MarketInfo().get_future_main_code_filter_by_manual(date_now)
        for ts_code in ts_codes:
            try:
                security_point_data = SecurityData().get_future_security_point_data(ts_code, start_date, end_date)
                buy_flag = buy(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "future_bs_when_trend_start", "B", date_now)
            except Exception as e:
                pass

            try:
                security_point_data = SecurityData().get_future_security_point_data(ts_code, start_date, end_date)
                buy_flag = sell(security_point_data)

                if buy_flag is True:
                    Result().insert_strategy_result_data(ts_code, "future_bs_when_trend_start", "S", date_now)
            except Exception as e:
                pass

            # security_point_data = SecurityData().get_future_security_point_data(ts_code, start_date, end_date)
            # buy_flag = buy(security_point_data)
            #
            # if buy_flag is True:
            #     print(ts_code, buy_flag)


if __name__ == "__main__":
    start_date, end_date = datetime.datetime(2019, 9, 1), datetime.datetime(2019, 12, 31)
    for date in get_date_range(start_date, end_date):
        print(date)
        start(date)
