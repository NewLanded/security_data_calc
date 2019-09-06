import datetime

from util.util_data.security_data import SecurityData

ts_code = "600030.SH"
security_point_data = SecurityData().get_security_point_data(ts_code, datetime.datetime(2016, 1, 1), datetime.datetime(2019, 3, 22))
security_daily_basic_data = SecurityData().get_security_daily_basic_data(ts_code, datetime.datetime(2016, 1, 1), datetime.datetime(2019, 3, 22))
security_point_data["turnover_rate"] = security_daily_basic_data["turnover_rate_f"]
security_point_data.drop("pre_close", axis=1, inplace=True)
security_point_data.drop("vol", axis=1, inplace=True)
security_point_data.drop("amount", axis=1, inplace=True)
security_point_data.drop("change", axis=1, inplace=True)
security_point_data.drop("ts_code", axis=1, inplace=True)
security_point_data.to_csv('./' + ts_code + '.csv', index=False, columns=['trade_date', 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg'], header=False)