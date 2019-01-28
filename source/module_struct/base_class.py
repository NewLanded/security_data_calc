from source.util.util_data.result import Result


class HoldenFake:
    def __init__(self):
        self._holded_flag = False
        self._hold_ts_code = None
        self._hold_tactics_code = None
        self._hold_hold_point = None
        self._hold_hold_amount = None

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
        self._hold_hold_point = None
        self._hold_hold_amount = None

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
    _holden_class = HoldenReal

    def __init__(self, ts_code, date, tactics_code):
        self._ts_code = ts_code
        self._date = date
        self._tactics_code = tactics_code

        self._update_holden_flag = False  # 是否更新持仓
        self._init_holden_data()
        self._init_bs_result()

    def _init_holden_data(self):
        holden_data = self._holden_class().get_holded_data(self._ts_code, self._tactics_code)
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
                self._hold_point = (self._hold_amount * self._hold_point - self._sell_amount * self._sell_point) / self._hold_amount if self._hold_amount else 0

            if self._buy_flag is True:
                self._hold_amount = self._hold_amount + self._buy_amount
                self._hold_point = (self._hold_amount * self._hold_point + self._buy_amount * self._buy_point) / self._hold_amount if self._hold_amount else 0

            if self._sell_flag is True or self._buy_flag is True:
                self._holden_class().update_holded_data(self._ts_code, self._tactics_code, self._hold_point, self._hold_amount)

    def _get_bs_result(self):
        return self._buy_flag, self._sell_flag, self._buy_point, self._sell_point, self._buy_amount, self._sell_amount

    def start(self):
        self.sell()
        self.buy()
        self.loss_stop()
        self.update_holden_data()
        return self._get_bs_result()

    @classmethod
    def set_holden_class(cls, holded_class):
        cls._holden_class = holded_class


if __name__ == "__main__":
    BSBase.set_holden_class(HoldenFake)
    print(BSBase(1, 2, 1)._holden_class)
