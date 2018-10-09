import datetime

from source.util.util_base.db_util import get_connection, get_boolean_value, get_multi_data


class SecurityData:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_security_point_data(self, ts_code, start_date, end_date):
        sql = """
        select ts_code, trade_date, `open`, high, low, `close`, pre_close, `change`, pct_change, vol, amount from security_point_data 
        where ts_code = :ts_code and trade_date between :start_date and :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(self._session, sql, args)

        security_point_data = {}
        for ts_code, trade_date, open_point, high, low, close, pre_close, change, pct_change, vol, amount in result:
            security_point_data[trade_date] = {
                "open": open_point,
                "high": high,
                "low": low,
                "close": close,
                "pre_close": pre_close,
                "change": change,
                "pct_change": pct_change / 100,
                "vol": vol,
                "amount": amount,
            }

        return security_point_data

    def get_security_daily_basic_data(self, ts_code, start_date, end_date):
        sql = """
        select ts_code, trade_date, close, turnover_rate, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, total_share, float_share, free_share, total_mv, circ_mv from security_point_data 
        where ts_code = :ts_code and trade_date between :start_date and :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(self._session, sql, args)

        security_point_data = {}
        for ts_code, trade_date, close, turnover_rate, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, total_share, float_share, free_share, total_mv, circ_mv in result:
            security_point_data[trade_date] = {
                "close": close,
                "turnover_rate": turnover_rate / 100 if turnover_rate else turnover_rate,
                "volume_ratio": volume_ratio,
                "pe": pe,
                "pe_ttm": pe_ttm,
                "pb": pb,
                "ps": ps,
                "ps_ttm": ps_ttm,
                "total_share": total_share,
                "float_share": float_share,
                "free_share": free_share,
                "total_mv": total_mv,
                "circ_mv": circ_mv,
            }

        return security_point_data


if __name__ == "__main__":
    ss = SecurityData()
    ff = ss.get_security_point_data("000001.SZ", datetime.datetime(2018, 8, 1), datetime.datetime(2018, 8, 10))
    aa = 1

