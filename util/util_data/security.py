from util.util_base.db_util import get_connection, get_single_column, get_single_row


class Security:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_code_info_by_ts_code(self, ts_code):
        sql = """
        select `ts_code`, `code`, `name`, `area`, `industry`, `market`, `list_date` from s_info where ts_code = :ts_code
        """
        args = {"ts_code": ts_code}
        result = get_single_row(self._session, sql, args)
        result = {
            "code": result[1],
            "name": result[2],
            "area": result[3],
            "industry": result[4],
            "market": result[5],
            "list_date": result[6]
        }

        return result

    def get_efficient_ts_code_by_column_name(self, tactics_status_column):
        sql = """
        select ts_code from security_status where {0} = 1 and normal_status = 1
        """.format(tactics_status_column)
        efficient_ts_code = get_single_column(self._session, sql)

        return efficient_ts_code

    def get_efficient_ts_code_by_column_name_list(self, tactics_status_column_list):
        efficient_ts_code_all = []
        for tactics_status_column in tactics_status_column_list:
            efficient_ts_code = self.get_efficient_ts_code_by_column_name(tactics_status_column)
            efficient_ts_code_all.append(set(efficient_ts_code))

        if efficient_ts_code_all:
            efficient_ts_code = efficient_ts_code_all[0]
            for efficient_ts_code_now in efficient_ts_code_all[1:]:
                efficient_ts_code.intersection_update(efficient_ts_code_now)
        else:
            efficient_ts_code = set()
        return list(efficient_ts_code)


if __name__ == "__main__":
    ss = Security()
