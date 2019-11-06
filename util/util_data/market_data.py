import datetime

from util.util_base.db_util import get_connection
from util.util_base.db_util import get_multi_data


class MarketData:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_holder_number_data(self, ts_code, start_date, end_date):
        sql = """
        select ts_code, ann_date, end_date, holder_num from holder_number_data where ts_code = :ts_code and end_date >= :start_date and end_date <= :end_date order by end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(self._session, sql, args)

        return result


if __name__ == "__main__":
    ss = MarketData()
    ff = ss.get_holder_number_data("000001.SZ", datetime.datetime(2018, 8, 1), datetime.datetime(2019, 8, 4))
    print(ff)
    aa = 1
