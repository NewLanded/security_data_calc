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

        self._per_interval_info = []  # [[开始时间, 结束时间, 持仓点位, 卖出点位]]


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
