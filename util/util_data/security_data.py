import datetime

import pandas as pd

from util.util_base.db_util import engine


class SecurityData:
    """
    sql = '''select trade_date, close from security_point_data where ts_code='000001.SZ' order by trade_date '''
    df = pd.read_sql_query(sql, engine)
    """

    def get_index_point_data(self, ts_code, start_date, end_date):
        sql = """
        select `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from index_point_data 
        where ts_code = %(ts_code)s and trade_date between %(start_date)s and %(end_date)s
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        security_point_data = pd.read_sql_query(sql, engine, params=args)
        security_point_data.set_index(security_point_data["trade_date"], inplace=True)
        security_point_data = security_point_data.sort_index()

        return security_point_data

    def get_security_point_data(self, ts_code, start_date, end_date):
        sql = """
        select `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from security_point_data 
        where ts_code = %(ts_code)s and trade_date between %(start_date)s and %(end_date)s
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        security_point_data = pd.read_sql_query(sql, engine, params=args)
        security_point_data.set_index(security_point_data["trade_date"], inplace=True)
        security_point_data = security_point_data.sort_index()

        return security_point_data

    def get_qfq_security_point_data(self, ts_code, start_date, end_date):
        sql = """
        select `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from qfq_security_point_data 
        where ts_code = %(ts_code)s and trade_date between %(start_date)s and %(end_date)s
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        security_point_data = pd.read_sql_query(sql, engine, params=args)
        security_point_data.set_index(security_point_data["trade_date"], inplace=True)
        security_point_data = security_point_data.sort_index()

        return security_point_data

    def get_security_daily_basic_data(self, ts_code, start_date, end_date):
        sql = """
        select ts_code, trade_date, close, turnover_rate, turnover_rate_f, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, total_share, float_share, free_share, total_mv, circ_mv from security_daily_basic 
        where ts_code = %(ts_code)s and trade_date between %(start_date)s and %(end_date)s
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        security_daily_basic_data = pd.read_sql_query(sql, engine, params=args)
        security_daily_basic_data.set_index(security_daily_basic_data["trade_date"], inplace=True)
        security_daily_basic_data = security_daily_basic_data.sort_index()

        return security_daily_basic_data

    def get_future_security_point_data(self, ts_code, start_date, end_date):
        sql = """
        select `ts_code`, `trade_date`, `pre_close`, `pre_settle`, `open`, `high`, `low`, `close`, `settle`, `change1`, `change2`, `vol`, `amount`, `oi`, `oi_chg` from future_daily_point_data 
        where ts_code = %(ts_code)s and trade_date between %(start_date)s and %(end_date)s
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        security_point_data = pd.read_sql_query(sql, engine, params=args)
        security_point_data.set_index(security_point_data["trade_date"], inplace=True)
        security_point_data = security_point_data.sort_index()

        return security_point_data


if __name__ == "__main__":
    ss = SecurityData()
    ff = ss.get_future_security_point_data('P2001.DCE', datetime.datetime(2019, 11, 1), datetime.datetime(2019, 11, 21))
    print(ff)
    aa = 1
