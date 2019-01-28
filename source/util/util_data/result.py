import datetime

from source.util.util_base.db_util import get_connection, update_data, get_single_row, get_multi_data


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def insert_result_data(self, code, bs_flag, b_point=0, s_point=0, quantity=0, tactics_code="", forecast_date=None):
        sql = """
        insert into bs_data (code, b_point, s_point, quantity, tactics_code, bs_flag, sent_flag, forecast_date, update_date) 
        values(:code, :b_point, :s_point, :quantity, :tactics_code, :bs_flag, 0, :forecast_date, :update_date)
        """
        args = {"code": code, "b_point": b_point, "s_point": s_point, "quantity": quantity, "tactics_code": tactics_code, "bs_flag": bs_flag,
                "update_date": datetime.datetime.now(), "forecast_date": forecast_date}
        update_data(self._session, sql, args)

    def get_unsent_result(self):
        pass

    def update_result_data(self):
        pass

    def get_holden_data(self, ts_code, tactics_code):
        sql = """
        select ts_code, tactics_code, hold_point, hold_amount from holded_info where ts_code = :ts_code and tactics_code = :tactics_code
        """
        args = {"ts_code": ts_code, "tactics_code": tactics_code}
        result = get_single_row(self._session, sql, args)
        if result:
            result = {
                "ts_code": result[0],
                "tactics_code": result[1],
                "hold_point": result[2],
                "hold_amount": result[3]
            }
        else:
            result = {}
        return result

    def delete_holden_data(self, ts_code, tactics_code):
        sql = """
        delete from holded_info where ts_code=:ts_code and tactics_code=:tactics_code
        """
        args = {"ts_code": ts_code, "tactics_code": tactics_code}
        update_data(self._session, sql, args)

    def update_holden_data(self, ts_code, tactics_code, hold_point, hold_amount):
        self.delete_holden_data(ts_code, tactics_code)

        sql = """
        insert into holded_info(ts_code, tactics_code, hold_point, hold_amount, update_date) values(:ts_code, :tactics_code, :hold_point, :hold_amount, :update_date)
        """
        args = {"ts_code": ts_code, "tactics_code": tactics_code, "hold_point": hold_point, "hold_amount": hold_amount, "update_date": datetime.datetime.now()}
        update_data(self._session, sql, args)


if __name__ == "__main__":
    ss = Result()
    print(ss.get_holden_data("000001.SZ", "aa"))
