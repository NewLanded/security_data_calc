from source.util.util_data.result import Result


class HoldenFake:
    def __init__(self):
        self._holded_flag = False
        self._hold_ts_code = None
        self._hold_tactics_code = None
        self._hold_hold_point = 0
        self._hold_hold_amount = 0

    def is_holden(self, ts_code, tactics_code):
        return True if self.get_holded_data(ts_code, tactics_code) else False

    def get_holded_data(self, ts_code, tactics_code):
        if self._holded_flag is True:
            return {
                "ts_code": self._hold_ts_code,
                "tactics_code": self._hold_tactics_code,
                "hold_point": self._hold_hold_point,
                "hold_amount": self._hold_hold_amount
            }
        else:
            return {}

    def delete_holded_data(self, ts_code, tactics_code):
        self._holded_flag = False
        self._hold_ts_code = None
        self._hold_tactics_code = None
        self._hold_hold_point = 0
        self._hold_hold_amount = 0

    def update_holded_data(self, ts_code, tactics_code, hold_point, hold_amount):
        self._holded_flag = True
        self._hold_ts_code = ts_code
        self._hold_tactics_code = tactics_code
        self._hold_hold_point = hold_point
        self._hold_hold_amount = hold_amount


class HoldenReal:
    def is_holden(self, ts_code, tactics_code):
        return True if self.get_holded_data(ts_code, tactics_code) else False

    def get_holded_data(self, ts_code, tactics_code):
        return Result().get_holden_data(ts_code, tactics_code)

    def delete_holded_data(self, ts_code, tactics_code):
        Result().delete_holden_data(ts_code, tactics_code)

    def update_holded_data(self, ts_code, tactics_code, hold_point, hold_amount):
        Result().update_holden_data(ts_code, tactics_code, hold_point, hold_amount)


class BSBase:
    """
    判断买点和卖点其实并不以你持仓了多少位标准, 所以类似于越跌越买的策略, 是写在回测框架中看是否有效的, 这里只是判断个股价格走势
    """
    """
    关于 buy 和 sell 方法的复用
        可以在外部定义buy和sell的细节, 然后在类内部调用这些定义好的函数, 但是我们需要的是有用的策略, 没必要复用写一堆没用的
    
    关于sell有时候不需要定义导致的没办法回测
        这个就是得定义sell, 定义的时候先加一个检验是否有持仓的判断, 如果没持仓, 就不运行, 这个也是合理的(回测的时候肯定是有持仓的)
    """
    _holden_instance = HoldenReal()

    def __init__(self, ts_code, date, tactics_code, update_holden_flag=False):
        self._ts_code = ts_code
        self._date = date
        self._tactics_code = tactics_code

        self._update_holden_flag = update_holden_flag  # 是否更新持仓
        self._init_holden_data()
        self._init_bs_result()

    def _init_holden_data(self):
        holden_data = self._holden_instance.get_holded_data(self._ts_code, self._tactics_code)
        self._hold_point = holden_data.get("hold_point", 0)
        self._hold_amount = holden_data.get("hold_amount", 0)

    def _init_bs_result(self):
        self._buy_flag = None
        self._sell_flag = None

        self._buy_point = 0
        self._sell_point = 0

        self._buy_amount = 0
        self._sell_amount = 0

    def buy(self):
        """
        注意是否已持仓, 可能会是不同的算法
        """
        pass

    def sell(self):
        """
        注意是否已持仓, 可能会是不同的算法
        """
        pass

    def loss_stop(self):
        pass

    def update_holden_data(self):
        if self._update_holden_flag is True:
            if self._sell_flag is True:
                self._hold_amount = self._hold_amount - self._sell_amount
                self._hold_point = self._hold_point if self._hold_amount else 0

            if self._buy_flag is True:
                self._hold_point = (self._hold_amount * self._hold_point + self._buy_amount * self._buy_point) / (
                        self._hold_amount + self._buy_amount) if self._hold_amount + self._buy_amount else 0
                self._hold_amount = self._hold_amount + self._buy_amount

            if (self._sell_flag is True or self._buy_flag is True) and self._hold_amount:
                self._holden_instance.update_holded_data(self._ts_code, self._tactics_code, self._hold_point, self._hold_amount)
            elif self._sell_flag is True or self._buy_flag is True:
                self._holden_instance.delete_holded_data(self._ts_code, self._tactics_code)
            else:
                pass

    def _get_bs_result(self):
        return self._buy_flag, self._sell_flag, self._buy_point, self._sell_point, self._buy_amount, self._sell_amount

    def start(self):
        self.sell()
        self.buy()
        self.loss_stop()
        self.update_holden_data()
        return self._get_bs_result()

    @classmethod
    def set_holden_instance(cls, holded_instance):
        cls._holden_instance = holded_instance


class BSBaseOneSell(BSBase):
    """
    这个是计算简单的收益, 即支持多次买入, 但只支持一次全部卖出, 支持的策略为不关注持仓的具体数量
    (但是要有一个名义数量, 比如初始设置为1, 然后每次买入翻倍之类的, 用来计算多次买入后的持仓点位)
    现在只支持每次买入翻倍, 若想支持其他买入倍数, 可以覆盖 _init_buy_amount
    """

    def __init__(self, ts_code, date, tactics_code, update_holden_flag=False):
        super().__init__(ts_code=ts_code, date=date, tactics_code=tactics_code, update_holden_flag=update_holden_flag)
        self._init_buy_amount()

    def _init_buy_amount(self):
        if self._hold_amount == 0:
            self._buy_amount = 1
        else:
            self._buy_amount = self._hold_amount


class BSBaseMultiSells(BSBase):
    """
    这个是计算复杂的收益, 即支持多次买入, 多次卖出, 需要设定期初净值, 最后以  (期末净值-期初净值)/期初净值  作为收益率,
    支持的策略需要关注具体的持仓数量及价格, 买入时的开销不能超过现有可动用的资金
    (所以需要多维护两个类变量, total_fund总资金, available_fund可用于投资的资金, 这是维护在BS类里面, 具体策略里面用的)
    """

    def __init__(self, ts_code, date, tactics_code, update_holden_flag=False, total_fund=100000):
        super().__init__(ts_code=ts_code, date=date, tactics_code=tactics_code, update_holden_flag=update_holden_flag)
        self._total_fund = total_fund  # 期初资金
        self._available_fund = self._total_fund  # 可用于购买的资金

    def _update_available_fund(self, change_fund):
        self._available_fund += change_fund

    def sell(self):
        """
        对于 BSBaseMultiSells 下的sell, 必须返回卖出的数量, 即有持仓, 才能卖
        """
        if self._hold_amount:
            pass


class BSBaseMultiBSOneDay(BSBase):
    """
    支持在一天中多次买入卖出, 暂不实现
    """
    pass


if __name__ == "__main__":
    BSBase.set_holden_instance(HoldenFake())
    print(BSBase(1, 2, 1)._holden_instance)
