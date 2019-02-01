import datetime
import json

from source.interface.fluctuation_tactics_1_restruct import BS
from source.module_struct.base_class import BSBaseOneSell, BSBaseMultiSells, HoldenFake, BSBaseMultiBSOneDay
from source.util.util_base.date_util import get_date_range
from source.util.util_base.result_util import print_format_result
from source.util.util_data.date import Date


class BackLook:
    """
    接收的方法: 买入(个券代码, 时间), 卖出(个券代码, 时间), 止损(个券代码, 时间)
    接收的参数: 开始时间, 结束时间, 个券代码
    计算的指标: 总收益率, 每一段的开始结束时间, 每一段持续的天数, 每一段的收益率, 每一段的最大回撤
    注意的问题: 当传入的结束日期到了但是还没有卖出, 这时抛弃这段时间的数据
                做成可扩展性的结构, 以后不知道还要加什么
    """

    def __init__(self, ts_code, start_date, end_date, bs_class, tactics_code):
        self._ts_code = ts_code
        self._start_date = start_date
        self._end_date = end_date
        self._bs_class = bs_class
        self._tactics_code = tactics_code

        # [{start_date: 开始时间, end_date: 结束时间, sub_interval_list: [{date: 日期, hold_point: 持仓点位, hold_amount: 持仓数量, sell_point: 卖出点位, sell_amount: 卖出数量}, ...]}]
        self._per_interval_info = []

    # 判断是否已持仓, 在回测的类中和每天的定时任务中, 一个是定义的类变量, 一个是要从数据库取, 可以定义同名的方法来实现这个
    @staticmethod
    def _calc_yield_by_yield_list(yield_list):
        total_yield = 0
        for yield_now in yield_list:
            total_yield = (total_yield + 1) * (yield_now + 1) - 1
        return total_yield

    def _calc_describe_data(self, **kwargs):
        # 总损益 _total_gainloss, 每一段持续的天数 _per_interval_days, 每一段的收益率 _per_interval_yield, 每一段的最大回撤 _per_interval_max_drawdown
        # 计算最大回撤需要收益率日期有序, 现在打算做一个日期为行索引的DataFrame, 不知行不行,  这应该是从数据库里面获取的数据按日期截取的一部分
        """
                   open    close ....
        2016-1-1   10.1    10.2 ...
        2016-1-2   ...
        ...
        """
        daily_yield = kwargs["daily_yield"]
        interval_yield = self._calc_yield_by_yield_list(daily_yield)

        self._total_yield = self._calc_yield_by_yield_list([self._total_yield, interval_yield])
        self._per_interval_start_end_date.append(kwargs["_per_interval_start_end_date"])
        self._per_interval_days.append(kwargs["_per_interval_days"])
        self._per_interval_yield.append(interval_yield)
        self._per_interval_max_drawdown.append(kwargs["_per_interval_max_drawdown"])

    def start(self):
        if issubclass(self._bs_class, BSBaseOneSell):
            self.start_multi_sell()
        elif issubclass(self._bs_class, BSBaseMultiSells):
            self.start_multi_sell()
        elif issubclass(self._bs_class, BSBaseMultiBSOneDay):
            self.start_multi_buy_sell_one_day()
        else:
            raise TypeError("未找到BS类的父类")

        self._calc_describe_data()

    def start_multi_sell(self):
        holden_instance = HoldenFake()
        self._bs_class.set_holden_instance(holden_instance)
        per_interval_started_flag = False

        for date_now in get_date_range(self._start_date, self._end_date):
            if Date().is_workday(date_now):
                buy_flag, sell_flag, buy_point, sell_point, buy_amount, sell_amount = self._bs_class(self._ts_code, date_now, self._tactics_code, False).start()

                holded_data = holden_instance.get_holded_data(self._ts_code, self._tactics_code)
                hold_amount, hold_point = holded_data.get("hold_amount", 0), holded_data.get("hold_point", 0)
                if sell_flag is True:
                    hold_amount = hold_amount - sell_amount
                    hold_point = hold_point if hold_amount else 0

                    if hold_amount == 0:
                        self._per_interval_info[-1]["end_date"] = date_now
                        self._per_interval_info[-1]["sub_interval_list"].append({
                            "date": date_now,
                            "hold_point": hold_point,
                            "hold_amount": hold_amount,
                            "sell_point": sell_point,
                            "sell_amount": sell_amount
                        })
                        per_interval_started_flag = False
                    else:
                        self._per_interval_info[-1]["sub_interval_list"].append({
                            "date": date_now,
                            "hold_point": hold_point,
                            "hold_amount": hold_amount,
                            "sell_point": sell_point,
                            "sell_amount": sell_amount
                        })

                if buy_flag is True:
                    hold_point = (hold_amount * hold_point + buy_amount * buy_point) / (hold_amount + buy_amount) if hold_amount + buy_amount else 0
                    hold_amount = hold_amount + buy_amount

                    if per_interval_started_flag is False:
                        self._per_interval_info.append({
                            "start_date": date_now,
                            "end_date": None,
                            "sub_interval_list": [{
                                "date": date_now,
                                "hold_point": hold_point,
                                "hold_amount": hold_amount,
                                "sell_point": None,
                                "sell_amount": None
                            }]
                        })
                        per_interval_started_flag = True
                    else:
                        if self._per_interval_info[-1]["sub_interval_list"][-1]["date"] == date_now:
                            self._per_interval_info[-1]["sub_interval_list"][-1]["hold_point"] = hold_point
                            self._per_interval_info[-1]["sub_interval_list"][-1]["hold_amount"] = hold_amount
                        else:
                            self._per_interval_info[-1]["sub_interval_list"].append({
                                "date": date_now,
                                "hold_point": hold_point,
                                "hold_amount": hold_amount,
                                "sell_point": None,
                                "sell_amount": None
                            })

                if (sell_flag is True or buy_flag is True) and hold_amount:
                    holden_instance.update_holded_data(self._ts_code, self._tactics_code, hold_point, hold_amount)
                elif sell_flag is True or buy_flag is True:
                    holden_instance.delete_holded_data(self._ts_code, self._tactics_code)
                else:
                    pass

        if self._per_interval_info and self._per_interval_info[-1]["end_date"] is None:  # 最后一段时期没走完, 就不算了, 也没法算
            self._per_interval_info.pop()

        print_format_result(self._per_interval_info)
        

    def start_multi_buy_sell_one_day(self):
        pass


if __name__ == "__main__":
    BackLook("000650.SZ", datetime.datetime(2018, 10, 11), datetime.datetime(2018, 11, 20), BS, "fluctuation_tactics_1").start()
