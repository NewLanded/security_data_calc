import datetime

from source.util.util_base.db_util import get_connection, get_boolean_value, get_single_value


class Date:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def is_workday(self, date):
        sql = """
        select 1 from sec_date_info where date = :date and is_workday_flag=1
        """
        args = {"date": date}
        workday_flag = get_boolean_value(self._session, sql, args)
        return workday_flag

    def get_previous_workday(self, date):
        sql = """
        select max(date) from sec_date_info where date < :date and is_workday_flag=1
        """
        args = {"date": date}
        workday_flag = get_single_value(self._session, sql, args)
        return workday_flag


if __name__ == "__main__":
    ss = Date()
    ee = ss.get_previous_workday(datetime.datetime(2018, 9, 10))
    print(ee)
