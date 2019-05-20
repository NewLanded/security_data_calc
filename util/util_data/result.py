import datetime

from util.util_base.db_util import get_connection, update_data, get_single_column
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

    def get_strategy_result_data(self, strategy_code, bs_flag, date):
        sql = """
        select a.ts_code from strategy_result a 
        where strategy_code=:strategy_code and date=:date and bs_flag=:bs_flag
        """
        args = {"strategy_code": strategy_code, "bs_flag": bs_flag, "date": date}
        result = get_single_column(self._session, sql, args)
        return result


if __name__ == "__main__":
    ss = Result()
    print(ss.get_strategy_result_data("bbond", 'B', datetime.datetime(2019, 5, 20)))
