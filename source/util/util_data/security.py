import datetime

from source.util.util_base.db_util import get_connection, get_boolean_value, get_multi_data, get_single_column, get_single_row


class Security:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_code_info_by_ts_code(self, ts_code):
        sql = """
        select code, name from s_info where ts_code = :ts_code
        """
        args = {"ts_code": ts_code}
        result = get_single_row(self._session, sql, args)

        return {"code": result[0], "code_name": result[1]}

    def get_efficient_ts_code_by_column_name(self, tactics_status_column):
        sql = """
        select ts_code from security_status where {0} = 1 and normal_status = 1
        """.format(tactics_status_column)
        efficient_ts_code = get_single_column(self._session, sql)

        return efficient_ts_code

    def get_efficient_ts_code(self, tactics_status_column_list):
        efficient_ts_code = set()
        for tactics_status_column in tactics_status_column_list:
            efficient_ts_code_now = self.get_efficient_ts_code_by_column_name(tactics_status_column)
            if not efficient_ts_code:
                efficient_ts_code = set(efficient_ts_code_now)
            else:
                efficient_ts_code = efficient_ts_code.intersection(set(efficient_ts_code_now))

        return list(efficient_ts_code)


if __name__ == "__main__":
    ss = Security()
