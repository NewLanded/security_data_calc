import datetime

from source.util.util_base.db_util import get_connection, update_data


class Dml:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def store_failed_message(self, code, index, error_message, date):
        sql = """
        insert into failed_code(`code`, `index`, `error_message`, `date`)
        values(:code, :index, :error_message, :date)
        """
        args = {
            "code": code,
            "index": index,
            "error_message": error_message,
            "date": date
        }
        update_data(self._session, sql, args)


if __name__ == "__main__":
    ss = Dml()
    ss.store_failed_message("01", "01", "01", datetime.datetime(2018, 9, 7))
