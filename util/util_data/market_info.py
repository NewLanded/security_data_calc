import datetime
import re

from util.util_base.constant import symbol_endwith_L, manual_code_list
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

        result_new = []
        for row in result:
            # symbol = row[0].split('.')[0]
            symbol_ts, symbol_main = row[0].split('.')[0], row[1].split('.')[0]

            if re.match(r'[A-Z]*', symbol_ts).group(0) == re.match(r'[A-Z]*', symbol_main).group(0):
                result_new.append(row[1])

            # if symbol.endswith('L'):
            #     if symbol in symbol_endwith_L:
            #         result_new.append(row[1])
            # elif symbol.endswith('L'):
            #     pass
            # else:
            #     result_new.append(row[1])

        result = list(set(result_new))
        result.sort()

        return result

    def get_future_main_code_filter_by_manual(self, trade_date):
        main_code_list_ori = self.get_future_main_code(trade_date)

        main_code_list = []
        for code in main_code_list_ori:
            code_symbol = code.split('.')[0][:-4]
            if code_symbol in manual_code_list:
                main_code_list.append(code)

        main_code_list = list(set(main_code_list))
        main_code_list.sort()

        return main_code_list


if __name__ == "__main__":
    ss = MarketInfo()
    ff = ss.get_future_main_code_filter_by_manual(datetime.datetime(2019, 11, 28))
    print(ff)
    print(len(ff))
    aa = 1
