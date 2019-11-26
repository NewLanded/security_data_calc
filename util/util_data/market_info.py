import datetime

from util.util_base.db_util import get_connection
from util.util_base.db_util import get_multi_data


class MarketInfo:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_future_main_code(self, trade_date):
        sql = """
        select ts_code, mapping_ts_code from future_main_code_data where trade_date=:trade_date
        """
        args = {"trade_date": trade_date}
        result = get_multi_data(self._session, sql, args)

        code_month_list = ['01', '05', '09']
        result = [i[1] for i in result if i[1].split('.')[0][-2:] in code_month_list]
        result = list(set(result))

        return result

    def get_future_main_code_filter_by_manual(self, trade_date):
        main_code_list_ori = self.get_future_main_code(trade_date)

        code_start_str_list = ['CF', 'OI', 'FG', 'RM', 'CY', 'AP', 'SR', 'JD', 'C', 'L', 'M', 'P', 'Y', 'HC', 'RB']
        main_code_list = []
        for code in main_code_list_ori:
            code_symbol = code.split('.')[0][:-4]
            if code_symbol in code_start_str_list:
                main_code_list.append(code)

        main_code_list = list(set(main_code_list))
        main_code_list.sort()

        return main_code_list


if __name__ == "__main__":
    ss = MarketInfo()
    ff = ss.get_future_main_code_filter_by_manual(datetime.datetime(2019, 11, 21))
    print(ff)
    aa = 1
