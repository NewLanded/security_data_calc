import datetime

from source.util.util_base.db_util import get_connection, update_data


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def insert_result_data(self, code, b_point=0, s_point=0, quantity=0, tactics_code="", forecast_date=None):
        sql = """
        insert into bs_data (code, b_point, s_point, quantity, tactics_code, sent_flag, forecast_date, update_date) 
        values(:code, :b_point, :s_point, :quantity, :tactics_code, 0, :forecast_date, :update_date)
        """
        args = {"code": code, "b_point": b_point, "s_point": s_point, "quantity": quantity, "tactics_code": tactics_code,
                "update_date": datetime.datetime.now(), "forecast_date": forecast_date}
        update_data(self._session, sql, args)

    def get_unsent_result(self):
        pass

    def update_result_data(self):
        pass


if __name__ == "__main__":
    ss = Result()
    ss.insert_result_data("ee", forecast_date=datetime.datetime.now())
