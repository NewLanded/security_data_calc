import datetime

from util.util_base.db_util import get_connection, update_data
from util.util_data.security import Security


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def insert_strategy_result_data(self, ts_code, strategy_code, bs_flag, date):
        code = Security().get_code_info_by_ts_code(ts_code)["code"]
        sql = """
        insert into strategy_result (ts_code, code, strategy_code, bs_flag, date, update_date) 
        values(:ts_code, :code, :strategy_code, :bs_flag, :date, :update_date)
        """
        args = {"ts_code": ts_code, "code": code, "strategy_code": strategy_code, "bs_flag": bs_flag,
                "date": date, "update_date": datetime.datetime.now()}
        update_data(self._session, sql, args)


if __name__ == "__main__":
    ss = Result()
    print(ss.insert_strategy_result_data("000001.SZ", "aa", 'B', datetime.datetime(2016, 1, 1)))
