import datetime
import math

import backtrader as bt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

from conf import DB_CONNECT
from strategy.backtest.result_code import get_result_ts_code_list

engine = create_engine(DB_CONNECT, echo=False, pool_recycle=3600)


def get_security_data(ts_code):
    sql = """
    select trade_date, open, high, low, close, vol as volume from qfq_security_point_data where ts_code='{0}' 
    order by trade_date
    """.format(ts_code)
    df = pd.read_sql_query(sql, engine)
    df = df.set_index('trade_date')
    df = df.sort_index()
    return df


# def get_all_ts_code():
#     sql = """
#     select ts_code from security_status where normal_status=1 and tactics_5_status=1 and tactics_4_status=1 and tactics_3_status=1
#     """
#     df = pd.read_sql_query(sql, engine)
#     aa = list(df["ts_code"])
#     return aa
def get_all_ts_code():
    sql = """
    select ts_code from security_concept_info_detail where concept_code='TS11'
    """
    df = pd.read_sql_query(sql, engine)
    aa = list(df["ts_code"])
    return aa


class AllIn(bt.Sizer):
    params = (
        ('stake', 1),
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            try:
                return cash * (1 - comminfo.p.commission) // data.lines.open[1]
            except IndexError as e:
                return 0

        # Sell situation
        position = self.broker.getposition(data)
        if not position.size:
            return 0  # do not sell if nothing is open

        return position.size


class PowOne(bt.Sizer):
    params = (
        ('stake', 1),
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            try:
                position = self.broker.getposition(data)
                # print(position.size)
                if not position:
                    return 1
                else:
                    position = position.size
                    return position
            except IndexError as e:
                return 0

        # Sell situation
        position = self.broker.getposition(data)
        if not position.size:
            return 0  # do not sell if nothing is open

        return position.size


class SMASlope(bt.Indicator):
    lines = ("sma_slope_10", "sma_slope_30")

    def __init__(self):
        self.sma_data_10 = bt.indicators.SimpleMovingAverage(self.datas[0], period=10)
        self.sma_data_30 = bt.indicators.SimpleMovingAverage(self.datas[0], period=30)

    def _get_first_point_multiplying_power_by_1(self, point):
        return point / 100

    def _get_point_list(self, sma_data, period=5):
        first_point = sma_data[-period]
        multiplying_power = self._get_first_point_multiplying_power_by_1(first_point)

        point_list = []
        for index in range(-period, 1):
            if not math.isnan(sma_data[index]) and not math.isnan(first_point):
                point_list.append([index + period, sma_data[index] / multiplying_power])
        return point_list

    def _calc_slope(self, point_list):
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
        return slope

    def next(self):
        point_list_sma10 = self._get_point_list(self.sma_data_10)
        point_list_sma30 = self._get_point_list(self.sma_data_30)

        slope_10 = self._calc_slope(point_list_sma10)
        slope_30 = self._calc_slope(point_list_sma30)

        self.lines.sma_slope_10[0] = slope_10
        self.lines.sma_slope_30[0] = slope_30


class PctChg(bt.Indicator):
    lines = ("pct_chg",)

    def __init__(self, close_data):
        self.close_data = close_data

    def next(self):
        pct_chg = (self.close_data[0] - self.close_data[-1]) / self.close_data[-1]
        self.lines.pct_chg[0] = pct_chg


class MaxPoint(bt.Indicator):
    lines = ("max_point",)

    def __init__(self, close_data, maperiod):
        self.close_data = close_data
        self.maperiod = maperiod

    def next(self):
        max_point = 0
        for i in range(-self.maperiod, 1):
            max_point = max(max_point, self.close_data[i])

        self.lines.max_point[0] = max_point


class MinPoint(bt.Indicator):
    lines = ("min_point",)

    def __init__(self, close_data, maperiod):
        self.close_data = close_data
        self.maperiod = maperiod

    def next(self):
        min_point = 10000
        for i in range(-self.maperiod, 1):
            min_point = min(min_point, self.close_data[i])

        self.lines.min_point[0] = min_point


class TestStrategy(bt.Strategy):
    params = (
        ('maperiod_sma', 15),
        ('maperiod_bbands', 15),
        ('maperiod_max_point', 50),
        ('maperiod_min_point', 50),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.pct_chg = PctChg(close_data=self.dataclose)
        self.std_dev = bt.talib.STDDEV(close_data=self.dataclose, timeperiod=self.params.maperiod_bbands, nbdev=2)
        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=7)
        self.sma_slope = SMASlope()
        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod_sma)
        self.bbands = bt.talib.BBANDS(self.datas[0], timeperiod=self.params.maperiod_bbands, nbdevup=2, nbdevdn=2, matype=0)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price if not self.buyprice else (self.buyprice + order.executed.price) / 2
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = None
                self.buycomm = None
                pass

            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # self.log('Close, {0:.2f}, {1:.4f}'.format(self.dataclose[0], self.sma_slope.lines.sma_slope_30[0]))
        if self.order:
            return
        if not self.position:
            # 收盘价上穿布林带下轨
            if self.dataclose[0] < self.bbands.lines.lowerband[0] * 1.01 and \
                    self.std_dev[0] / self.bbands.lines.middleband[0] > 0.04 and \
                    self.sma_slope.lines.sma_slope_30[0] >= 0:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.buyprice * 0.95:
                self.order = self.sell()
            elif self.dataclose[0] > self.buyprice * 1.06 and self.sma_slope.lines.sma_slope_10[0] <= 0:
                self.order = self.sell()
            elif self.dataclose[0] > self.buyprice * 1.15 and self.dataclose[0] < self.dataclose[-1]:
                self.order = self.sell()


if __name__ == '__main__':
    result = []
    # all_ts_code = get_all_ts_code()
    all_ts_code = get_result_ts_code_list()
    for ts_code in all_ts_code:
        try:
            cerebro = bt.Cerebro()

            cerebro.addstrategy(TestStrategy)
            # cerebro.addsizer(PowOne)
            cerebro.addsizer(AllIn)

            security_data = get_security_data(ts_code)

            # data = bt.feeds.PandasData(dataname=security_data, fromdate=datetime.datetime(2017, 3, 1),
            #                            todate=datetime.datetime(2018, 6, 30))
            data = bt.feeds.PandasData(dataname=security_data, fromdate=datetime.datetime(2016, 1, 1),
                                       todate=datetime.datetime(2019, 1, 30))
            # data = bt.feeds.PandasData(dataname=security_data, fromdate=datetime.datetime(2017, 6, 30),
            #                            todate=datetime.datetime(2019, 4, 30))
            cerebro.adddata(data)

            cerebro.broker.setcash(100.0)

            cerebro.broker.setcommission(commission=0.0025)
            results = cerebro.run()

            print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
            result.append([ts_code, cerebro.broker.getvalue()])
            cerebro.plot()
        except Exception as e:
            pass
    result.sort(key=lambda x: x[1], reverse=True)
    print(len([i[1] for i in result if i[1] > 100]) / len(result))
    print(len([i[1] for i in result if i[1] == 100]) / len(result))
    print(len([i[1] for i in result if i[1] < 100]) / len(result))
    print(result)
